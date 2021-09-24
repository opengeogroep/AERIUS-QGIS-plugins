# -*- coding: utf-8 -*-
import os
import time
import json

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QHBoxLayout
)
from qgis.PyQt import uic

from qgis.utils import iface
from qgis.gui import (
    QgsMapLayerComboBox,
    QgsFieldComboBox
)
from qgis.core import (
    QgsMapLayerProxyModel,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform
)

from ImaerPlugin.config import (
    emission_sectors,
    emission_elements,
    ui_settings
)

from ImaerPlugin.imaer4 import (
    ImaerDocument,
    AeriusCalculatorMetadata,
    EmissionSourceType,
    EmissionSourceCharacteristics,
    EmissionSource,
    SpecifiedHeatContent,
    Emission
)

#from .imaer4.imaer_document import ImaerDocument


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'generate_calc_input_dlg.ui'))




class GenerateCalcInputDialog(QDialog, FORM_CLASS):
    def __init__(self, plugin, parent=None):
        """Constructor."""
        super(GenerateCalcInputDialog, self).__init__(parent)

        self.setupUi(self)
        self.iface = iface
        self.plugin = plugin

        self.emission_tabs = {}
        self.emission_tabs['ROAD_TRANSPORTATION'] = self.tab_road_transportation
        self.emission_tabs['OTHER'] = self.tab_emission_sources

        self.init_gui()


    def init_gui(self):
        self.combo_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.combo_sector.currentIndexChanged.connect(self.set_emission_tab)
        ##self.combo_subsector.currentIndexChanged.connect(self.set_elements)
        self.edit_outfile.textChanged.connect(self.update_ok_button)

        self.combo_layer.layerChanged.connect(self.update_field_combos)
        self.button_outfile.clicked.connect(self.browse_generate_calc_input_file)

        self.btn_save_settings.clicked.connect(self.save_settings)
        self.btn_load_settings.clicked.connect(self.load_settings)

        for fcb in self.findChildren(QgsFieldComboBox):
            fcb.setAllowEmptyFieldName(True)

        self.set_fixed_options()
        self.update_field_combos()
        self.update_ok_button()
        self.set_emission_tab()


    def __del__(self):
        self.edit_outfile.textChanged.disconnect(self.update_ok_button)
        self.combo_sector.currentIndexChanged.disconnect(self.set_emission_tab)
        self.combo_layer.layerChanged.disconnect(self.update_field_combos)
        self.button_outfile.clicked.disconnect(self.browse_generate_calc_input_file)

        self.btn_save_settings.clicked.disconnect(self.save_settings)
        self.btn_load_settings.clicked.disconnect(self.load_settings)


    def browse_generate_calc_input_file(self):
        if self.plugin.dev:
            out_path = '/home/raymond/terglobo/projecten/aerius/202007_calc_input_plugin/demodata/gen_calc_input'
        else:
            out_path = ''
        out_fn = time.strftime("calcinput_%Y%m%d_%H%M%S.gml")
        out_fn = os.path.join(out_path, out_fn)

        gml_outfn, filter = self.plugin.calc_input_file_dialog.getSaveFileName(caption="Save as Calculator input gml file", filter='*.gml', directory=out_fn, parent=self.iface.mainWindow())
        self.edit_outfile.setText(gml_outfn)


    def set_fixed_options(self):
        # crs
        for crs in ui_settings['crs']:
            self.combo_crs.addItem(crs['name'], crs['srid'])

        # sectors
        self.combo_sector.addItem('<Select sector>', 0)
        for sector_name in emission_sectors:
            ##print(sector_name)
            self.combo_sector.addItem(sector_name)

        # project
        for item in ui_settings['project_years']:
            self.combo_project_year.addItem(item, item)
        self.combo_project_year.setCurrentIndex(self.combo_project_year.count() - 1)

        # situation
        self.edit_situation_name.setText(ui_settings['situation_name'])
        for item in ui_settings['situation_types']:
            self.combo_situation_type.addItem(item, item)


    def set_emission_tab(self):
        # Remove all tabs but 'Metadata'
        while self.tabWidget.count() > 1:
            self.tabWidget.removeTab(1)
        # Add selected emission tab
        sector = self.combo_sector.currentText()
        if sector in self.emission_tabs:
            self.tabWidget.insertTab(1, self.emission_tabs[sector], sector)
            self.tabWidget.setCurrentIndex(1)


    def update_field_combos(self):
        for fcb in self.findChildren(QgsFieldComboBox):
            fcb.setLayer(self.combo_layer.currentLayer())


    def update_ok_button(self):
        if self.edit_outfile.text() == '':
            self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
            return
        ##if self.get_current_sector_id() == 0:
        ##    self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
        ##    return
        self.buttonBox.button(QDialogButtonBox.Save).setEnabled(True)


    def get_imaer_doc_from_gui(self):
        '''Maps items from GUI widgets to IMAER object'''

        imaer_doc = ImaerDocument()

        year = self.combo_project_year.currentData()
        description = self.edit_project_description.toPlainText()

        if self.group_situation.isChecked():
             situation_name = self.edit_situation_name.text()
             situation_reference = self.edit_situation_reference.text()
             situation_type = self.combo_situation_type.currentText()
             situation = {'name': situation_name, 'reference': situation_reference, 'type': situation_type}
        else:
            situation = None

        metadata = AeriusCalculatorMetadata(
            project = {'year': year, 'description': description},
            situation = situation,
        )

        imaer_doc.metadata = metadata

        input_layer = self.combo_layer.currentLayer()
        crs_source = input_layer.crs()
        crs_dest_srid = self.combo_crs.currentData()
        crs_dest = QgsCoordinateReferenceSystem(crs_dest_srid)
        if crs_source == crs_dest:
            crs_transform = None
        else:
            crs_transform = QgsCoordinateTransform(crs_source, crs_dest, QgsProject.instance())

        for feat in input_layer.getFeatures():
            local_id = 'ES.{}'.format(feat.id())

            sector_id = self.get_feature_value(self.fcb_es_sector_id, feat)
            label = self.get_feature_value(self.fcb_es_label, feat)
            description = self.get_feature_value(self.fcb_es_description, feat)

            # geometry
            geom = feat.geometry()
            if crs_transform is not None:
                geom.transform(crs_transform)

            es = EmissionSource(local_id=local_id, sector_id=sector_id, label=label, geom=geom)
            print('1:', type(es), es.emissions, es.description)

            es.description = description

            # emission source characteristics
            if self.groupBox_es_characteristics.isChecked():
                esc_height = self.get_feature_value(self.fcb_es_emission_height, feat)
                esc_spread = self.get_feature_value(self.fcb_es_spread, feat)

                hc_value = self.get_feature_value(self.fcb_es_hc_value, feat)
                if hc_value is not None:
                    hc = SpecifiedHeatContent(value=hc_value)
                else:
                    hc = None

                es.emission_source_characteristics = EmissionSourceCharacteristics(
                    emission_height=esc_height,
                    spread=esc_spread,
                    heat_content=hc,
                )

            '''if hc is not None and esc_height is not None:
                    esc = EmissionSourceCharacteristics(hc, esc_height)

                    esc_bld_height = self.get_widget_value('esc_bld_height', feat, 'float')
                    esc_bld_width = self.get_widget_value('esc_bld_width', feat, 'float')
                    esc_bld_length = self.get_widget_value('esc_bld_length', feat, 'float')
                    esc_bld_orientation = self.get_widget_value('esc_bld_orientation', feat, 'float')
                    if esc_bld_height is not None:
                        bld = Building(esc_bld_height, esc_bld_width, esc_bld_length, esc_bld_orientation)
                        esc.building = bld

                    es.es_characteristics = esc'''

            # emissions
            es.emissions = [] # TODO: Figure out why and fix this! (Without setting this clean list, emissions from former features are present.)
            em = self.get_feature_value(self.fcb_em_nox, feat)
            if em is not None:
                es.emissions.append(Emission('NOX', em))
            em = self.get_feature_value(self.fcb_em_nh3, feat)
            if em is not None:
                es.emissions.append(Emission('NH3', em))

            imaer_doc.feature_members.append(es)

        return imaer_doc


    def get_feature_value(self, widget, feat, cast_to=None):
        if not isinstance(widget, QgsFieldComboBox):
            return None
        field_name = widget.currentField()
        if field_name == '':
            return None
            #return widget_set['fixed'].text() TODO: return fixed value after data type check (or something..)
        else:
            value = feat[field_name]

        if isinstance(value, QVariant) and str(value) == 'NULL':
            return None

        if cast_to is not None:
            #if cast_to == 'double':
            #    return result.toDouble()
            if cast_to == 'float':
                if isinstance(result, float):
                    return
                if isInstance(result, QVariant):
                    result.toFloat()
            elif cast_to == 'integer':
                return result.toInt()
            elif cast_to == 'string':
                return result.toString()
        return value


    def save_settings(self):
        work_dir = self.plugin.settings.value('imaer_plugin/work_dir', defaultValue=None)
        if work_dir is None:
            raise Exception('Work dir not set')
            return
        # TODO: choose file name
        base_name = 'generate_gml_config.json'
        out_fn = os.path.join(work_dir, base_name)
        print(out_fn)
        field_dict = self.collect_field_settings()
        txt = json.dumps(field_dict, indent=4)
        with open(out_fn, 'w') as out_file:
            out_file.write(txt)


    def collect_field_settings(self):
        '''Collects a dictionary with all widget_names and field_names for all QgsFieldComboBoxes'''
        result = {}
        result['imaer_plugin_version'] = 1
        result['fields'] = {}
        for fcb in self.findChildren(QgsFieldComboBox):
            k = fcb.objectName()
            v = fcb.currentText()
            result['fields'][k] = v
        return result


    def load_settings(self):
        work_dir = self.plugin.settings.value('imaer_plugin/work_dir', defaultValue=None)
        if work_dir is None:
            raise Exception('Work dir not set')
            return
        # TODO: choose file name
        base_name = 'generate_gml_config.json'
        out_fn = os.path.join(work_dir, base_name)
        print(out_fn)

        with open(out_fn, 'r') as out_file:
            txt = out_file.read()

        field_dict = json.loads(txt)

        if not 'imaer_plugin_version' in field_dict:
            print('This is not a valid field configuration file')
            return

        self.set_field_settings(field_dict['fields'])


    def set_field_settings(self, field_cfg):
        '''Sets texts from a dictionary with all widget_names and field_names for all QgsFieldComboBoxes'''
        layer_fields = self.combo_layer.currentLayer().fields().names()
        for fcb in self.findChildren(QgsFieldComboBox):
            widget_name = fcb.objectName()
            if not widget_name in field_cfg:
                continue
            new_field = field_cfg[widget_name]
            if new_field == '':
                fcb.setCurrentIndex(0)
                continue
            if new_field in layer_fields:
                fcb.setCurrentText(new_field)
            else:
                # Set empty
                fcb.setCurrentIndex(0)
                print(f'Current input layer does not contain a field \'{new_field}\'')
