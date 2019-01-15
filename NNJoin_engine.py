# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NNJoin_engine
                          NNJoinEngine of the NNJoin plugin
 Nearest neighbour spatial join
                             -------------------
        begin                : 2014-09-04
        git sha              : $Format:%H$
        copyright            : (C) 2014 by Håvard Tveite
        email                : havard.tveite@nmbu.no
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import QgsMessageLog
from qgis.core import QgsWkbTypes
from qgis.core import QgsVectorLayer, QgsFeature, QgsSpatialIndex
from qgis.core import QgsFeatureRequest, QgsField
from qgis.core import QgsRectangle, QgsCoordinateTransform
# from qgis.core import QgsCoordinateTransformContext
from qgis.core import QgsProject

# QGIS 3
from qgis.PyQt import QtCore
from qgis.PyQt.QtCore import QCoreApplication, QVariant


class Worker(QtCore.QObject):
    '''The worker that does the heavy lifting.
    /* QGIS offers spatial indexes to make spatial search more
     * effective.  QgsSpatialIndex will find the nearest index
     * (approximate) geometry (rectangle) for a supplied point.
     * QgsSpatialIndex will only give correct results when searching
     * for the nearest neighbour of a point in a point data set.
     * So something has to be done for non-point data sets
     *
     * Non-point join data set:
     * A two pass search is performed.  First the index is used to
     * find the nearest index geometry (approximation - rectangle),
     * and then compute the distance to the actual indexed geometry.
     * A rectangle is constructed from this (maximum minimum)
     * distance, and this rectangle is used to find all features in
     * the join data set that may be the closest feature to the given
     * point.
     * For all the features is this candidate set, the actual
     * distance to the given point is calculated, and the nearest
     * feature is returned.
     *
     * Non-point input data set:
     * First the centroid of the non-point input geometry is
     * calculated.  Then the index is used to find the nearest
     * neighbour to this point (using the approximate index
     * geometry).
     * The distance vector to this feature, combined with the
     * bounding rectangle of the input feature is used to create a
     * search rectangle to find the candidate join geometries.
     * For all the features is this candidate set, the actual
     * distance to the given feature is calculated, and the nearest
     * feature is returned.
     *
     * Joins involving multi-geometry data sets are not supported
     * by a spatial index.
     *
    */
    '''
    # Define the signals used to communicate back to the application
    progress = QtCore.pyqtSignal(float)  # For reporting progress
    status = QtCore.pyqtSignal(str)      # For reporting status
    error = QtCore.pyqtSignal(str)       # For reporting errors
    # Signal for sending over the result:
    finished = QtCore.pyqtSignal(bool, object)

    def __init__(self, inputvectorlayer, joinvectorlayer,
                 outputlayername, joinprefix,
                 distancefieldname="distance",
                 approximateinputgeom=False,
                 usejoinlayerapproximation=False,
                 usejoinlayerindex=True,
                 selectedinputonly=True,
                 selectedjoinonly=True,
                 excludecontaining=True):
        """Initialise.

        Arguments:
        inputvectorlayer -- (QgsVectorLayer) The base vector layer
                            for the join
        joinvectorlayer -- (QgsVectorLayer) the join layer
        outputlayername -- (string) the name of the output memory
                           layer
        joinprefix -- (string) the prefix to use for the join layer
                      attributes in the output layer
        distancefieldname -- name of the (new) field where neighbour
                             distance is stored
        approximateinputgeom -- (boolean) should the input geometry
                                be approximated?  Is only be set for
                                non-single-point layers
        usejoinlayerindexapproximation -- (boolean) should the index
                             geometry approximations be used for the
                             join?
        usejoinlayerindex -- (boolean) should an index for the join
                             layer be used.
        selectedinputonly -- Only selected features from the input
                             layer
        selectedjoinonly -- Only selected features from the join
                            layer
        excludecontaining -- exclude the containing polygon for points
        """

        QtCore.QObject.__init__(self)  # Essential!
        # Set a variable to control the use of indexes and exact
        # geometries for non-point input geometries
        self.nonpointexactindex = usejoinlayerindex
        # Creating instance variables from the parameters
        self.inpvl = inputvectorlayer
        self.joinvl = joinvectorlayer
        self.outputlayername = outputlayername
        self.joinprefix = joinprefix
        self.approximateinputgeom = approximateinputgeom
        self.usejoinlayerapprox = usejoinlayerapproximation
        self.selectedinonly = selectedinputonly
        self.selectedjoonly = selectedjoinonly
        self.excludecontaining = excludecontaining

        # Check if the layers are the same (self join)
        self.selfjoin = False
        if self.inpvl is self.joinvl:
            # This is a self join
            self.selfjoin = True
        # The name of the attribute for the calculated distance
        self.distancename = distancefieldname
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
        # calculate_progress (set when needed)
        self.feature_count = 1
        # The number of elements that is needed to increment the
        # progressbar (set when needed)
        self.increment = 0

    def run(self):
        try:
            # Check if the layers look OK
            if self.inpvl is None or self.joinvl is None:
                self.status.emit('Layer is missing!')
                self.finished.emit(False, None)
                return
            # Check if there are features in the layers
            incount = 0
            if self.selectedinonly:
                incount = self.inpvl.selectedFeatureCount()
            else:
                incount = self.inpvl.featureCount()
            joincount = 0
            if self.selectedjoonly:
                joincount = self.joinvl.selectedFeatureCount()
            else:
                joincount = self.joinvl.featureCount()
            if incount == 0 or joincount == 0:
                self.status.emit('Layer without features!')
                self.finished.emit(False, None)
                return
            # Check if the input layer has geometries
            if (self.inpvl.geometryType() == QgsWkbTypes.NullGeometry):
                self.status.emit('No geometry!')
                self.finished.emit(False, None)
                return
            # Check the geometry type and prepare the output layer
            inpwkbType = self.inpvl.wkbType()
            inpwkbtypetext = QgsWkbTypes.displayString(int(inpwkbType))
            # self.inputmulti = QgsWkbTypes.isMultiType(inpwkbType)
            # self.status.emit('wkbtype: ' + inpwkbtypetext)
            # geometryType = self.inpvl.geometryType()
            # geometrytypetext = 'Point'
            # if geometryType == QgsWkbTypes.PointGeometry:
            #     geometrytypetext = 'Point'
            # elif geometryType == QgsWkbTypes.LineGeometry:
            #     geometrytypetext = 'LineString'
            # elif geometryType == QgsWkbTypes.PolygonGeometry:
            #     geometrytypetext = 'Polygon'
            # if self.inputmulti:
            #     geometrytypetext = 'Multi' + geometrytypetext
            # geomttext = geometrytypetext

            geomttext = inpwkbtypetext
            # Set the coordinate reference system to the input
            # layer's CRS using authid (proj4 may be more robust)
            if self.inpvl.crs() is not None:
                geomttext = (geomttext + "?crs=" +
                             str(self.inpvl.crs().authid()))
            # Retrieve the fields from the input layer
            outfields = self.inpvl.fields().toList()
            # Retrieve the fields from the join layer
            if self.joinvl.fields() is not None:
                jfields = self.joinvl.fields().toList()
                for joinfield in jfields:
                    outfields.append(QgsField(self.joinprefix +
                                     str(joinfield.name()),
                                     joinfield.type()))
            else:
                self.status.emit('Unable to get any join layer fields')
            # Add the nearest neighbour distance field
            # Check if there is already a "distance" field
            # (should be avoided in the user interface)
            # Try a new name if there is a collission
            collission = True
            while collission:   # Iterate until there are no collissions
                collission = False
                for field in outfields:
                    # This check should not be necessary - handled in the UI
                    if field.name() == self.distancename:
                        self.status.emit(
                              'Distance field already exists - renaming!')
                        # self.abort = True
                        # self.finished.emit(False, None)
                        # break
                        collission = True
                        self.distancename = self.distancename + '1'
            outfields.append(QgsField(self.distancename, QVariant.Double))
            # Create a memory layer using a CRS description
            self.mem_joinl = QgsVectorLayer(geomttext,
                                            self.outputlayername,
                                            "memory")
            # Set the CRS to the inputlayer's CRS
            self.mem_joinl.setCrs(self.inpvl.crs())
            self.mem_joinl.startEditing()
            # Add the fields
            for field in outfields:
                self.mem_joinl.dataProvider().addAttributes([field])
            # For an index to be used, the input layer has to be a
            # point layer, the input layer geometries have to be
            # approximated to centroids, or the user has to have
            # accepted that a join layer index is used (for
            # non-point input layers).
            # (Could be extended to multipoint)
            if (self.inpvl.wkbType() == QgsWkbTypes.Point or
                    self.inpvl.wkbType() == QgsWkbTypes.Point25D or
                    self.approximateinputgeom or
                    self.nonpointexactindex):
                # Create a spatial index to speed up joining
                self.status.emit('Creating join layer index...')
                # Number of features in the input layer - used by
                # calculate_progress
                if self.selectedjoonly:
                    self.feature_count = self.joinvl.selectedFeatureCount()
                else:
                    self.feature_count = self.joinvl.featureCount()
                # The number of elements that is needed to increment the
                # progressbar - set early in run()
                self.increment = self.feature_count // 1000
                self.joinlind = QgsSpatialIndex()
                if self.selectedjoonly:
                    for feat in self.joinvl.getSelectedFeatures():
                        # Allow user abort
                        if self.abort is True:
                            break
                        self.joinlind.insertFeature(feat)
                        self.calculate_progress()
                else:
                    for feat in self.joinvl.getFeatures():
                        # Allow user abort
                        if self.abort is True:
                            break
                        self.joinlind.insertFeature(feat)
                        self.calculate_progress()
                self.status.emit('Join layer index created!')
                self.processed = 0
                self.percentage = 0
                # self.calculate_progress()
            # Does the join layer contain multi geometries?
            # Try to check the first feature
            # This is not used for anything yet
            self.joinmulti = False
            if self.selectedjoonly:
                feats = self.joinvl.getSelectedFeatures()
            else:
                feats = self.joinvl.getFeatures()
            if feats is not None:
                testfeature = next(feats)
                feats.rewind()
                feats.close()
                if testfeature is not None:
                    if testfeature.hasGeometry():
                        if testfeature.geometry().isMultipart():
                            self.joinmulti = True
            # Prepare for the join by fetching the layers into memory
            # Add the input features to a list
            self.inputf = []
            if self.selectedinonly:
                for f in self.inpvl.getSelectedFeatures():
                    self.inputf.append(f)
            else:
                for f in self.inpvl.getFeatures():
                    self.inputf.append(f)
            # Add the join features to a list
            self.joinf = []
            if self.selectedjoonly:
                for f in self.joinvl.getSelectedFeatures():
                    self.joinf.append(f)
            else:
                for f in self.joinvl.getFeatures():
                    self.joinf.append(f)
            self.features = []
            # Do the join!
            # Number of features in the input layer - used by
            # calculate_progress
            if self.selectedinonly:
                self.feature_count = self.inpvl.selectedFeatureCount()
            else:
                self.feature_count = self.inpvl.featureCount()
            # The number of elements that is needed to increment the
            # progressbar - set early in run()
            self.increment = self.feature_count // 1000
            # Using the original features from the input layer
            for feat in self.inputf:
                # Allow user abort
                if self.abort is True:
                    break
                self.do_indexjoin(feat)
                self.calculate_progress()
            self.mem_joinl.dataProvider().addFeatures(self.features)
            self.status.emit('Join finished')
        except:
            import traceback
            self.error.emit(traceback.format_exc())
            self.finished.emit(False, None)
            if self.mem_joinl is not None:
                self.mem_joinl.rollBack()
        else:
            self.mem_joinl.commitChanges()
            if self.abort:
                self.finished.emit(False, None)
            else:
                self.status.emit('Delivering the memory layer...')
                self.finished.emit(True, self.mem_joinl)

    def calculate_progress(self):
        '''Update progress and emit a signal with the percentage'''
        self.processed = self.processed + 1
        # update the progress bar at certain increments
        if (self.increment == 0 or
                self.processed % self.increment == 0):
            # Calculate percentage as integer
            perc_new = (self.processed * 100) / self.feature_count
            if perc_new > self.percentage:
                self.percentage = perc_new
                self.progress.emit(self.percentage)

    def kill(self):
        '''Kill the thread by setting the abort flag'''
        self.abort = True

    def do_indexjoin(self, feat):
        '''Find the nearest neigbour using an index, if possible

        Parameter: feat -- The feature for which a neighbour is
                           sought
        '''
        infeature = feat
        # Get the feature ID
        infeatureid = infeature.id()
        # self.status.emit('**infeatureid: ' + str(infeatureid))
        # Get the feature geometry
        inputgeom = infeature.geometry()
        # Shall approximate input geometries be used?
        if self.approximateinputgeom:
            # Use the centroid as the input geometry
            inputgeom = infeature.geometry().centroid()
        # Check if the coordinate systems are equal, if not,
        # transform the input feature!
        if (self.inpvl.crs() != self.joinvl.crs()):
            try:
                # inputgeom.transform(QgsCoordinateTransform(
                #     self.inpvl.crs(), self.joinvl.crs(), None))
                # transcontext = QgsCoordinateTransformContext()
                # inputgeom.transform(QgsCoordinateTransform(
                #     self.inpvl.crs(), self.joinvl.crs(), transcontext))
                inputgeom.transform(QgsCoordinateTransform(
                    self.inpvl.crs(), self.joinvl.crs(),
                    QgsProject.instance()))
            except:
                import traceback
                self.error.emit(self.tr('CRS Transformation error!') +
                                ' - ' + traceback.format_exc())
                self.abort = True
                return
        # Find the closest feature!
        nnfeature = None
        mindist = float("inf")

        # If the input layer's geometry type is point, or has been
        # approximated to point (centroid), then a join index will
        # be used.
        if (self.approximateinputgeom or
                self.inpvl.wkbType() == QgsWkbTypes.Point or
                self.inpvl.wkbType() == QgsWkbTypes.Point25D):
            # Are there points on the join side?
            # Then the index nearest neighbour function is sufficient
            if (self.usejoinlayerapprox or
                    self.joinvl.wkbType() == QgsWkbTypes.Point or
                    self.joinvl.wkbType() == QgsWkbTypes.Point25D):
                # Is it a self join?
                if self.selfjoin:
                    # Have to consider the two nearest neighbours
                    nearestids = self.joinlind.nearestNeighbor(
                                             inputgeom.asPoint(), 2)
                    fch = 0  # Which of the two features to choose
                    if (nearestids[0] == infeatureid and
                                               len(nearestids) > 1):
                        # The first feature is the same as the input
                        # feature, so choose the second one
                        fch = 1
                    # Get the feature!
                    if False:
                    #if self.selectedjoonly:
                        # This caused problems (wrong results) in QGIS 3.0.1
                        nnfeature = next(
                            self.joinvl.getSelectedFeatures(
                                QgsFeatureRequest(nearestids[fch])))
                    else:
                        nnfeature = next(self.joinvl.getFeatures(
                            QgsFeatureRequest(nearestids[fch])))
                # Not a self join
                else:
                    # Not a self join, so we can search for only the
                    # nearest neighbour (1)
                    nearestid = self.joinlind.nearestNeighbor(
                                           inputgeom.asPoint(), 1)[0]
                    # Get the feature!
                    if False:
                    #if self.selectedjoonly:
                        nnfeature = next(self.joinvl.getSelectedFeatures(
                                 QgsFeatureRequest(nearestid)))
                    else:
                        nnfeature = next(self.joinvl.getFeatures(
                                 QgsFeatureRequest(nearestid)))
                mindist = inputgeom.distance(nnfeature.geometry())
            # Not points on the join side
            # Handle common (non multi) non-point geometries
            elif (self.joinvl.wkbType() == QgsWkbTypes.Polygon or
                  self.joinvl.wkbType() == QgsWkbTypes.Polygon25D or
                  self.joinvl.wkbType() == QgsWkbTypes.LineString or
                  self.joinvl.wkbType() == QgsWkbTypes.LineString25D):
                # Use the join layer index to speed up the join when
                # the join layer geometry type is polygon or line
                # and the input layer geometry type is point or a
                # point approximation
                nearestindexid = self.joinlind.nearestNeighbor(
                    inputgeom.asPoint(), 1)[0]
                # Check for self join (possible if approx input)
                if self.selfjoin and nearestindexid == infeatureid:
                    # Self join and same feature, so get the
                    # first two neighbours
                    nearestindexes = self.joinlind.nearestNeighbor(
                                             inputgeom.asPoint(), 2)
                    nearestindexid = nearestindexes[0]
                    if (nearestindexid == infeatureid and
                                  len(nearestindexes) > 1):
                        nearestindexid = nearestindexes[1]

                # If exclude containing, check for containment
                if self.excludecontaining:
                    contained = False
                    nearfeature = next(self.joinvl.getFeatures(
                                           QgsFeatureRequest(nearestindexid)))
                    # Check for containment
                    if nearfeature.geometry().contains(inputgeom):
                        contained = True
                    if inputgeom.contains(nearfeature.geometry()):
                        contained = True
                    numberofnn = 2
                    # Assumes that nearestNeighbor returns hits in the same
                    # sequence for all numbers of nearest neighbour
                    while contained:
                        if self.abort is True:
                            break
                        nearestindexes = self.joinlind.nearestNeighbor(
                                               inputgeom.asPoint(), numberofnn)
                        if len(nearestindexes) < numberofnn:
                            nearestindexid = nearestindexes[numberofnn - 2]
                            self.status.emit('No non-containing geometries!')
                            break
                        else:
                            nearestindexid = nearestindexes[numberofnn - 1]
                            # Seems to respect selection...?
                            nearfeature = next(self.joinvl.getFeatures(
                                QgsFeatureRequest(nearestindexid)))
                            # Check for containment  # Works!
                            if nearfeature.geometry().contains(
                                                         inputgeom):
                                contained = True
                            elif inputgeom.contains(
                                    nearfeature.geometry()):
                                contained = True
                            else:
                                contained = False
                        numberofnn = numberofnn + 1
                    # end while

                # Get the feature among the candidates from the index
                #if self.selectedjoonly:
                #    # Does not get the correct feature!
                #    nnfeature = next(self.joinvl.getSelectedFeatures(
                #        QgsFeatureRequest(nearestindexid)))
                # This seems to work also in the presence of selections
                nnfeature = next(self.joinvl.getFeatures(
                    QgsFeatureRequest(nearestindexid)))
                mindist = inputgeom.distance(nnfeature.geometry())
                if mindist == 0:
                    insidep = nnfeature.geometry().contains(
                                                          inputgeom.asPoint())
                    # self.status.emit('0 distance! - ' + str(nearestindexid))
                    # self.status.emit('Inside: ' + str(insidep))
                px = inputgeom.asPoint().x()
                py = inputgeom.asPoint().y()
                # Search the neighbourhood
                closefids = self.joinlind.intersects(QgsRectangle(
                    px - mindist,
                    py - mindist,
                    px + mindist,
                    py + mindist))
                for closefid in closefids:
                    if self.abort is True:
                        break
                    # Check for self join and same feature
                    if self.selfjoin and closefid == infeatureid:
                        continue
                    # If exclude containing, check for containment
                    if self.excludecontaining:
                        # Seems to respect selection...?
                        closefeature = next(self.joinvl.getFeatures(
                            QgsFeatureRequest(closefid)))
                        # Check for containment
                        if closefeature.geometry().contains(
                                                         inputgeom.asPoint()):
                            continue
                    if False:
                    #if self.selectedjoonly:
                        closef = next(self.joinvl.getSelectedFeatures(
                            QgsFeatureRequest(closefid)))
                    else:
                        closef = next(self.joinvl.getFeatures(
                            QgsFeatureRequest(closefid)))
                    thisdistance = inputgeom.distance(closef.geometry())
                    if thisdistance < mindist:
                        mindist = thisdistance
                        nnfeature = closef
                    if mindist == 0:
                        # self.status.emit('  Mindist = 0!')
                        break
            # Other geometry on the join side (multi and more)
            else:
                # Join with no index use
                # Go through all the features from the join layer!
                for inFeatJoin in self.joinf:
                    if self.abort is True:
                        break
                    joingeom = inFeatJoin.geometry()
                    thisdistance = inputgeom.distance(joingeom)
                    # If the distance is 0, check for equality of the
                    # features (in case it is a self join)
                    if (thisdistance == 0 and self.selfjoin and
                            infeatureid == inFeatJoin.id()):
                        continue
                    if thisdistance < mindist:
                        mindist = thisdistance
                        nnfeature = inFeatJoin
                    # For 0 distance, settle with the first feature
                    if mindist == 0:
                        break
        # non (simple) point input geometries (could be multipoint)
        else:
            if (self.nonpointexactindex):
                # Use the spatial index on the join layer (default).
                # First we do an approximate search
                # Get the input geometry centroid
                centroid = infeature.geometry().centroid()
                centroidgeom = centroid.asPoint()
                # Find the nearest neighbour (index geometries only)
                nearestid = self.joinlind.nearestNeighbor(centroidgeom, 1)[0]
                # Check for self join
                if self.selfjoin and nearestid == infeatureid:
                    # Self join and same feature, so get the two
                    # first two neighbours
                    nearestindexes = self.joinlind.nearestNeighbor(
                        centroidgeom, 2)
                    nearestid = nearestindexes[0]
                    if nearestid == infeatureid and len(nearestindexes) > 1:
                        nearestid = nearestindexes[1]
                # Get the feature!
                if False:
                #if self.selectedjoonly:
                    nnfeature = next(self.joinvl.getSelectedFeatures(
                        QgsFeatureRequest(nearestid)))
                else:
                    nnfeature = next(self.joinvl.getFeatures(
                        QgsFeatureRequest(nearestid)))
                mindist = inputgeom.distance(nnfeature.geometry())
                # Calculate the search rectangle (inputgeom BBOX
                inpbbox = infeature.geometry().boundingBox()
                minx = inpbbox.xMinimum() - mindist
                maxx = inpbbox.xMaximum() + mindist
                miny = inpbbox.yMinimum() - mindist
                maxy = inpbbox.yMaximum() + mindist
                # minx = min(inpbbox.xMinimum(), centroidgeom.x() - mindist)
                # maxx = max(inpbbox.xMaximum(), centroidgeom.x() + mindist)
                # miny = min(inpbbox.yMinimum(), centroidgeom.y() - mindist)
                # maxy = max(inpbbox.yMaximum(), centroidgeom.y() + mindist)
                searchrectangle = QgsRectangle(minx, miny, maxx, maxy)
                # Fetch the candidate join geometries
                closefids = self.joinlind.intersects(searchrectangle)
                # Loop through the geometries and choose the closest
                # one
                for closefid in closefids:
                    if self.abort is True:
                        break
                    # Check for self join and identical feature
                    if self.selfjoin and closefid == infeatureid:
                        continue
                    if False:
                    #if self.selectedjoonly:
                        closef = next(self.joinvl.getSelectedFeatures(
                            QgsFeatureRequest(closefid)))
                    else:
                        closef = next(self.joinvl.getFeatures(
                            QgsFeatureRequest(closefid)))
                    thisdistance = inputgeom.distance(closef.geometry())
                    if thisdistance < mindist:
                        mindist = thisdistance
                        nnfeature = closef
                    if mindist == 0:
                        break
            else:
                # Join with no index use
                # Check all the features of the join layer!
                mindist = float("inf")  # should not be necessary
                for inFeatJoin in self.joinf:
                    if self.abort is True:
                        break
                    joingeom = inFeatJoin.geometry()
                    thisdistance = inputgeom.distance(joingeom)
                    # If the distance is 0, check for equality of the
                    # features (in case it is a self join)
                    if (thisdistance == 0 and self.selfjoin and
                            infeatureid == inFeatJoin.id()):
                        continue
                    if thisdistance < mindist:
                        mindist = thisdistance
                        nnfeature = inFeatJoin
                    # For 0 distance, settle with the first feature
                    if mindist == 0:
                        break
        if not self.abort:
            # self.status.emit('Near feature - ' + str(nnfeature.id()))
            # Collect the attribute
            atMapA = infeature.attributes()
            atMapB = nnfeature.attributes()
            attrs = []
            attrs.extend(atMapA)
            attrs.extend(atMapB)
            attrs.append(mindist)
            # Create the feature
            outFeat = QgsFeature()
            # Use the original input layer geometry!:
            outFeat.setGeometry(infeature.geometry())
            # Use the modified input layer geometry (could be
            # centroid)
            # outFeat.setGeometry(inputgeom)
            # Add the attributes
            outFeat.setAttributes(attrs)
            # self.calculate_progress()
            self.features.append(outFeat)
            # self.mem_joinl.dataProvider().addFeatures([outFeat])
    # end of do_indexjoin

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
