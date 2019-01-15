# -*- coding: utf-8 -*-

"""
/***************************************************************************
 NNJoin
                                 A QGIS plugin
                              -------------------
        begin                : 2018-10-04
        copyright            : (C) 2018 by Håvard Tveite
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

__author__ = 'Håvard Tveite'
__date__ = '2018-10-04'
__copyright__ = '(C) 2018 by Håvard Tveite'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import math
from PyQt5.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterString)
from qgis.core import QgsWkbTypes
from qgis.core import QgsFeature, QgsSpatialIndex
from qgis.core import QgsFeatureRequest, QgsField, QgsFields
from qgis.core import QgsRectangle, QgsCoordinateTransform
# from qgis.core import QgsCoordinateTransformContext
from qgis.core import QgsProject  # CRS Transformation


class NNJoinAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    # Parameter names
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'
    JOIN = 'JOIN'
    INPUTAPPROXIMATION = 'INPUTAPPROXIMATION'
    JOINAPPROXIMATION = 'JOINAPPROXIMATION'
    JOINPREFIX = 'JOINPREFIX'
    DISTANCEFIELDNAME = 'DISTANCEFIELDNAME'

    EXCLUDECONTAINING = 'EXCLUDECONTAINING'
    USEJOINLAYERINDEX = 'USEJOINLAYERINDEX'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # Add the input feature source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Input layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        # Add a checkbox for input geometry approximation.
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.INPUTAPPROXIMATION,
                self.tr('Approximate input geometries by centroids'),
                False
            )
        )
        # Add the join feature source. It can have any kind of geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.JOIN,
                self.tr('Join layer'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        # Add a checkbox for join geometry approximation.
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.JOINAPPROXIMATION,
                self.tr('Approximate join geometries by bounding boxes'),
                False
            )
        )

        # Add a checkbox for using the join layer index.
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.USEJOINLAYERINDEX,
                self.tr('Use the join layer index'),
                True
            )
        )

        # Add a textfield for join prefix.
        self.addParameter(
            QgsProcessingParameterString(
                self.JOINPREFIX,
                self.tr('Prefix for the join attributes'),
                'join_'
            )
        )

        # Add a checkbox for exclude containing geometries.
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.EXCLUDECONTAINING,
                self.tr('Exclude containing geometries'),
                False
            )
        )

        # Add a feature sink in which to store the result of the join.
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

        # Add a textfield for the name of the distance field.
        self.addParameter(
            QgsProcessingParameterString(
                self.DISTANCEFIELDNAME,
                self.tr('Neighbour distance field name'),
                'distance'
            )
        )
    # end of initAlgorithm

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        inputsource = self.parameterAsSource(parameters, self.INPUT, context)
        self.inpvl = inputsource
        # Check if the input layer looks OK
        if self.inpvl is None:
            feedback.reportError('Input layer is missing!')
            return {self.OUTPUT: None}
        if self.inpvl.featureCount() == 0:
            feedback.reportError('No features in the input layer!')
            return {self.OUTPUT: None}
        feedback.pushInfo("Feature count, input: " +
                          str(self.inpvl.featureCount()))
        # Get the join source
        joinsource = self.parameterAsSource(parameters, self.JOIN, context)
        self.joinvl = joinsource
        # Check if the join layer looks OK
        if self.joinvl is None:
            feedback.reportError('Join layer is missing!')
            return {self.OUTPUT: None}
        if self.joinvl.featureCount() == 0:
            feedback.reportError('No features in the join layer!')
            return {self.OUTPUT: None}
        feedback.pushInfo("Feature count, join: " +
                          str(self.joinvl.featureCount()))



        # Get the rest of the parameters
        inpapprox = self.parameterAsBool(parameters, self.INPUTAPPROXIMATION, context)
        self.approximateinputgeom = inpapprox
        joinapprox = self.parameterAsBool(parameters, self.JOINAPPROXIMATION, context)
        self.usejoinlayerapprox = joinapprox
        usejoinindex = self.parameterAsBool(parameters, self.USEJOINLAYERINDEX, context)
        self.nonpointexactindex = usejoinindex
        excludecontaining = self.parameterAsBool(parameters, self.EXCLUDECONTAINING, context)
        self.excludecontaining = excludecontaining
        joinprefix = self.parameterAsString(parameters, self.JOINPREFIX, context)
        self.joinprefix = joinprefix
        distname = self.parameterAsString(parameters, self.DISTANCEFIELDNAME, context)
        self.distancename = distname

        # Prepare the fields for the output sink
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
            feedback.pushInfo('Unable to get any join layer fields')
        collission = True
        while collission:   # Iterate until there are no collissions
            collission = False
            for field in outfields:
                if field.name() == self.distancename:
                    feedback.pushInfo(
                          'Distance field already exists - renaming!')
                    # self.abort = True
                    # self.finished.emit(False, None)
                    # break
                    collission = True
                    self.distancename = self.distancename + '1'
        outfields.append(QgsField(self.distancename, QVariant.Double))
        fieldsqgs = QgsFields()
        for fields in outfields:
            fieldsqgs.append(fields)            

        # Configure the sink
        (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
                context, fieldsqgs, inputsource.wkbType(),
                inputsource.sourceCrs())
        # (sink, dest_id) = self.parameterAsSink(parameters, self.OUTPUT,
        #         context, inputsource.fields(), inputsource.wkbType(),
        #         inputsource.sourceCrs())

        # Check if the inputs are the same (self join)
        self.selfjoin = False
        # if self.inpvl is self.joinvl:
        if (self.inpvl.sourceName() == self.joinvl.sourceName() and
            self.inpvl.fields() == self.joinvl.fields() and
            self.inpvl.wkbType() == self.joinvl.wkbType()):
            # This is a self join
            self.selfjoin = True
            feedback.pushInfo("Self join")

        # Compute the number of steps to display within the progress bar and
        # get features from source
        total = 100.0 / inputsource.featureCount() if inputsource.featureCount() else 0
        inpfeatures = inputsource.getFeatures()

        # For an index to be used, the input layer has to be a
        # point layer, the input layer geometries have to be
        # approximated to centroids, or the user has to have
        # accepted that a join layer index is used (for
        # non-point input layers).
        # (Could be extended to multipoint)
        # if (QgsWkbTypes.geometryType(self.inpvl.wkbType()) ==
        #     QgsWkbTypes.PointGeometry):
        if (self.inpvl.wkbType() == QgsWkbTypes.Point or
                self.inpvl.wkbType() == QgsWkbTypes.Point25D or
                self.approximateinputgeom or
                self.nonpointexactindex):
            # Create a spatial index to speed up joining
            feedback.pushInfo('Creating join layer index...')
            self.joinlind = QgsSpatialIndex()
            for current, feat in enumerate(self.joinvl.getFeatures()):
                # Allow user abort
                if feedback.isCanceled():
                    break
                self.joinlind.insertFeature(feat)
                feedback.setProgress(int(current * total))
            feedback.pushInfo('Join layer index created!')
            # self.percentage = 0

        # Does the join layer contain multi geometries?
        # Try to check the first feature
        # This is not used for anything yet
        self.joinmulti = False
        feats = self.joinvl.getFeatures()
        if feats is not None:
            testfeature = next(feats)
            feats.rewind()
            feats.close()
            if testfeature is not None:
                if testfeature.hasGeometry():
                    if testfeature.geometry().isMultipart():
                        self.joinmulti = True


        # Flag set by kill(), checked in the loop
        self.abort = False
        # Prepare for the join by fetching the layers into memory
        # Add the input features to a list
        self.inputf = []
        for f in self.inpvl.getFeatures():
            self.inputf.append(f)
        self.joinf = []
        for f in self.joinvl.getFeatures():
            self.joinf.append(f)
        self.features = []
        for current, feature in enumerate(self.inputf):
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            # Do the work:
            # # Add a feature in the sink
            # sink.addFeature(feature, QgsFeatureSink.FastInsert)
            self.do_indexjoin(feature, feedback)

            # Update the progress bar
            feedback.setProgress(int(current * total))
            # feedback.pushInfo(str(int(current * total)))
        sink.addFeatures(self.features, QgsFeatureSink.FastInsert)

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        return {self.OUTPUT: dest_id}
    # end of processAlgorithm

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'NNJoin'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'NNJoin'

    def tr(self, string):
        return QCoreApplication.translate('NNJoin', string)

    def createInstance(self):
        return NNJoinAlgorithm()

    def do_indexjoin(self, feat, feedback):
        '''Find the nearest neigbour using an index, if possible

        Parameter: feat -- The feature for which a neighbour is
                           sought
        '''
        infeature = feat
        # Get the feature ID
        infeatureid = infeature.id()
        # feedback.pushInfo('**infeatureid: ' + str(infeatureid))
        # Get the feature geometry
        inputgeom = infeature.geometry()
        # Shall approximate input geometries be used?
        if self.approximateinputgeom:
            # Use the centroid as the input geometry
            inputgeom = infeature.geometry().centroid()
        # Check if the coordinate systems are equal, if not,
        # transform the input feature!
        if (self.inpvl.sourceCrs() != self.joinvl.sourceCrs()):
            try:
                # inputgeom.transform(QgsCoordinateTransform(
                #     self.inpvl.crs(), self.joinvl.crs(), None))
                # transcontext = QgsCoordinateTransformContext()
                # inputgeom.transform(QgsCoordinateTransform(
                #     self.inpvl.crs(), self.joinvl.crs(), transcontext))
                inputgeom.transform(QgsCoordinateTransform(
                    self.inpvl.sourceCrs(), self.joinvl.sourceCrs(),
                    QgsProject.instance()))
            except:
                import traceback
                feedback.reportError(self.tr('CRS Transformation error!') +
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
                    nnfeature = next(self.joinvl.getFeatures(
                                QgsFeatureRequest(nearestids[fch])))
                # Not a self join
                else:
                    # Not a self join, so we can search for only the
                    # nearest neighbour (1)
                    nearestid = self.joinlind.nearestNeighbor(
                                           inputgeom.asPoint(), 1)[0]
                    # Get the feature!
                    nnfeature = next(self.joinvl.getFeatures(
                                      QgsFeatureRequest(nearestid)))
                mindist = inputgeom.distance(nnfeature.geometry())
            # Not points on the join side
            # # Handle common (non multi) non-point geometries
            # elif (self.joinvl.wkbType() == QgsWkbTypes.Polygon or
            #       self.joinvl.wkbType() == QgsWkbTypes.Polygon25D or
            #       self.joinvl.wkbType() == QgsWkbTypes.LineString or
            #       self.joinvl.wkbType() == QgsWkbTypes.LineString25D):
            # Handle all line and polygon geometries
            elif (QgsWkbTypes.geometryType(self.joinvl.wkbType()) ==
                  QgsWkbTypes.PolygonGeometry or
                  QgsWkbTypes.geometryType(self.joinvl.wkbType()) ==
                  QgsWkbTypes.LineGeometry):
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
                    # feedback.pushInfo('Exclude containing...')
                    nearfeature = next(self.joinvl.getFeatures(
                                           QgsFeatureRequest(nearestindexid)))
                    # Check for containment
                    contained = False
                    if nearfeature.geometry().contains(inputgeom):
                        contained = True
                    elif inputgeom.contains(nearfeature.geometry()):
                        # Should not happen with point input?
                        contained = True
                    else:
                        contained = False  # Superfluous
                    numberofnn = 2
                    # Assumes that nearestNeighbor returns hits in the same
                    # sequence for all numbers of nearest neighbour
                    while contained:
                        if feedback.isCanceled():
                            break
                        nearestindexes = self.joinlind.nearestNeighbor(
                                               inputgeom.asPoint(), numberofnn)
                        if len(nearestindexes) < numberofnn:
                            nearestindexid = nearestindexes[numberofnn - 2]
                            # feedback.pushInfo('No non-containing geometries!')
                            break
                        else:
                            nearestindexid = nearestindexes[numberofnn - 1]
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
                    if contained:
                        # No non-containing / contained features
                        attrs = []
                        atMapA = infeature.attributes()
                        attrs.extend(atMapA)
                        # Create the feature
                        outFeat = QgsFeature()
                        # Use the original input layer geometry!:
                        outFeat.setGeometry(infeature.geometry())
                        # Add the attributes
                        outFeat.setAttributes(attrs)
                        self.features.append(outFeat)
                        return
                # Get the feature among the candidates from the index
                nnfeature = next(self.joinvl.getFeatures(
                    QgsFeatureRequest(nearestindexid)))
                mindist = inputgeom.distance(nnfeature.geometry())
                px = inputgeom.asPoint().x()
                py = inputgeom.asPoint().y()
                # Search the neighbourhood
                closefids = self.joinlind.intersects(QgsRectangle(
                    px - mindist,
                    py - mindist,
                    px + mindist,
                    py + mindist))
                for closefid in closefids:
                    if feedback.isCanceled():
                        break
                    # Check for self join and same feature
                    if self.selfjoin and closefid == infeatureid:
                        continue
                    # If exclude containing, check for containment
                    if self.excludecontaining:
                        closefeature = next(self.joinvl.getFeatures(
                            QgsFeatureRequest(closefid)))
                        # Check for containment
                        if closefeature.geometry().contains(
                                                         inputgeom.asPoint()):
                            continue
                    closef = next(self.joinvl.getFeatures(
                                   QgsFeatureRequest(closefid)))
                    thisdistance = inputgeom.distance(closef.geometry())
                    if thisdistance < mindist:
                        mindist = thisdistance
                        nnfeature = closef
                    if mindist == 0:
                        # feedback.pushInfo('  Mindist = 0!')
                        break
            # Other geometries than lines, polygons and point/point25
            # on the join side.  Could be multipoints
            else:
                # Join with no index use
                # Go through all the features from the join layer!
                for inFeatJoin in self.joinf:
                    if feedback.isCanceled():
                        break
                    joingeom = inFeatJoin.geometry()
                    thisdistance = inputgeom.distance(joingeom)
                    # If the distance is 0, check for equality of the
                    # features (in case it is a self join)
                    if (thisdistance == 0 and self.selfjoin and
                            infeatureid == inFeatJoin.id()):
                        continue
                    if self.excludecontaining and thisdistance == 0.0:
                        continue
                    if thisdistance < mindist:
                        mindist = thisdistance
                        nnfeature = inFeatJoin
                    # For 0 distance, settle with the first feature
                    if mindist == 0:
                        break
        # non (simple) point input geometries (could be multipoint),
        # for instance all line and polygon geometry types.
        else:
            if (self.nonpointexactindex):
                # "exclude containing" not respected!!!

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
                nnfeature = next(self.joinvl.getFeatures(
                                  QgsFeatureRequest(nearestid)))
                mindist = inputgeom.distance(nnfeature.geometry())
                # Calculate the search rectangle (inputgeom BBOX + mindist)
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
                    if feedback.isCanceled():
                        break
                    # Check for self join and identical feature
                    if self.selfjoin and closefid == infeatureid:
                        continue
                    closef = next(self.joinvl.getFeatures(
                                   QgsFeatureRequest(closefid)))
                    thisdistance = inputgeom.distance(closef.geometry())
                    #if self.excludecontaining and thisdistance == 0.0:
                    #    continue
                    if thisdistance < mindist:
                        mindist = thisdistance
                        nnfeature = closef
                    if mindist == 0:
                        break
            else:
                # Join with no index use
                # Check all the features of the join layer!
                feedback.pushInfo('No index, non-point input layer')
                mindist = float("inf")  # should not be necessary
                for inFeatJoin in self.joinf:
                    if feedback.isCanceled():
                        break
                    joingeom = inFeatJoin.geometry()
                    thisdistance = inputgeom.distance(joingeom)
                    # feedback.pushInfo('Distance: ' + str(thisdistance))
                    # if self.excludecontaining and math.isclose(thisdistance, 0.0):
                    if self.excludecontaining and thisdistance == 0.0:
                        continue
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
        if not (feedback.isCanceled() or self.abort):
            # feedback.pushInfo('Near feature - ' + str(nnfeature.id()))
            # Collect the attribute
            attrs = []
            atMapA = infeature.attributes()
            attrs.extend(atMapA)
            if nnfeature is not None:
                atMapB = nnfeature.attributes()
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
            self.features.append(outFeat)
            # self.mem_joinl.dataProvider().addFeatures([outFeat])
    # end of do_indexjoin


