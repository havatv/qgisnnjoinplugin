# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NNJoin - __init__.py
                                 A QGIS plugin

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

__author__ = 'Håvard Tveite'
__date__ = '2018-10-04'
__copyright__ = '(C) 2018 by Håvard Tveite'


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Return the NNJoin class.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    # Load the NNJoin class from the file NNJoin_plugin.
    from .NNJoin_plugin import NNJoin
    return NNJoin(iface)
