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
        self.imaer_calc_layers = {}
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

        self.iface.mapCanvas().currentLayerChanged.connect(self.update_export_calc_widgets)

        self.update_export_calc_widgets()


    def unload(self):
        self.iface.mapCanvas().currentLayerChanged.disconnect(self.update_export_calc_widgets)

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
        layer_data_source = '{}|layername={}'.format(gpkg_fn, 'receptors')
        receptors_layer = QgsVectorLayer(layer_data_source, layer_name, 'ogr')

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

        if self.is_imaer_calc_layer(receptor_layer):
            task = ExportImaerCalculatorResultTask(receptor_layer, gml_fn)
            self.task_manager.addTask(task)


    def get_imaer_calc_metadata(self, layer):
        layer_id = layer.id()
        print(layer_id)

        if layer_id in self.imaer_calc_layers:
            return self.imaer_calc_layers[layer_id]

        self.imaer_calc_layers[layer_id] = {}
        self.imaer_calc_layers[layer_id]['is_imaer_calc_layer'] = False

        if layer is None:
            return self.imaer_calc_layers[layer_id]
        print('is_imaer_calc_layer {}'.format(layer.name()))

        if not isinstance(layer, QgsVectorLayer):
            print('  not vector')
            return self.imaer_calc_layers[layer_id]

        provider = layer.dataProvider()
        if not provider.wkbType() == 3:
            print('  not polygon')
            return self.imaer_calc_layers[layer_id]

        ds = provider.dataSourceUri()
        print(' ', ds)
        if '|layername=' in ds:
            gpkg_fn, gpkg_layer = ds.split('|layername=')
            print(' ', gpkg_fn, gpkg_layer)
        else:
            return self.imaer_calc_layers[layer_id]
        if not gpkg_layer == 'receptors':
            print('  not receptors')
            return self.imaer_calc_layers[layer_id]

        metadata_ds = '{}|layername=imaer_metadata'.format(gpkg_fn)
        print(metadata_ds)
        try:
            md_layer = QgsVectorLayer(metadata_ds, 'metadata', 'ogr')
        except:
            print('  no metadata')
            return self.imaer_calc_layers[layer_id]
        for md_feat in md_layer.getFeatures():
           self.imaer_calc_layers[layer_id][md_feat[1]] = md_feat[2]
        self.imaer_calc_layers[layer_id]['is_imaer_calc_layer'] = True

        return self.imaer_calc_layers[layer_id]


    def update_export_calc_widgets(self):
        metadata = self.get_imaer_calc_metadata(self.iface.activeLayer())
        self.export_calc_action.setEnabled(metadata['is_imaer_calc_layer'])
