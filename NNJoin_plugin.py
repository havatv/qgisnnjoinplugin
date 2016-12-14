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
import os.path
# QGIS imports
from qgis.core import QgsMapLayerRegistry, QgsMapLayer
from qgis.core import QGis
#from qgis.core import QgsWkbTypes
#import processing

#QGIS 3
#from qgis.PyQt.QtCore import QSettings, QCoreApplication, QTranslator
#from qgis.PyQt.QtCore import qVersion
#from qgis.PyQt.QtWidgets import QAction, QMessageBox
#from qgis.PyQt.QtGui import QIcon

#QGIS 2
from PyQt4.QtCore import QSettings, QCoreApplication, QTranslator, qVersion
from PyQt4.QtGui import QAction, QMessageBox, QIcon

# Plugin imports
import sys
sys.path.append(os.path.dirname(__file__))
import resources_rc
from .NNJoin_gui import NNJoinDialog


class NNJoin(object):
    """QGIS NNJoin Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save a reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'NNJoin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.NNJOIN = self.tr('NNJoin')
        self.NNJOINAMP = self.tr('&NNJoin')
        self.toolbar = None
        # Separate toolbar for NNJoin:
        #self.toolbar = self.iface.addToolBar(self.NNJOIN)
        #self.toolbar.setObjectName(self.NNJOIN)

        # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('NNJoin', message)

    def initGui(self):
        # Create action that will start plugin configuration
        icon_path = os.path.join(os.path.dirname(__file__), "nnjoin.png")
        self.action = QAction(
            QIcon(icon_path),
            self.NNJOIN, self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)
        # Add toolbar button
        if hasattr(self.iface, 'addVectorToolBarIcon'):
            self.iface.addVectorToolBarIcon(self.action)
        else:
            self.iface.addToolBarIcon(self.action)
        # Add menu item
        if hasattr(self.iface, 'addPluginToVectorMenu'):
            self.iface.addPluginToVectorMenu(self.NNJOINAMP, self.action)
        else:
            self.iface.addPluginToMenu(self.NNJOINAMP, self.action)

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        # Remove the plugin menu item
        if hasattr(self.iface, 'removePluginVectorMenu'):
            self.iface.removePluginVectorMenu(self.NNJOINAMP, self.action)
        else:
            self.iface.removePluginMenu(self.NNJOINAMP, self.action)
        # Remove the plugin toolbar icon
        if hasattr(self.iface, 'removeVectorToolBarIcon'):
            self.iface.removeVectorToolBarIcon(self.action)
        else:
            self.iface.removeToolBarIcon(self.action)

    def run(self):
        """Run method that initialises and starts the user interface"""
        # Create the dialog (after translation) and keep reference
        self.dlg = NNJoinDialog(self.iface)
        # Intitalise the components
        self.dlg.progressBar.setValue(0.0)
        self.dlg.outputDataset.setText('Result')
        # Populate the input and join layer combo boxes
        layers = QgsMapLayerRegistry.instance().mapLayers()
        layerslist = []
        for id in layers.keys():
            if layers[id].type() == QgsMapLayer.VectorLayer:
                if not layers[id].isValid():
                    QMessageBox.information(None,
                        self.tr('Information'),
                        'Layer ' + layers[id].name() + ' is not valid')
                if layers[id].wkbType() != QGis.WKBNoGeometry:
                    layerslist.append((layers[id].name(), id))
        if len(layerslist) == 0 or len(layers) == 0:
            QMessageBox.information(None,
               self.tr('Information'),
               self.tr('Vector layers not found'))
            return
        # Add the layers to the layers combobox
        self.dlg.inputVectorLayer.clear()
        for layerdescription in layerslist:
            self.dlg.inputVectorLayer.addItem(layerdescription[0],
                                        layerdescription[1])
        #for alayer in self.iface.legendInterface().layers():
        #for alayer in layers:
        #    if alayer.type() == QgsMapLayer.VectorLayer:
        #        self.dlg.inputVectorLayer.addItem(alayer.name(), alayer.id())
        self.dlg.joinVectorLayer.clear()
        #for alayer in self.iface.legendInterface().layers():
        #for alayer in layers:
        #    if alayer.type() == QgsMapLayer.VectorLayer:
        #        self.dlg.joinVectorLayer.addItem(alayer.name(), alayer.id())
        # Add the layers to the layers combobox
        for layerdescription in layerslist:
            self.dlg.joinVectorLayer.addItem(layerdescription[0],
                                        layerdescription[1])
        # show the dialog (needed for the messagebar cancel button)
        self.dlg.show()
        # Run the dialog event loop
        self.dlg.exec_()
