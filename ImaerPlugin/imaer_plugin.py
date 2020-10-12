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
import time
import webbrowser
import pathlib

from PyQt5.QtWidgets import QAction, QFileDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QVariant

from qgis.core import (
    QgsMessageLog,
    Qgis,
    QgsVectorLayer,
    QgsField,
    QgsProject,
    QgsApplication,
    QgsExpressionContextUtils,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsSettings)
from qgis.gui import QgsMapLayerComboBox

from .tasks import (
    ImportImaerCalculatorResultTask,
    ExportImaerCalculatorResultTask)
from .generate_calc_input import GenerateCalcInputDialog
from .configuration import ConfigurationDialog




class ImaerPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.task_manager = QgsApplication.taskManager()
        self.imaer_calc_layers = {}
        self.settings = QgsSettings()

        # Variable self.dev is set to True if a global variable terglobo_dev exists
        # holding the lowercase value 'on'. This is to ensure that any dev tricks
        # will never be visible for other plugin users.
        dev = QgsExpressionContextUtils.globalScope().variable('terglobo_dev')
        self.dev = dev is not None and dev == 'on'
        self.do_log = True


    def initGui(self):
        self.toolbar = self.iface.addToolBar("Imaer Toolbar")
        if self.dev:
             self.toolbar.setStyleSheet("QToolBar { background-color: rgba(200, 180, 200, 255); }")
        self.calc_result_file_dialog = QFileDialog()
        self.calc_input_file_dialog = QFileDialog()

        icon_import_calc = QIcon(os.path.join(self.plugin_dir, 'icon_import_calc_result.png'))
        self.import_calc_result_action = QAction(icon_import_calc, 'Import IMAER Calculator result gml', self.iface.mainWindow())
        self.import_calc_result_action.triggered.connect(self.run_import_calc_result)
        self.toolbar.addAction(self.import_calc_result_action)

        icon_export_calc = QIcon(os.path.join(self.plugin_dir, 'icon_export_calc_result.png'))
        self.export_calc_result_action = QAction(icon_export_calc, 'Export to IMAER Calculator result gml', self.iface.mainWindow())
        self.export_calc_result_action.triggered.connect(self.run_export_calc_result)
        self.toolbar.addAction(self.export_calc_result_action)

        icon_generate_calc_input = QIcon(os.path.join(self.plugin_dir, 'icon_generate_calc_input.png'))
        self.generate_calc_input_action = QAction(icon_generate_calc_input, 'Generate IMAER Calculator input gml', self.iface.mainWindow())
        self.generate_calc_input_action.triggered.connect(self.run_generate_calc_input)
        self.toolbar.addAction(self.generate_calc_input_action)

        self.generate_calc_input_dlg = GenerateCalcInputDialog(self, parent=self.iface.mainWindow())
        self.generate_calc_input_dlg.button_outfile.clicked.connect(self.browse_generate_calc_input_file)

        icon_configuration = QIcon(os.path.join(self.plugin_dir, 'icon_connect_at.svg'))
        self.configuration_action = QAction(icon_configuration, 'Configuration', self.iface.mainWindow())
        self.configuration_action.triggered.connect(self.open_configuration)
        self.toolbar.addAction(self.configuration_action)

        self.configuration_dlg = ConfigurationDialog(self, parent=self.iface.mainWindow())

        icon_documentation = QIcon(os.path.join(self.plugin_dir, 'icon_documentation.svg'))
        self.documentation_action = QAction(icon_documentation, 'Open online documentation', self.iface.mainWindow())
        self.documentation_action.triggered.connect(self.open_online_documentation)
        self.toolbar.addAction(self.documentation_action)

        self.iface.mapCanvas().currentLayerChanged.connect(self.update_export_calc_widgets)

        self.update_export_calc_widgets()


    def unload(self):
        self.iface.mapCanvas().currentLayerChanged.disconnect(self.update_export_calc_widgets)

        self.generate_calc_input_dlg.button_outfile.clicked.disconnect(self.browse_generate_calc_input_file)

        self.import_calc_result_action.triggered.disconnect(self.run_import_calc_result)
        self.toolbar.removeAction(self.import_calc_result_action)
        del self.import_calc_result_action

        self.export_calc_result_action.triggered.disconnect(self.run_export_calc_result)
        self.toolbar.removeAction(self.export_calc_result_action)
        del self.export_calc_result_action

        self.generate_calc_input_action.triggered.disconnect(self.run_generate_calc_input)
        self.toolbar.removeAction(self.generate_calc_input_action)
        del self.generate_calc_input_action

        self.configuration_action.triggered.disconnect(self.open_configuration)
        self.toolbar.removeAction(self.configuration_action)
        del self.configuration_action

        self.documentation_action.triggered.disconnect(self.open_online_documentation)
        self.toolbar.removeAction(self.documentation_action)
        del self.documentation_action

        del self.toolbar


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def run_import_calc_result(self):
        if self.dev:
            self.calc_result_file_dialog.setDirectory('/home/raymond/git/AERIUS-QGIS-plugins/demodata/')
        gml_fn, filter = self.calc_result_file_dialog.getOpenFileName(caption="Open Calculator result gml file", filter='*.gml', parent=self.iface.mainWindow())
        self.log(gml_fn)

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
        if self.dev:
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


    def suggest_export_calc_result_fn(self, gpkg_fn):
        time_str = time.strftime("%Y%m%d-%H%M%S")
        gpkg_path = pathlib.Path(gpkg_fn)
        gml_basename = f'{gpkg_path.stem}_modified-{time_str}.gml'
        gml_fn = os.path.join(gpkg_path.parent, gml_basename)
        return gml_fn


    def run_export_calc_result(self):
        self.log('run_export_calc_result()')

        receptor_layer = self.iface.activeLayer()
        metadata = self.get_imaer_calc_metadata(receptor_layer)

        if not metadata['is_imaer_calc_layer']:
            self.log('active layer is not an Imaer layer') #todo messagedlg error

        gml_fn = self.suggest_export_calc_result_fn(metadata['gpkg_fn'])
        gml_fn, filter = self.calc_result_file_dialog.getSaveFileName(caption="Save as Calculator result gml file", directory=gml_fn, parent=self.iface.mainWindow())
        #self.log(gml_fn)
        if gml_fn == '' and filter == '':
            return

        xml_lines = []
        for line in metadata['xml'].split('\n'):
            if not line.strip() == '':
                #print(line)
                xml_lines.append(line)

        task = ExportImaerCalculatorResultTask(receptor_layer, gml_fn, xml_lines)
        self.task_manager.addTask(task)


    def get_imaer_calc_metadata(self, layer):
        if layer is None:
            #print('layer is None')
            return

        layer_id = layer.id()

        if layer_id in self.imaer_calc_layers:
            #print('  in cache')
            return self.imaer_calc_layers[layer_id]

        self.imaer_calc_layers[layer_id] = {}
        self.imaer_calc_layers[layer_id]['is_imaer_calc_layer'] = False

        if not isinstance(layer, QgsVectorLayer):
            #print('  not vector')
            return self.imaer_calc_layers[layer_id]

        provider = layer.dataProvider()
        if not provider.wkbType() == 3:
            #print('  not polygon')
            return self.imaer_calc_layers[layer_id]

        ds = provider.dataSourceUri()
        #print(' ', ds)
        if '|layername=' in ds:
            gpkg_fn, gpkg_layer = ds.split('|layername=')
            #print(' ', gpkg_fn, gpkg_layer)
        else:
            return self.imaer_calc_layers[layer_id]
        if not gpkg_layer == 'receptors':
            #print('  not receptors')
            return self.imaer_calc_layers[layer_id]

        metadata_ds = '{}|layername=imaer_metadata'.format(gpkg_fn)
        #print(metadata_ds)
        try:
            md_layer = QgsVectorLayer(metadata_ds, 'metadata', 'ogr')
        except:
            #print(' print no metadata')
            return self.imaer_calc_layers[layer_id]
        for md_feat in md_layer.getFeatures():
           self.imaer_calc_layers[layer_id][md_feat[1]] = md_feat[2]
        self.imaer_calc_layers[layer_id]['is_imaer_calc_layer'] = True
        self.imaer_calc_layers[layer_id]['gpkg_fn'] = gpkg_fn

        return self.imaer_calc_layers[layer_id]


    def browse_generate_calc_input_file(self):
        if self.dev:
            out_path = '/home/raymond/terglobo/projecten/aerius/202007_calc_input_plugin/demodata/gen_calc_input'
        else:
            out_path = ''
        out_fn = time.strftime("calcinput_%Y%m%d_%H%M%S.gml")
        out_fn = os.path.join(out_path, out_fn)

        gml_outfn, filter = self.calc_input_file_dialog.getSaveFileName(caption="Save as Calculator input gml file", filter='*.gml', directory=out_fn, parent=self.iface.mainWindow())
        self.generate_calc_input_dlg.edit_outfile.setText(gml_outfn)


    def run_generate_calc_input(self):
        self.log('run_generate_calc_input()')
        self.generate_calc_input_dlg.show()
        result = self.generate_calc_input_dlg.exec_()
        #print(result)
        if result:
            self.log('starting calcinput generation ...')
            fcc = self.generate_calc_input_dlg.get_fcc_from_gui()
            fn = self.generate_calc_input_dlg.edit_outfile.text()
            if fcc.write_to_file(fn):
                self.iface.messageBar().pushMessage('Success', 'Imaer GML file saved as: <a href="{0}">{0}</a>'.format(fn), level=Qgis.Info, duration=10)
            else:
                self.iface.messageBar().pushMessage('Error', 'Could not export GML file to {0}'.format(fn), level=Qgis.Critical, duration=10)


    def update_export_calc_widgets(self):
        if self.iface.activeLayer() is not None:
            metadata = self.get_imaer_calc_metadata(self.iface.activeLayer())
            self.export_calc_result_action.setEnabled(metadata['is_imaer_calc_layer'])


    def open_online_documentation(self):
        doc_index_url = 'https://github.com/opengeogroep/AERIUS-QGIS-plugins/blob/v3new/documentation/00_index.md'
        webbrowser.open(doc_index_url)


    def open_configuration(self):
        self.log('open_configuration()')
        #self.configuration_dlg.show()
        self.configuration_dlg.load_ui_from_settings()
        result = self.configuration_dlg.exec_()
        print(result)
        if result:
            self.configuration_dlg.save_ui_to_settings()
