# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NN_Join_gui
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

from os.path import dirname
from os.path import join

from PyQt4 import uic
from PyQt4.QtCore import SIGNAL, QObject, QThread, Qt, QCoreApplication
from PyQt4.QtGui import QDialog, QDialogButtonBox, QProgressBar, QPushButton

from qgis.core import QgsMessageLog, QgsMapLayerRegistry
from qgis.core import QGis, QgsVectorLayer, QgsMapLayer
from qgis.gui import QgsMessageBar

from NNJoin_engine import Worker

FORM_CLASS, _ = uic.loadUiType(join(
    dirname(__file__), 'ui_frmNNJoin.ui'))


class NNJoinDialog(QDialog, FORM_CLASS):
    def __init__(self, iface, parent=None):
        """Constructor."""
        self.iface = iface
        self.NNJOIN = self.tr('NNJoin')
        self.CANCEL = self.tr('Cancel')
        self.CLOSE = self.tr('Close')
        self.OK = self.tr('OK')
        super(NNJoinDialog, self).__init__(parent)
        # The following makes the plugin dialog window always stay
        # on top (above all other windows):
        #QDialog.__init__(self, None, Qt.WindowStaysOnTopHint)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html#widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        # Modify ui components
        okButton = self.button_box.button(QDialogButtonBox.Ok)
        okButton.setText(self.OK)
        cancelButton = self.button_box.button(QDialogButtonBox.Cancel)
        cancelButton.setText(self.CANCEL)
        closeButton = self.button_box.button(QDialogButtonBox.Close)
        closeButton.setText(self.CLOSE)
        self.approximate_input_geom_cb.setCheckState(Qt.Unchecked)
        self.approximate_input_geom_cb.setVisible(False)
        self.use_index_cb.setCheckState(Qt.Unchecked)
        self.use_index_cb.setVisible(False)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

        # Connect signals
        okButton.clicked.connect(self.startWorker)
        cancelButton.clicked.connect(self.killWorker)
        closeButton.clicked.connect(self.reject)
        self.approximate_input_geom_cb.stateChanged['int'].connect(self.useindexchanged)
        inpIndexCh = self.inputVectorLayer.currentIndexChanged['QString']
        inpIndexCh.connect(self.layerchanged)
        joinIndexCh = self.joinVectorLayer.currentIndexChanged['QString']
        joinIndexCh.connect(self.layerchanged)
        self.iface.legendInterface().itemAdded.connect(self.layerindexchanged)
        self.iface.legendInterface().itemRemoved.connect(self.layerindexchanged)
        # pyuic4 uses old style connections, so the disconnect has
        # to be old style!
        # so does not work with pyuic4:
        #self.button_box.rejected.disconnect(self.reject)
        QObject.disconnect(self.button_box, SIGNAL("rejected()"), self.reject)

        # Set instance variables
        self.mem_layer = None
        self.worker = None
        self.NNJOIN = self.tr('NNJoin')

    def startWorker(self):
        """Initialises and starts the worker thread."""
        layerindex = self.inputVectorLayer.currentIndex()
        layerId = self.inputVectorLayer.itemData(layerindex)
        inputlayer = QgsMapLayerRegistry.instance().mapLayer(layerId)
        if inputlayer is None:
            self.showError(self.tr('No input layer defined'))
            return
        joinindex = self.joinVectorLayer.currentIndex()
        joinlayerId = self.joinVectorLayer.itemData(joinindex)
        joinlayer = QgsMapLayerRegistry.instance().mapLayer(joinlayerId)
        if joinlayer is None:
            self.showError(self.tr('No join layer defined'))
            return
        outputlayername = self.outputDataset.text()
        approximateinputgeom = self.approximate_input_geom_cb.isChecked()
        joinprefix = self.joinPrefix.text()
        useindex = self.use_index_cb.isChecked()
        # create a new worker instance
        worker = Worker(inputlayer, joinlayer, outputlayername,
                        approximateinputgeom, joinprefix, useindex)
        # configure the QgsMessageBar
        msgBar = self.iface.messageBar().createMessage(self.tr('Joining'), '')
        self.aprogressBar = QProgressBar()
        self.aprogressBar.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        acancelButton = QPushButton()
        acancelButton.setText(self.CANCEL)
        acancelButton.clicked.connect(self.killWorker)
        msgBar.layout().addWidget(self.aprogressBar)
        msgBar.layout().addWidget(acancelButton)
        # Has to be popped after the thread has finished (in
        # workerFinished).
        self.iface.messageBar().pushWidget(msgBar,
                                           self.iface.messageBar().INFO)
        self.messageBar = msgBar
        # start the worker in a new thread
        thread = QThread(self)
        worker.moveToThread(thread)
        worker.finished.connect(self.workerFinished)
        worker.error.connect(self.workerError)
        worker.status.connect(self.workerInfo)
        worker.progress.connect(self.progressBar.setValue)
        worker.progress.connect(self.aprogressBar.setValue)
        thread.started.connect(worker.run)
        thread.start()
        self.thread = thread
        self.worker = worker
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
        self.button_box.button(QDialogButtonBox.Close).setEnabled(False)
        if layerId == joinlayerId:
            self.showInfo("The join layer is the same as the"
                             " input layer - doing a self join!")

    def workerFinished(self, ok, ret):
        """Handles the output from the worker and cleans up after the
           worker has finished."""
        # clean up the worker and thread
        self.worker.deleteLater()
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()
        # remove widget from message bar (pop)
        self.iface.messageBar().popWidget(self.messageBar)
        if ok and ret is not None:
            # report the result
            mem_layer = ret
            QgsMessageLog.logMessage(self.tr('NNJoin finished'),
                                     self.NNJOIN, QgsMessageLog.INFO)
            mem_layer.dataProvider().updateExtents()
            mem_layer.commitChanges()
            QgsMapLayerRegistry.instance().addMapLayer(mem_layer)
        else:
            # notify the user that something went wrong
            if not ok:
                self.showError(self.tr('Aborted') + '!')
            else:
                self.showError(self.tr('No layer created') + '!')
        self.progressBar.setValue(0.0)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
        self.button_box.button(QDialogButtonBox.Close).setEnabled(True)

    def workerError(self, exception_string):
        """Report an error from the worker."""
        QgsMessageLog.logMessage(self.tr('Worker failed - exception') +
                                 ': ' + str(exception_string), self.NNJOIN,
                                 QgsMessageLog.CRITICAL)

    def workerInfo(self, message_string):
        """Report an info message from the worker."""
        QgsMessageLog.logMessage(self.tr('Worker') + ': ' + message_string,
                                 self.NNJOIN, QgsMessageLog.INFO)

    def layerchanged(self, number=0):
        """Do the necessary updates after a layer selection has
           been changed."""
        layerindex = self.inputVectorLayer.currentIndex()
        layerId = self.inputVectorLayer.itemData(layerindex)
        inputlayer = QgsMapLayerRegistry.instance().mapLayer(layerId)
        joinindex = self.joinVectorLayer.currentIndex()
        joinlayerId = self.joinVectorLayer.itemData(joinindex)
        joinlayer = QgsMapLayerRegistry.instance().mapLayer(joinlayerId)
        if inputlayer is not None:
            inputwkbtype = inputlayer.wkbType()
            inputlayerwkbtext = self.getwkbtext(inputwkbtype)
            self.inputgeometrytypelabel.setText(inputlayerwkbtext)
        if joinlayer is not None:
            joinwkbtype = joinlayer.wkbType()
            joinlayerwkbtext = self.getwkbtext(joinwkbtype)
            self.joingeometrytypelabel.setText(joinlayerwkbtext)
        if inputlayer is not None and joinlayer is not None:
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
        self.updateui()

    def useindexchanged(self, number=0):
        self.updateui()

    def layerindexchanged(self):
        # Repopulate the input and join layer combo boxes
        self.inputVectorLayer.clear()
        for alayer in self.iface.legendInterface().layers():
            if alayer.type() == QgsMapLayer.VectorLayer:
                self.inputVectorLayer.addItem(alayer.name(), alayer.id())
        self.joinVectorLayer.clear()
        for alayer in self.iface.legendInterface().layers():
            if alayer.type() == QgsMapLayer.VectorLayer:
                self.joinVectorLayer.addItem(alayer.name(), alayer.id())

        self.updateui()

    def updateui(self):
        """Do the necessary updates after a layer selection has
           been changed."""
        self.outputDataset.setText(self.inputVectorLayer.currentText() +
                                   '_' + self.joinVectorLayer.currentText())
        layerindex = self.inputVectorLayer.currentIndex()
        layerId = self.inputVectorLayer.itemData(layerindex)
        inputlayer = QgsMapLayerRegistry.instance().mapLayer(layerId)
        joinindex = self.joinVectorLayer.currentIndex()
        joinlayerId = self.joinVectorLayer.itemData(joinindex)
        joinlayer = QgsMapLayerRegistry.instance().mapLayer(joinlayerId)
        if (inputlayer is not None and joinlayer is not None and
                inputlayer.dataProvider().crs() !=
                joinlayer.dataProvider().crs()):
            self.showWarning('Layers have different CRS - results may'
                             'not be correct')
        if inputlayer is not None:
            geometryType = inputlayer.geometryType()
            wkbType = inputlayer.wkbType()
            joinwkbType = QGis.WKBUnknown
            if joinlayer is not None:
                joinwkbType = joinlayer.wkbType()
            feats = inputlayer.getFeatures()
            # It the input layer is not a point layer, allow choosing
            # approximate geometry (centroid)
            if wkbType == QGis.WKBPoint or wkbType == QGis.WKBPoint25D:
                self.approximate_input_geom_cb.setCheckState(Qt.Unchecked)
                self.approximate_input_geom_cb.setVisible(False)
            else:
                self.approximate_input_geom_cb.setVisible(True)
            # Update the use index checkbox:
            if ((wkbType == QGis.WKBPoint or wkbType == QGis.WKBPoint25D or
                    self.approximate_input_geom_cb.isChecked()) and
                    not (joinwkbType == QGis.WKBPoint or
                    joinwkbType == QGis.WKBPoint25D)):
                self.use_index_cb.setVisible(True)
            else:
                self.use_index_cb.setCheckState(Qt.Unchecked)
                self.use_index_cb.setVisible(False)
        else:
            self.approximate_input_geom_cb.setVisible(False)
            self.use_index_cb.setVisible(False)

    def getwkbtext(self, number):
        if number == QGis.WKBUnknown:
            return "Unknown"
        elif number == QGis.WKBPoint:
            return "Point"
        elif number == QGis.WKBLineString:
            return "LineString"
        elif number == QGis.WKBPolygon:
            return "Polygon"
        elif number == QGis.WKBMultiPoint :
            return "MultiPoint"
        elif number == QGis.WKBMultiLineString :
            return "MultiLineString"
        elif number == QGis.WKBMultiPolygon :
            return "MultiPolygon"
        elif number == QGis.WKBNoGeometry :
            return "NoGeometry"
        elif number == QGis.WKBPoint25D:
            return "Point25D"
        elif number == QGis.WKBLineString25D:
            return "LineString25D"
        elif number == QGis.WKBPolygon25D:
            return "Polygon25D"
        elif number == QGis.WKBMultiPoint25D:
            return "MultiPoint25D"
        elif number == QGis.WKBMultiLineString25D:
            return "MultiLineString25D"
        elif number == QGis.WKBMultiPolygon25D:
            return "MultiPolygon25D"
        else:
            return "Don't know"

    def killWorker(self):
        """Kill the worker thread."""
        if self.worker is not None:
            QgsMessageLog.logMessage(self.tr('Killing worker'),
                                     self.NNJOIN, QgsMessageLog.INFO)
            self.worker.kill()

    def showError(self, text):
        """Show an error."""
        self.iface.messageBar().pushMessage(self.tr('Error'), text,
                                            level=QgsMessageBar.CRITICAL,
                                            duration=3)
        QgsMessageLog.logMessage('Error: ' + text, self.NNJOIN,
                                 QgsMessageLog.CRITICAL)

    def showWarning(self, text):
        """Show a warning."""
        self.iface.messageBar().pushMessage(self.tr('Warning'), text,
                                            level=QgsMessageBar.WARNING,
                                            duration=2)
        QgsMessageLog.logMessage('Warning: ' + text, self.NNJOIN,
                                 QgsMessageLog.WARNING)

    def showInfo(self, text):
        """Show info."""
        self.iface.messageBar().pushMessage(self.tr('Info'), text,
                                            level=QgsMessageBar.INFO,
                                            duration=2)
        QgsMessageLog.logMessage('Info: ' + text, self.NNJOIN,
                                 QgsMessageLog.INFO)

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        return QCoreApplication.translate('NNJoinDialog', message)

    # Implement the accept method to avoid exiting the dialog when
    # starting the work
    def accept(self):
        """Accept override."""
        pass

    # Implement the reject method to have the possibility to avoid
    # exiting the dialog when cancelling
    def reject(self):
        """Reject override."""
        # exit the dialog
        QDialog.reject(self)
