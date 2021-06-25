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

from qgis.PyQt.QtWidgets import QAction, QFileDialog, QDialogButtonBox
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtCore import QVariant, QStandardPaths

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

from ImaerPlugin.tasks import (
    ImportImaerCalculatorResultTask,
    ExportImaerCalculatorResultTask,
    ExtractGmlFromPdfTask)
from ImaerPlugin.generate_calc_input import GenerateCalcInputDialog
from ImaerPlugin.configuration import ConfigurationDialog
from ImaerPlugin.connect_receptorsets import ConnectReceptorSetsDialog
from ImaerPlugin.connect_jobs import ConnectJobsDialog
from ImaerPlugin.relate_calc_results import RelateCalcResultsDialog

from ImaerPlugin.connect import (
    AeriusConnection,
    AeriusOpenData
)




class ImaerPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.download_dir = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)
        self.task_manager = QgsApplication.taskManager()
        self.imaer_calc_layers = {}
        self.settings = QgsSettings()

        self.aerius_connection = AeriusConnection()

        # Variable self.dev is set to True if a global variable terglobo_dev exists
        # holding the lowercase value 'on'. This is to ensure that any dev tricks
        # will never be visible for other plugin users.
        dev = QgsExpressionContextUtils.globalScope().variable('terglobo_dev')
        self.dev = dev is not None and dev == 'on'
        self.do_log = True

        self.action_configuration = [
            {
                'name': 'import_calc_result',
                'icon': 'icon_import_calc_result.svg',
                'tool_tip': 'Import IMAER Calculator result GML',
                'triggered_slot': self.run_import_calc_result
            },{
                'name': 'export_calc_result',
                'icon': 'icon_export_calc_result.svg',
                'tool_tip': 'Export to IMAER Calculator result GML',
                'triggered_slot': self.run_export_calc_result
            },{
                'name': 'extract_gml_from_pdf',
                'icon': 'icon_extract_gml_from_pdf.svg',
                'tool_tip': 'Extract GML from Aerius PDF',
                'triggered_slot': self.run_extract_gml_from_pdf
            },{
                'name': 'generate_calc_input',
                'icon': 'icon_generate_calc_input.svg',
                'tool_tip': 'Generate IMAER Calculator input gml',
                'triggered_slot': self.run_generate_calc_input
            },{
                'name': 'relate_calc_results',
                'icon': 'icon_relate_calc_results.svg',
                'tool_tip': 'Relate Calculation results',
                'triggered_slot': self.run_relate_calc_results
            },{
                'name': 'add_open_data',
                'icon': 'icon_add_open_data_layer.svg',
                'tool_tip': 'Add Open Data Layer',
                'triggered_slot': self.open_add_open_data
            },{
                'name': 'connect_receptorsets',
                'icon': 'icon_connect_receptorsets.svg',
                'tool_tip': 'Receptor Sets',
                'triggered_slot': self.open_connect_receptorsets
            },{
                'name': 'connect_jobs',
                'icon': 'icon_connect_jobs.svg',
                'tool_tip': 'Jobs',
                'triggered_slot': self.open_connect_jobs
            },{
                'name': 'configuration',
                'icon': 'icon_configuration.svg',
                'tool_tip': 'Configure',
                'triggered_slot': self.open_configuration
            },{
                'name': 'documentation',
                'icon': 'icon_documentation.svg',
                'tool_tip': 'Open online documentation',
                'triggered_slot': self.open_online_documentation
            }
        ]
        self.actions = {}


    def initGui(self):
        # Create toolbar and actions
        self.toolbar = self.iface.addToolBar("Imaer Toolbar")
        if self.dev:
             self.toolbar.setStyleSheet("QToolBar { background-color: rgba(200, 180, 200, 255); }")

        for action_config in self.action_configuration:
            icon = QIcon(os.path.join(self.plugin_dir, 'img', action_config['icon']))
            action = QAction(icon, action_config['tool_tip'], self.iface.mainWindow())
            action.triggered.connect(action_config['triggered_slot'])
            self.toolbar.addAction(action)
            self.actions[action_config['name']] = action

        # Create dialogs
        self.calc_result_file_dialog = QFileDialog()
        self.calc_input_file_dialog = QFileDialog()

        self.generate_calc_input_dlg = GenerateCalcInputDialog(self, parent=self.iface.mainWindow())
        self.relate_calc_results_dlg = RelateCalcResultsDialog(self, parent=self.iface.mainWindow())
        self.configuration_dlg = ConfigurationDialog(self, parent=self.iface.mainWindow())
        self.connect_receptorsets_dlg = ConnectReceptorSetsDialog(self, parent=self.iface.mainWindow())
        self.connect_jobs_dlg = ConnectJobsDialog(self, parent=self.iface.mainWindow())

        # Widget update logic
        self.iface.mapCanvas().currentLayerChanged.connect(self.update_export_calc_widgets)
        self.update_all_widgets()


    def unload(self):
        '''Removes all plugin widgets and connections'''
        # Clean up connections
        self.iface.mapCanvas().currentLayerChanged.disconnect(self.update_export_calc_widgets)

        # Clean up actions and toolbar
        for action_config in self.action_configuration:
            name = action_config['name']
            action = self.actions[name]
            action.triggered.disconnect(action_config['triggered_slot'])
            self.toolbar.removeAction(action)
            del action
            self.actions.pop(name)

        del self.toolbar

        # TODO (?) Delete all plugin dialogs?
        # del self.relate_calc_results_dlg


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def run_import_calc_result(self, checked=False, gml_fn=None):
        #print('run_import_calc_result()')
        #print(gml_fn)
        if self.dev:
            self.calc_result_file_dialog.setDirectory('/home/raymond/git/AERIUS-QGIS-plugins/demodata/')

        if gml_fn is None:
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

        qml = os.path.join(self.plugin_dir, 'styles', 'calc_result_abs.qml')
        receptors_layer.loadNamedStyle(qml)
        QgsProject.instance().addMapLayer(receptors_layer)

        if zoom:
            canvas = self.iface.mapCanvas()
            extent = receptors_layer.extent()
            extent.grow(100)
            canvas.setExtent(extent)


    def run_extract_gml_from_pdf(self):
        if self.dev:
            self.calc_result_file_dialog.setDirectory('/home/raymond/terglobo/projecten/aerius/202007_calc_input_plugin/demodata')
        pdf_fn, filter = self.calc_result_file_dialog.getOpenFileName(caption="Open IMAER PDF file", filter='*.pdf', parent=self.iface.mainWindow())
        self.log(f'run pdf: {pdf_fn}')

        if os.path.exists(os.path.dirname(pdf_fn)):
            gml_fn = pdf_fn.replace('.pdf', '.gml')
            task = ExtractGmlFromPdfTask(pdf_fn, gml_fn, self.extract_gml_from_pdf_callback)
            self.task_manager.addTask(task)
            self.log('added to task manager')


    def extract_gml_from_pdf_callback(self, fn):
        if fn is not None:
            msg = 'Extracted GML file saved as: <a href="{0}">{0}</a>'.format(fn)
            self.iface.messageBar().pushMessage('Success', msg, level=Qgis.Info, duration=10)
        else:
            msg = 'GML could not be extracted from PDF document.'
            self.iface.messageBar().pushMessage('Warning', msg, level=Qgis.Warning, duration=10)


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

        layer_imaer_version = metadata['imaer_version']

        task = ExportImaerCalculatorResultTask(receptor_layer, gml_fn, xml_lines, layer_imaer_version)
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


    def update_all_widgets(self):
        self.update_export_calc_widgets()
        self.update_connect_widgets()


    def update_export_calc_widgets(self):
        if self.iface.activeLayer() is not None:
            metadata = self.get_imaer_calc_metadata(self.iface.activeLayer())
            self.actions['export_calc_result'].setEnabled(metadata['is_imaer_calc_layer'])
        else:
            self.actions['export_calc_result'].setEnabled(False)


    def update_connect_widgets(self):
        conn_configured = self.aerius_connection.is_valid()
        self.actions['connect_receptorsets'].setEnabled(conn_configured)
        self.actions['connect_jobs'].setEnabled(conn_configured)


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
            self.update_connect_widgets()


    def open_connect_receptorsets(self):
        self.log('open_connect_receptorsets()')
        result = self.connect_receptorsets_dlg.exec_()
        print(result)


    def open_connect_jobs(self):
        self.log('open_connect_jobs()')
        result = self.connect_jobs_dlg.exec_()
        #print(result)


    def run_relate_calc_results(self):
        result = self.relate_calc_results_dlg.exec_()

        if not result == 1:
            return

        layers = self.relate_calc_results_dlg.get_layer_list()
        print(layers)

        calc_type = self.relate_calc_results_dlg.combo_calc_type.currentText()

        if calc_type == 'difference':
            self.relate_calc_results_dlg.calculate_difference(layers)

        if calc_type == 'sum':
            self.relate_calc_results_dlg.calculate_sum(layers)

        if calc_type == 'maximum':
            self.relate_calc_results_dlg.calculate_maximum(layers)


    def open_add_open_data(self):
        # TODO Move this to a QgsTask when specs are clear
        layer_ns = 'base_geometries'
        layer_name = 'hexagons'
        force_download = False # Option to enforce downloading for more dynamic data types

        base_fn = f'imaer_{layer_ns}_{layer_name}'
        zip_fn = os.path.join(self.download_dir, f'{base_fn}.zip')

        if not os.path.isfile(zip_fn) or force_download:
            # Download zip file
            conn = AeriusOpenData()
            print(conn)
            response = conn.get_dataset(layer_ns, layer_name, output_format='SHAPE-ZIP')

            if response is None:
                print('Download failed')
                return

            with open(zip_fn, 'wb') as zip_file:
                zip_file.write(response)

        download_layer = QgsVectorLayer(zip_fn, f'{layer_ns}:{layer_name}', 'ogr')

        qml = os.path.join(self.plugin_dir, 'styles', f'{layer_ns}_{layer_name}.qml')
        download_layer.loadNamedStyle(qml)
        QgsProject.instance().addMapLayer(download_layer)
