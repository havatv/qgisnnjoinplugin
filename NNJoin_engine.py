# -*- coding: utf-8 -*-
from qgis.core import *
from processing import *
from PyQt4 import QtCore
from PyQt4.QtCore import QCoreApplication
from qgis.core import QgsMessageLog, QgsMapLayerRegistry, QGis
from qgis.core import QgsVectorLayer, QgsFeature, QgsSpatialIndex
from qgis.core import QgsFeatureRequest

# Parameters:
#   inputvectorlayer - vector layer (QgsVectorLayer)
#   joinvectorlayer - vector layer (QgsVectorLayer)
#   outputlayername - string with the name of the output (memory) layer


class Worker(QtCore.QObject):
    '''The worker that does the heavy lifting.'''
    # Define the signals used to communicate
    progress = QtCore.pyqtSignal(float)  # For reporting progress
    status = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    #killed = QtCore.pyqtSignal()
    # Signal for sending over the result:
    finished = QtCore.pyqtSignal(bool, object)

    def __init__(self, inputvectorlayer, joinvectorlayer,
                 outputlayername, approximateinputgeom, joinprefix,
                 usejoinlayerindex):
        """Initialise.

        Arguments:
        inputvectorlayer -- (QgsVectorLayer) The base vector layer
                            for the join
        joinvectorlayer -- (QgsVectorLayer) the join layer
        outputlayername -- (string) the name of the output memory layer
        approximateinputgeom -- (boolean) should the input geometry
                                be approximated?  Is only be set for
                                non-single-point layers
        joinprefix -- (string) the prefix to use for the join layer
                      attributes in the output layer
        usejoinlayerindex -- (boolean) should an index for the join
                             layer be used.  Will only use the index
                             geometry approximations for the join
        """

        QtCore.QObject.__init__(self)  # Essential!
        # Creating instance variables from parameters
        self.inputvectorlayer = inputvectorlayer
        self.joinvectorlayer = joinvectorlayer
        self.outputlayername = outputlayername
        self.approximateinputgeom = approximateinputgeom
        self.joinprefix = joinprefix
        self.usejoinlayerindex = usejoinlayerindex
        # Creating instance variables for the progress bar ++
        # Number of elements that have been processed - updated by
        # calculate_progress
        self.processed = 0
        # Current percentage of progress - updated by
        # calculate_progress
        self.percentage = 0
        # Flag set by kill(), checked in the loop
        self.abort = False
        # Number of features in the input layer - used by
        # calculate_progress
        self.feature_count = self.inputvectorlayer.featureCount()
        # The number of elements that is needed to increment the
        # progressbar - set early in run()
        self.increment = self.feature_count // 1000

    def run(self):
        try:
            #self.status.emit('Started!')
            # Check the geometry type
            geometryType = self.inputvectorlayer.geometryType()
            geometrytypetext = 'Point'
            if geometryType == QGis.Point:
                geometrytypetext = 'Point'
            elif geometryType == QGis.Line:
                geometrytypetext = 'LineString'
            elif geometryType == QGis.Polygon:
                geometrytypetext = 'Polygon'
            multi = False
            feats = self.inputvectorlayer.getFeatures()
            if feats.next().geometry().isMultipart():
                multi = True
                geometrytypetext = 'Multi' + geometrytypetext
            feats.rewind()
            feats.close()
            geomparametertext = geometrytypetext
            # Set the coordinate reference system to the input layer's CRS
            if self.inputvectorlayer.dataProvider().crs() is not None:
                geomparametertext = (geomparametertext + "?crs=" +
                    str(self.inputvectorlayer.dataProvider().crs().authid()))
            # Create a memory layer
            outfields = self.inputvectorlayer.pendingFields().toList()
            jfields = self.joinvectorlayer.pendingFields().toList()
            for joinfield in jfields:
                outfields.append(QgsField(self.joinprefix +
                                 str(joinfield.name()),
                                 joinfield.type()))
            outfields.append(QgsField("distance", QVariant.Double))
            self.mem_joinlayer = QgsVectorLayer(geomparametertext,
                                                self.outputlayername,
                                                "memory")
            self.mem_joinlayer.startEditing()
            for field in outfields:
                self.mem_joinlayer.dataProvider().addAttributes([field])
            # For an index to be used, the input layer has to be a point
            # layer, or the input layer geometries have to be approximated
            # to centroids.
            # (Could be extended to multipoint)
            if (self.inputvectorlayer.wkbType() == QGis.WKBPoint or
                    self.inputvectorlayer.wkbType() == QGis.WKBPoint25D or
                    self.approximateinputgeom):
                # Create a spatial index to speed up joining of point
                # layer inputs
                self.status.emit('Creating index on the join layer...')
                self.joinlayerindex = QgsSpatialIndex()
                for feat in self.joinvectorlayer.getFeatures():
                    # Allow user abort
                    if self.abort is True:
                        break
                    self.joinlayerindex.insertFeature(feat)
                self.status.emit('Finised creating index on the join layer!')
            # Do the join!
            features = self.inputvectorlayer.getFeatures()
            for feat in features:
                # Allow user abort
                if self.abort is True:
                    break
                self.do_indexjoin(feat)
                self.calculate_progress()
            self.status.emit('Join finished')
        except:
            import traceback
            self.error.emit(traceback.format_exc())
            self.finished.emit(False, None)
            self.mem_joinlayer.rollback()
        else:
            self.mem_joinlayer.commitChanges()
            if self.abort:
                self.finished.emit(False, None)
            else:
                self.status.emit('Delivering the memory layer...')
                self.finished.emit(True, self.mem_joinlayer)

    def calculate_progress(self):
        '''Update progress and emit a signal with the percentage'''
        self.processed = self.processed + 1
        # update the progress bar at certain increments
        if self.increment == 0 or self.processed % self.increment == 0:
            percentage_new = (self.processed * 100) / self.feature_count
            if percentage_new > self.percentage:
                self.percentage = percentage_new
                self.progress.emit(self.percentage)

    def kill(self):
        '''Kill the thread by setting the abort flag'''
        self.abort = True

    def do_indexjoin(self, feat):
        '''Find the nearest neigbour using an index, if possible

        Parameter: feat -- The feature for which a neighbour is sought
        '''
        infeature = feat
        inputgeom = QgsGeometry(infeature.geometry())
        # Working with approximate geometries?
        if self.approximateinputgeom:
            # Use the centroid as the input geometry
            inputgeom = QgsGeometry(infeature.geometry()).centroid()
        # Check if the coordinate systems are equal, if not transform
        if (self.inputvectorlayer.dataProvider().crs() !=
                    self.joinvectorlayer.dataProvider().crs()):
            try:
                inputgeom.transform(QgsCoordinateTransform(
                        self.inputvectorlayer.dataProvider().crs(),
                        self.joinvectorlayer.dataProvider().crs()))
            except:
                self.error.emit(self.tr('CRS Transformation error!'))
                self.abort = True
                return
        nnfeature = None
        mindistance = float("inf")
        ## Find the closest feature!
        # The join index nearest neighbour function can be used as it
        # is when the join layer is a point layer (or the user wants
        # the index geometries to be used).  But the input layer
        # geometry type has to be point (either original or centroid
        # approximations
        if (   (self.usejoinlayerindex or
                self.joinvectorlayer.wkbType() == QGis.WKBPoint or
                self.joinvectorlayer.wkbType() == QGis.WKBPoint25D) and
                (self.approximateinputgeom or
                self.inputvectorlayer.wkbType() == QGis.WKBPoint or
                self.inputvectorlayer.wkbType() == QGis.WKBPoint25D)):
            # Check if it is a self join!
            if self.inputvectorlayer == self.joinvectorlayer:
                # Pick the second closest neighbour!
                # (the first is the point itself)
                nearestid = self.joinlayerindex.nearestNeighbor(inputgeom.asPoint(), 2)[1]
                nnfeature = self.joinvectorlayer.getFeatures(QgsFeatureRequest(nearestid)).next()
            # Not a self join:
            else:
                nearestid = self.joinlayerindex.nearestNeighbor(inputgeom.asPoint(), 1)[0]
                nnfeature = self.joinvectorlayer.getFeatures(QgsFeatureRequest(nearestid)).next()
            mindistance = inputgeom.distance(nnfeature.geometry())
        # Use the join layer index to speed up the join when the join
        # layer geometry type is polygon or line and the input layer
        # geometry type is point
        elif ( (self.joinvectorlayer.wkbType() == QGis.WKBPolygon or
                self.joinvectorlayer.wkbType() == QGis.WKBPolygon25D or
                self.joinvectorlayer.wkbType() == QGis.WKBLineString or
                self.joinvectorlayer.wkbType() == QGis.WKBLineString25D) and
                (self.approximateinputgeom or
                self.inputvectorlayer.wkbType() == QGis.WKBPoint or
                self.inputvectorlayer.wkbType() == QGis.WKBPoint25D)):
            nearestindexid = self.joinlayerindex.nearestNeighbor(inputgeom.asPoint(), 1)[0]
            nnfeature = self.joinvectorlayer.getFeatures(QgsFeatureRequest(nearestindexid)).next()
            mindistance = inputgeom.distance(nnfeature.geometry())
            px = inputgeom.asPoint().x()
            py = inputgeom.asPoint().y()
            closefeatureids = self.joinlayerindex.intersects(
                                  QgsRectangle(px - mindistance,
                                  py - mindistance, px + mindistance,
                                  py + mindistance))
            for closefeatureid in closefeatureids:
                if self.abort is True:
                    break
                closefeature = self.joinvectorlayer.getFeatures(QgsFeatureRequest(closefeatureid)).next()
                thisdistance = inputgeom.distance(closefeature.geometry())
                if thisdistance < mindistance:
                    mindistance = thisdistance
                    nnfeature = closefeature
                if mindistance == 0:
                    break
        # Join with no index use
        else:
            # Get all the features from the join layer!
            joinfeatures = self.joinvectorlayer.getFeatures()
            for inFeatJoin in joinfeatures:
                if self.abort is True:
                    break
                joingeom = QgsGeometry(inFeatJoin.geometry())
                thisdistance = inputgeom.distance(joingeom)
                # If the distance is 0, check for equality of the
                # features (in case it is a self join)
                if (thisdistance == 0 and
                        infeature.__dict__ == inFeatJoin.__dict__):
                    continue
                if thisdistance < mindistance:
                    mindistance = thisdistance
                    nnfeature = inFeatJoin
                # For 0 distance, choose the first feature
                if mindistance == 0:
                    break
        if not self.abort:
            atMapA = infeature.attributes()
            atMapB = nnfeature.attributes()
            attrs = []
            attrs.extend(atMapA)
            attrs.extend(atMapB)
            attrs.append(mindistance)

            outFeat = QgsFeature()
            # Use the original input layer geometry!:
            outFeat.setGeometry(QgsGeometry(infeature.geometry()))
            # Use the modified input layer geometry (could be centroid)
            #outFeat.setGeometry(QgsGeometry(inputgeom))
            outFeat.setAttributes(attrs)
            self.calculate_progress()
            self.mem_joinlayer.dataProvider().addFeatures([outFeat])

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('NNJoinEngine', message)
