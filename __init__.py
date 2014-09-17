# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CoordinateScaling
                                 A QGIS plugin
 Scales the coordinates of a vector layer by a given factor
                             -------------------
        begin                : 2014-09-04
        copyright            : (C) 2014 by Håvard Tveite
        email                : havard.tveite@nmbu.no
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load CoordinateScaling class from file CoordinateScaling.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from NNJoin_plugin import NNJoin
    return NNJoin(iface)
