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
    progress = QtCore.pyqtSignal(float) # For reporting progress
    status = QtCore.pyqtSignal(str)
    error = QtCore.pyqtSignal(str)
    #killed = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal(bool, object) # For sending over the result

    def __init__(self, inputvectorlayer, joinvectorlayer, outputlayername, approximateinputgeom, joinprefix, useindex):
        """Initialise.

        Arguments:
        inputvectorlayer -- the base vector layer for the join
        joinvectorlayer -- the join layer
        outputlayername -- the name of the output memory layer
        approximateinputgeom -- boolean: should the input geometry
                                be approximated?  Is only be set for
                                non-single-point layers
        joinprefix -- the prefix to use for the join layer attributes
                      in the output layer
        useindex -- boolean: should an index for the join layer be
                    used.
        """
        
        QtCore.QObject.__init__(self)  # Essential!
        # Creating instance variables from parameters
        self.inputvectorlayer = inputvectorlayer
        self.joinvectorlayer = joinvectorlayer
        self.outputlayername = outputlayername
        self.approximateinputgeom = approximateinputgeom
        self.joinprefix = joinprefix
        self.useindex = useindex
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
        self.increment = self.feature_count // 100

    def run(self):
        try:
            self.status.emit('Started!')
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
                geometrytypetext = 'Multi'+geometrytypetext
            feats.rewind()
            feats.close()
            geomparametertext = geometrytypetext
            # Set the coordinate reference system to the input layer's CRS
            if self.inputvectorlayer.dataProvider().crs() != None:
                geomparametertext = (geomparametertext + "?crs=" +
                    str(self.inputvectorlayer.dataProvider().crs().authid()))
                pass
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
            # For point input layers and approximate input geometries
            # (centroids), an index can be used:
            if ((geometrytypetext == 'Point' or self.approximateinputgeom) and
                    (self.useindex or
                    (self.joinvectorlayer.wkbType() == QGis.WKBPoint or
                    self.joinvectorlayer.wkbType() == QGis.WKBPoint25D)
                    #(self.joinvectorlayer.geometryType() == QGis.Point)
                    )):
                # Create a spatial index to speed up joining of point
                # layer inputs
                self.status.emit('Creating index...')
                self.joinlayerindex = QgsSpatialIndex()
                for feat in self.joinvectorlayer.getFeatures(): 
                    if self.abort is True:
                        break
                    self.joinlayerindex.insertFeature(feat)
                self.status.emit('Finised creating index!')
            features = self.inputvectorlayer.getFeatures()
            for feat in features:
                if self.abort is True:
                    break
                self.do_indexjoin(feat)
                self.calculate_progress()
            self.status.emit('Finished')
        except:
            import traceback
            self.error.emit(traceback.format_exc())
            self.finished.emit(False, None)
        else:
            if self.abort:
                self.finished.emit(False, None)
            else:
                self.finished.emit(True, self.mem_joinlayer)

    def calculate_progress(self):
        '''Updathe progress and emit a signal with the percantage'''
        self.processed = self.processed + 1
        # update the progress bar at certain increments
        if self.increment == 0 or self.processed % self.increment == 0:
            percentage_new = (self.processed * 100) / self.feature_count
            if percentage_new > self.percentage:
                self.percentage = percentage_new
                self.progress.emit(self.percentage)
                #self.status.emit('Task percentage: '+str(self.percentage))

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
            inputgeom = QgsGeometry(infeature.geometry()).centroid()
        # Check if the coordinate systems are equal
        if (self.inputvectorlayer.dataProvider().crs() !=
                        self.joinvectorlayer.dataProvider().crs()):
            inputgeom.transform(QgsCoordinateTransform(
                self.inputvectorlayer.dataProvider().crs(),
                self.joinvectorlayer.dataProvider().crs()))
        nnfeature = None
        mindistance = float("inf")
        ## Find the closest feature!
        # Should an index be used?
        if  ((self.useindex or
                (self.joinvectorlayer.wkbType() == QGis.WKBPoint or
                self.joinvectorlayer.wkbType() == QGis.WKBPoint25D)) and
                #self.joinvectorlayer.geometryType() == QGis.Point) and
                (self.approximateinputgeom or
                (self.inputvectorlayer.wkbType() == QGis.WKBPoint or
                self.inputvectorlayer.wkbType() == QGis.WKBPoint25D))):
                #(self.inputvectorlayer.geometryType() == QGis.Point and
                #not infeature.geometry().isMultipart()))):
            # Check if it is a self join!
            if self.inputvectorlayer == self.joinvectorlayer:
                nearestid = self.joinlayerindex.nearestNeighbor(inputgeom.asPoint(),2)[1]
                nnfeature = self.joinvectorlayer.getFeatures(QgsFeatureRequest(nearestid)).next()
            else:
                nearestid = self.joinlayerindex.nearestNeighbor(inputgeom.asPoint(),1)[0]
                nnfeature = self.joinvectorlayer.getFeatures(QgsFeatureRequest(nearestid)).next()
            mindistance = inputgeom.distance(QgsGeometry(nnfeature.geometry()))

        else:
            joinfeatures = self.joinvectorlayer.getFeatures()
            count = 0
            for inFeatJoin in joinfeatures:
                count = count + 1
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
        if not self.abort:
            atMapA = infeature.attributes()
            atMapB = nnfeature.attributes()
            attrs = []
            attrs.extend(atMapA)
            attrs.extend(atMapB)
            attrs.append(mindistance)

            outFeat = QgsFeature()
            # Use the original geometry!:
            outFeat.setGeometry(QgsGeometry(infeature.geometry()))
            outFeat.setAttributes(attrs)
            #self.status.emit('iter_features calculating progress')
            self.calculate_progress()
            #self.status.emit('iter_features progress calculated')
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
        return QCoreApplication.translate('NNJoinDialog', message)
