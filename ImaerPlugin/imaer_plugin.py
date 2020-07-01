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

from .tasks import (
    ImportImaerCalculatorResultTask,
    ExportImaerCalculatorResultTask)




class ImaerPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.task_manager = QgsApplication.taskManager()
        self.do_log = True


    def initGui(self):
        self.toolbar = self.iface.addToolBar("Imaer Toolbar")
        self.calc_file_dialog = QFileDialog()

        import_calc_icon = QIcon(os.path.join(self.plugin_dir, 'icon_calc_import.png'))
        self.import_calc_action = QAction(import_calc_icon, 'Import IMAER Calculator result gml', self.iface.mainWindow())
        self.import_calc_action.triggered.connect(self.run_import_calc)
        self.toolbar.addAction(self.import_calc_action)

        export_calc_icon = QIcon(os.path.join(self.plugin_dir, 'icon_calc_export.png'))
        self.export_calc_action = QAction(export_calc_icon, 'Export to IMAER Calculator result gml', self.iface.mainWindow())
        self.export_calc_action.triggered.connect(self.run_export_calc)
        self.toolbar.addAction(self.export_calc_action)


    def unload(self):
        self.import_calc_action.triggered.disconnect(self.run_import_calc)
        self.toolbar.removeAction(self.import_calc_action)
        del self.import_calc_action

        self.export_calc_action.triggered.disconnect(self.run_export_calc)
        self.toolbar.removeAction(self.export_calc_action)
        del self.export_calc_action

        del self.toolbar


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def run_import_calc(self):
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


    def run_export_calc(self):
        self.log('run_export_calc()')

        receptor_layer = self.iface.activeLayer()

        gml_fn = ''

        if self.is_imaer_layer(receptor_layer):
            task = ExportImaerCalculatorResultTask(receptor_layer, gml_fn)
            self.task_manager.addTask(task)


    def is_imaer_layer(self, receptor_layer):
        return True
