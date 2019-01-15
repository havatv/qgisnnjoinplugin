# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NNJoin
                                 A QGIS plugin
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

__author__ = 'Håvard Tveite'
__date__ = '2018-10-04'
__copyright__ = '(C) 2018 by Håvard Tveite'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

# import os
# import sys
# import inspect

# from qgis.core import QgsProcessingAlgorithm   # ???
from qgis.core import QgsApplication
import os.path
from .NNJoin_provider import NNJoinProvider

#cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
#if cmd_folder not in sys.path:
#    sys.path.insert(0, cmd_folder)


class NNJoinProcessingPlugin(object):

    def __init__(self):
        self.provider = NNJoinProvider()

    def initGui(self):
        QgsApplication.processingRegistry().addProvider(self.provider)

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)

