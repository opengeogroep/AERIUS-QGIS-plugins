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
    QHBoxLayout,
    QSizePolicy
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
    ui_settings
)

from ImaerPlugin.imaer5 import (
    ImaerDocument,
    AeriusCalculatorMetadata,
    EmissionSourceType,
    EmissionSourceCharacteristics,
    EmissionSource,
    SpecifiedHeatContent,
    Emission,
    SRM2Road,
    RoadSideBarrier,
    StandardVehicle
)

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
        # Add message bar

        self.combo_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.combo_sector.currentIndexChanged.connect(self.set_emission_tab)
        # self.combo_subsector.currentIndexChanged.connect(self.set_elements)
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
        # IMAER versions
        self.combo_imaer_v.addItems(ui_settings['imaer_versions'])
        # Select last item (= most recent version) by default
        self.combo_imaer_v.setCurrentIndex(self.combo_imaer_v.count() - 1)

        # crs
        for crs in ui_settings['crs']:
            crs_name = f"{crs['name']} ({crs['srid']})"
            self.combo_crs.addItem(crs_name, crs['srid'])
        crs_setting = self.plugin.settings.value('imaer_plugin/crs', defaultValue='')
        crs_index = self.combo_crs.findData(crs_setting)
        self.combo_crs.setCurrentIndex(crs_index)

        # sectors
        self.combo_sector.addItem('<Select sector>', 0)
        for sector_name in emission_sectors:
            # print(sector_name)
            self.combo_sector.addItem(sector_name)

        # year
        for item in ui_settings['project_years']:
            self.combo_project_year.addItem(str(item), item)
        year_index = self.combo_project_year.findData(ui_settings['project_default_year'])
        self.combo_project_year.setCurrentIndex(year_index)

        # situation
        self.edit_situation_name.setText(ui_settings['situation_name'])
        for item in ui_settings['situation_types_gml']:
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
        '''
        if self.get_current_sector_id() == 0:
            self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
            return
        '''
        self.buttonBox.button(QDialogButtonBox.Save).setEnabled(True)

    def get_imaer_doc_from_gui(self):
        '''Maps items from GUI widgets to IMAER object'''

        imaer_doc = ImaerDocument()

        year = self.combo_project_year.currentData()
        description = self.edit_project_description.toPlainText()

        if self.group_situation.isChecked():
            situation_name = self.edit_situation_name.text()
            situation_type = self.combo_situation_type.currentText()
            situation = {'name': situation_name, 'type': situation_type}
        else:
            situation = None

        metadata = AeriusCalculatorMetadata(
            project={'year': year, 'description': description},
            situation=situation,
        )

        imaer_doc.metadata = metadata

        input_layer = self.combo_layer.currentLayer()
        crs_source = input_layer.crs()
        crs_dest_srid = self.combo_crs.currentData()
        print(crs_dest_srid)
        crs_dest = QgsCoordinateReferenceSystem(crs_dest_srid)
        if crs_source == crs_dest:
            crs_transform = None
        else:
            crs_transform = QgsCoordinateTransform(crs_source, crs_dest, QgsProject.instance())

        # Loop all features
        for feat in input_layer.getFeatures():
            local_id = 'ES.{}'.format(feat.id())

            # geometry
            geom = feat.geometry()

            geom2 = self.make_single_part(geom)
            if geom2 is None:
                self.plugin.log(f'Input data contains multipart geometry: {geom.asWkt(precision=3)}', bar=True, lvl='Critical')
                return
            geom = geom2

            # TODO: Check for invalid geometries

            if crs_transform is not None:
                geom.transform(crs_transform)

            sector_name = self.combo_sector.currentText()
            if sector_name == 'OTHER':
                es = self.get_emission_source_from_gui(feat, geom, crs_dest_srid, local_id)
            elif sector_name == 'ROAD_TRANSPORTATION':
                es = self.get_srm2_road_from_gui(feat, geom, crs_dest_srid, local_id)
            else:
                raise Exception('Invalid sector')

            imaer_doc.feature_members.append(es)
            # self.plugin.tempes = es # For debugging

        return imaer_doc

    # Emission Source
    def get_emission_source_from_gui(self, feat, geom, epsg_id, local_id):
        sector_id = self.get_feature_value(self.fcb_es_sector_id, feat)
        label = self.get_feature_value(self.fcb_es_label, feat)
        description = self.get_feature_value(self.fcb_es_description, feat)

        es = EmissionSource(local_id=local_id, sector_id=sector_id, label=label, geom=geom, epsg_id=epsg_id)
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

        # emissions
        es.emissions = []  # TODO: Figure out why and fix this! (Without setting this clean list, emissions from former features are present.)
        em = self.get_feature_value(self.fcb_em_nox, feat)
        if em is not None:
            es.emissions.append(Emission('NOX', em))
        em = self.get_feature_value(self.fcb_em_nh3, feat)
        if em is not None:
            es.emissions.append(Emission('NH3', em))

        return es

    # SRM2Road
    def get_srm2_road_from_gui(self, feat, geom, epsg_id, local_id):
        sector_id = 3100  # This is the only option in NL
        # sector_id = self.get_feature_value(self.fcb_rd_sector_id, feat)
        label = self.get_feature_value(self.fcb_rd_label, feat)

        road_area_type = 'NL'  # This is the only option in NL
        # road_area_type = self.get_feature_value(self.fcb_rd_area_type, feat)
        road_type = self.get_feature_value(self.fcb_rd_type, feat)

        es = SRM2Road(
            local_id=local_id,
            sector_id=sector_id,
            label=label,
            geom=geom,
            epsg_id=epsg_id,
            road_area_type=road_area_type,
            road_type=road_type)

        es.description = self.get_feature_value(self.fcb_rd_description, feat)

        es.tunnel_factor = self.get_feature_value(self.fcb_rd_tunnel_factor, feat)
        es.elevation = self.get_feature_value(self.fcb_rd_elevation, feat)
        es.elevation_height = self.get_feature_value(self.fcb_rd_elevation_height, feat)

        # barriers
        for side in ['left', 'right']:
            fcb = getattr(self, f'fcb_rd_b_{side}_type')
            b_type = self.get_feature_value(fcb, feat)
            fcb = getattr(self, f'fcb_rd_b_{side}_height')
            b_height = self.get_feature_value(fcb, feat)
            fcb = getattr(self, f'fcb_rd_b_{side}_distance')
            b_distance = self.get_feature_value(fcb, feat)

            if not (b_type is None and b_height is None and b_distance is None):
                rsb = RoadSideBarrier(b_type, b_height, b_distance)
                if side == 'left':
                    es.barrier_left = rsb
                else:
                    es.barrier_right = rsb

        # vehicles
        vehicles = []
        vehicle_types = {
            'lt1': 'LIGHT_TRAFFIC',
            'lt2': 'LIGHT_TRAFFIC',
            'nf': 'NORMAL_FREIGHT',
            'hf': 'HEAVY_FREIGHT',
            'ab': 'AUTO_BUS'
        }
        for veh_type_key, veh_type_name in vehicle_types.items():

            fcb = getattr(self, f'fcb_rd_v_{veh_type_key}_vehicles_per_time')
            veh_number = self.get_feature_value(fcb, feat)
            fcb = getattr(self, f'fcb_rd_v_{veh_type_key}_stagnation')
            veh_stagnation = self.get_feature_value(fcb, feat)
            fcb = getattr(self, f'fcb_rd_v_{veh_type_key}_maxspeed')
            veh_speed = self.get_feature_value(fcb, feat)
            fcb = getattr(self, f'fcb_rd_v_{veh_type_key}_strict')
            veh_strict = self.get_feature_value(fcb, feat)

            if not (veh_number is None and veh_stagnation is None):
                vehicle = StandardVehicle(
                    vehicles_per_time_unit=veh_number,
                    time_unit='DAY',
                    stagnation_factor=veh_stagnation,
                    vehicle_type=veh_type_name,
                    maximum_speed=veh_speed,
                    strict_enforcement=veh_strict
                )
                vehicles.append(vehicle)

            es.vehicles = vehicles

        return es

    def get_feature_value(self, widget, feat, cast_to=None):
        if not isinstance(widget, QgsFieldComboBox):
            return None
        field_name = widget.currentField()
        if field_name == '':
            return None
            # return widget_set['fixed'].text() TODO: return fixed value after data type check (or something..)
        else:
            value = feat[field_name]

        if isinstance(value, QVariant) and str(value) == 'NULL':
            return None

        if cast_to is not None:
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
        # print(out_fn)
        field_dict = self.collect_field_settings()
        txt = json.dumps(field_dict, indent=4)
        with open(out_fn, 'w') as out_file:
            out_file.write(txt)

    def load_settings(self):
        work_dir = self.plugin.settings.value('imaer_plugin/work_dir', defaultValue=None)
        if work_dir is None:
            raise Exception('Work dir not set')
            return
        # TODO: choose file name
        base_name = 'generate_gml_config.json'
        out_fn = os.path.join(work_dir, base_name)
        # print(out_fn)

        with open(out_fn, 'r') as out_file:
            txt = out_file.read()

        field_dict = json.loads(txt)

        if 'imaer_plugin_version' not in field_dict:
            self.plugin.log('This is not a valid field configuration file', lvl='Warning', bar=True)
            return

        self.set_field_settings(field_dict['fields'])
        self.plugin.log('Configuration file loaded', bar=True)

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

    def set_field_settings(self, field_cfg):
        '''Sets texts from a dictionary with all widget_names and field_names for all QgsFieldComboBoxes'''
        layer_fields = self.combo_layer.currentLayer().fields().names()
        for fcb in self.findChildren(QgsFieldComboBox):
            widget_name = fcb.objectName()
            if widget_name not in field_cfg:
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
                # print(f'Current input layer does not contain a field \'{new_field}\'')

    def make_single_part(self, geom):
        '''Returns single part geometry or None if input has more than 1 part'''
        parts = geom.asGeometryCollection()
        if len(parts) == 1:
            result = parts[0]
            # Make sure the type is Point, LineString or Polygon
            if result.wkbType() in [1, 2, 3]:
                return result
        return None
