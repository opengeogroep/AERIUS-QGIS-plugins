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

from qgis.core import (
    QgsMessageLog,
    Qgis,
    QgsVectorLayer,
    QgsField,
    QgsProject,
    QgsApplication)

from .tasks import ImportImaerCalculatorResultTask




class ImaerPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.task_manager = QgsApplication.taskManager()
        self.do_log = True


    def initGui(self):
        self.toolbar = self.iface.addToolBar("Imaer Toolbar")
        self.calc_file_dialog = QFileDialog()

        reader_icon = QIcon(os.path.join(self.plugin_dir, 'icon_reader.png'))
        self.reader_action = QAction(reader_icon, 'Import IMAER Calculator result gml', self.iface.mainWindow())
        self.reader_action.triggered.connect(self.calc_reader_run)
        self.toolbar.addAction(self.reader_action)


    def unload(self):
        self.reader_action.triggered.disconnect(self.calc_reader_run)
        self.toolbar.removeAction(self.reader_action)
        del self.reader_action
        del self.toolbar


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def calc_reader_run(self):
        self.calc_file_dialog.setDirectory('/home/raymond/git/AERIUS-QGIS-plugins/demodata/')
        gml_fn, filter = self.calc_file_dialog.getOpenFileName(caption = "Open Calculator result gml file", filter='*.gml', parent=self.iface.mainWindow())
        self.log(gml_fn)
        #print(gml_fn)

        if os.path.exists(os.path.dirname(gml_fn)):
            gpkg_fn = gml_fn.replace('.gml', '.gpkg')
            task = ImportImaerCalculatorResultTask(gml_fn, gpkg_fn, self.load_calc_layer)
            self.task_manager.addTask(task)
            self.log('added to task manager')


    def load_calc_layer(self, gpkg_fn, zoom=True):
        '''Callback function from the task after finishing the gpkg'''
        base = os.path.basename(gpkg_fn)
        stem, ext = os.path.splitext(base)
        layer_name = '{} receptors'.format(stem)
        self.log(layer_name)
        receptors_layer = QgsVectorLayer(gpkg_fn, layer_name, 'ogr')

        hexagon_qml = os.path.join(self.plugin_dir, 'styles', 'imaer_hexagon.qml')
        receptors_layer.loadNamedStyle(hexagon_qml)
        QgsProject.instance().addMapLayer(receptors_layer)

        if zoom:
            canvas = self.iface.mapCanvas()
            extent = receptors_layer.extent()
            extent.grow(100)
            canvas.setExtent(extent)
