# -*- coding: utf-8 -*-
################################################################################
#
# begin:      2020-05-08
# copyright:  (C) 2020 by OpenGeoGroep
# email:      info@opengeogroep.nl

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
################################################################################

import os

from PyQt5.QtWidgets import QAction, QFileDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QVariant

from qgis.core import QgsMessageLog, Qgis, QgsVectorLayer, QgsField, QgsProject

from .imaer_reader_dialog import ImaerReaderDialog





class ImaerPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.do_log = True
        #self.log('init')


    def initGui(self):
        self.toolbar = self.iface.addToolBar("Imaer Toolbar")

        self.reader_dlg = ImaerReaderDialog()

        reader_icon = QIcon(os.path.join(self.plugin_dir, 'icon_reader.png'))
        self.reader_action = QAction(reader_icon, 'Import IMAER result gml', self.iface.mainWindow())
        self.reader_action.triggered.connect(self.reader_run)
        self.toolbar.addAction(self.reader_action)

        self.reader_dlg.fileBrowseButton.clicked.connect(self.chooseFile)
        self.reader_dlg.gmlFileNameBox.textChanged.connect(self.gmlFileNameBoxChanged)
        self.reader_dlg.workerEnd.connect(self.zoomToLayers)


    def unload(self):
        self.reader_action.triggered.disconnect(self.reader_run)
        self.toolbar.removeAction(self.reader_action)
        del self.reader_action
        del self.toolbar

        self.reader_dlg.fileBrowseButton.clicked.disconnect(self.chooseFile)
        self.reader_dlg.gmlFileNameBox.textChanged.disconnect(self.gmlFileNameBoxChanged)
        self.reader_dlg.workerEnd.disconnect(self.zoomToLayers)


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def reader_run(self):
        self.log('hiero')
        self.reader_dlg.gmlFileNameBox.setText('/home/raymond/git/AERIUS-QGIS-plugins/demodata/AERIUS_20200623162435_0_Situatie1.gml')
        self.reader_dlg.gmlFileNameBox.setText('/home/raymond/git/AERIUS-QGIS-plugins/demodata/AERIUS_20200623162435_0_Situatie1_4.gml')
        self.reader_dlg.show()
        result = self.reader_dlg.exec_()
        self.log(result)
        if result:
            self.reader_dlg.import_result_gml(self.reader_dlg.gmlFileNameBox.text())


    def chooseFile(self):
        """Opens the file dialog to pick a file to open"""
        filename, filter = QFileDialog.getOpenFileName(caption = "Open IMAER gml File", filter = '*.gml', parent=self.reader_dlg)
        self.reader_dlg.gmlFileNameBox.setText(filename)


    def gmlFileNameBoxChanged(self):
        """Enables the OK button after entering a file name"""
        filename = self.reader_dlg.gmlFileNameBox.text()
        enable_open = os.path.exists(os.path.dirname(filename))
        enable_open = True # !!!!!!!!!!!!!!!!!!!!!!!!
        self.reader_dlg.cancel_open_button_box.button(QDialogButtonBox.Open).setEnabled(enable_open)


    def zoomToLayers(self):
        canvas = self.iface.mapCanvas()
        if self.doHexagon:
            self.hexagonLayer.updateExtents()
            canvas.setExtent(self.hexagonLayer.extent())
        if self.doPoint:
            self.pointLayer.updateExtents()
            if not self.doHexagon:
                canvas.setExtent(self.pointLayer.extent())
        canvas.refresh()
