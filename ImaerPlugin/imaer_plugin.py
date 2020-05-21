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
from .imaerread import ImaerRead




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
        self.reader_action = QAction(reader_icon, 'Import IMAER result', self.iface.mainWindow())
        self.reader_action.triggered.connect(self.reader_run)
        self.toolbar.addAction(self.reader_action)

        self.reader_dlg.fileBrowseButton.clicked.connect(self.chooseFile)
        self.reader_dlg.gmlFileNameBox.textChanged.connect(self.gmlFileNameBoxChanged)

        #self.log('initGui')


    def unload(self):
        self.reader_action.triggered.disconnect(self.reader_run)
        self.toolbar.removeAction(self.reader_action)
        del self.reader_action
        del self.toolbar

        self.reader_dlg.fileBrowseButton.clicked.disconnect(self.chooseFile)
        self.reader_dlg.gmlFileNameBox.textChanged.disconnect(self.gmlFileNameBoxChanged)

        #self.log('unload')


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def reader_run(self):
        self.reader_dlg.show()
        result = self.reader_dlg.exec_()
        self.log(result)
        if result:
            self.doPoint = self.reader_dlg.point_checkBox.checkState()
            self.doHexagon = self.reader_dlg.hexagon_checkBox.checkState()

            # create new IMAER feature collection object
            featureCollection = ImaerRead(gmlFile = self.reader_dlg.gmlFileNameBox.text())

            self.attributes = featureCollection.attributeFields

            #create layers
            if self.doPoint:
                (self.pointLayer, self.pointProvider) = self.createLayer(dim=0, name="Deposition Points")
            else:
                self.pointProvider = None
            if self.doHexagon:
                (self.hexagonLayer, self.hexagonProvider) = self.createLayer(dim=2, name="Deposition Hexagons")
            else:
                self.hexagonProvider = None

            # start worker for reading features in different thread
            self.reader_dlg.startWorker(featureCollection, self.attributes, self.pointProvider, self.hexagonProvider)

            # add layers to map
            canvas = self.iface.mapCanvas()
            if self.doHexagon:
                hexagonQml = os.path.join(self.plugin_dir, 'styles', 'imaer_hexagon.qml')
                self.hexagonLayer.loadNamedStyle(hexagonQml)
                QgsProject.instance().addMapLayer(self.hexagonLayer)
            if self.doPoint:
                # TODO: create some point style too
                #self.pointLayer.loadNamedStyle()
                QgsProject.instance().addMapLayer(self.pointLayer)

    def chooseFile(self):
        """Opens the file dialog to pick a file to open"""
        filename, filter = QFileDialog.getOpenFileName(caption = "Open IMAER gml File", filter = '*.gml')
        self.reader_dlg.gmlFileNameBox.setText(filename)


    def gmlFileNameBoxChanged(self):
        """Enables the OK button after entering a file name"""
        filename = self.reader_dlg.gmlFileNameBox.text()
        enable_open = os.path.exists(os.path.dirname(filename))
        self.reader_dlg.cancel_open_button_box.button(QDialogButtonBox.Open).setEnabled(enable_open)


    def createLayer(self, dim=2, name="imaer layer"):
        """Creates a map layer of polygon (2) or point (0) type, and returns both the layer and the provider as a tuple.

        :param dim: dimension of the geometry
        :type dim: int

        :param name: layer name (defaults to 'imaer layer'
        :type ft: str
        """
        # create layer
        self.log('creating layer')
        if dim == 2:
            vl = QgsVectorLayer("Polygon?crs=EPSG:28992", name, "memory")
        else:
            vl = QgsVectorLayer("Point?crs=EPSG:28992", name, "memory")
        pr = vl.dataProvider()

        # add fields
        pr.addAttributes([QgsField("id", QVariant.String)])
        for subst in self.attributes:
            pr.addAttributes([QgsField(subst, QVariant.Double)])
        vl.updateFields()
        return (vl, pr)
