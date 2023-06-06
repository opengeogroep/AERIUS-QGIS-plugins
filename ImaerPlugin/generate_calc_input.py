# -*- coding: utf-8 -*-
import os
import time
import json

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import (
    QWidget,
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
    Srm2RoadSideBarrier,
    ADMSRoad,
    AdmsRoadSideBarrier,
    StandardVehicle,
    CustomVehicle
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
        self.emission_tabs['roads'] = getattr(self, 'tab_roads')
        self.emission_tabs['other'] = getattr(self, 'tab_emission_sources')
        self.emission_tabs['buildings'] = getattr(self, 'tab_buildings')
        self.emission_tabs['receptors'] = getattr(self, 'tab_receptors')

        self.init_gui()

    def init_gui(self):
        # Add message bar

        self.combo_layer_es.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.combo_layer_rd.setFilters(QgsMapLayerProxyModel.LineLayer)
        self.combo_layer_bld.setFilters(QgsMapLayerProxyModel.PolygonLayer | QgsMapLayerProxyModel.PointLayer)
        self.combo_layer_rec.setFilters(QgsMapLayerProxyModel.PointLayer)

        #self.combo_sector.currentIndexChanged.connect(self.update_emission_tab)
        self.checkBox_es.toggled.connect(self.update_emission_tab)
        self.checkBox_rd.toggled.connect(self.update_emission_tab)
        self.checkBox_bld.toggled.connect(self.update_emission_tab)
        self.checkBox_rec.toggled.connect(self.update_emission_tab)

        # self.combo_subsector.currentIndexChanged.connect(self.set_elements)
        self.edit_outfile.textChanged.connect(self.update_ok_button)

        self.combo_layer_es.layerChanged.connect(self.update_field_combos)
        self.combo_layer_rd.layerChanged.connect(self.update_field_combos)
        self.combo_layer_bld.layerChanged.connect(self.update_field_combos)
        self.combo_layer_rec.layerChanged.connect(self.update_field_combos)

        self.button_outfile.clicked.connect(self.browse_generate_calc_input_file)

        self.btn_save_settings.clicked.connect(self.save_settings)
        self.btn_load_settings.clicked.connect(self.load_settings)

        self.radio_veh_page_custom.page = self.page_veh_custom
        self.radio_veh_page_eft.page = self.page_veh_eft
        self.radio_veh_page_custom.toggled.connect(self.update_adms_vehicle_page)
        self.radio_veh_page_eft.toggled.connect(self.update_adms_vehicle_page)

        for fcb in self.findChildren(QgsFieldComboBox):
            fcb.setAllowEmptyFieldName(True)

        self.fcb_rd_v_custom_movements_units.addItems([''] + ui_settings['units_veh_movements'])
        self.fcb_rd_v_eft_units.addItems([''] + ui_settings['units_veh_movements'])

        # Make sure the corresponding vehicle page is displayed
        self.radio_veh_page_custom.setChecked(True)
        self.stack_rd_veh_adms.setCurrentWidget(self.radio_veh_page_custom.page)

        self.set_fixed_options()
        self.update_field_combos()
        self.update_ok_button()
        self.update_emission_tab()

    def __del__(self):
        self.edit_outfile.textChanged.disconnect(self.update_ok_button)
        self.combo_sector.currentIndexChanged.disconnect(self.update_emission_tab)
        self.combo_layer_es.layerChanged.disconnect(self.update_field_combos)
        self.combo_layer_rd.layerChanged.disconnect(self.update_field_combos)
        self.combo_layer_bld.layerChanged.disconnect(self.update_field_combos)
        self.combo_layer_rec.layerChanged.disconnect(self.update_field_combos)
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
        # country
        self.combo_country.addItem('', '')
        for country in ui_settings['countries']:
            self.combo_country.addItem(country, country)

        # crs
        self.combo_crs.addItem('', '')
        for crs in ui_settings['crs']:
            crs_name = f"{crs['name']} ({crs['srid']})"
            self.combo_crs.addItem(crs_name, crs['srid'])

        # sectors
        #self.combo_sector.addItem('<Select sector>', 0)
        #for sector in emission_sectors:
        #    sector_name = emission_sectors[sector]['tab_name']
        #    self.combo_sector.addItem(sector_name, sector)

        # year
        for item in ui_settings['project_years']:
            self.combo_project_year.addItem(str(item), item)
        year_index = self.combo_project_year.findData(ui_settings['project_default_year'])
        self.combo_project_year.setCurrentIndex(year_index)

        # situation
        self.edit_situation_name.setText(ui_settings['situation_name'])
        for item in ui_settings['situation_types_gml']:
            self.combo_situation_type.addItem(item, item)

    def update_emission_tab(self):
        country = self.plugin.settings.value('imaer_plugin/country', defaultValue='')
        country_index = self.combo_country.findData(country)
        self.combo_country.setCurrentIndex(country_index)

        crs_setting = self.plugin.settings.value('imaer_plugin/crs', defaultValue='')
        crs_index = self.combo_crs.findData(crs_setting)
        self.combo_crs.setCurrentIndex(crs_index)

        # Remove all tabs but 'Metadata'
        while self.tabs_mapping.count() > 1:
            self.tabs_mapping.removeTab(1)
        # Add selected emission tab
        '''
        sector = self.combo_sector.currentData()
        if sector in self.emission_tabs:
            sector_name = emission_sectors[sector]['tab_name']
            self.tabs_mapping.insertTab(1, self.emission_tabs[sector], sector_name)
            self.tabs_mapping.setCurrentIndex(1)
        '''
        n = 1
        if self.checkBox_es.isChecked():
            sector1 = 'other'
            sector_name = emission_sectors[sector1]['tab_name']
            self.tabs_mapping.insertTab(n, self.emission_tabs[sector1], sector_name)
            self.tabs_mapping.setCurrentIndex(n)
            n += 1
        else:
            sector1 = None

        if self.checkBox_rd.isChecked():
            sector2 = 'roads'
            sector_name = emission_sectors[sector2]['tab_name']
            self.tabs_mapping.insertTab(n, self.emission_tabs[sector2], sector_name)
            self.tabs_mapping.setCurrentIndex(n)
            n += 1
        else:
            sector2 = None

        if self.checkBox_bld.isChecked():
            sector3 = 'buildings'
            sector_name = emission_sectors[sector3]['tab_name']
            self.tabs_mapping.insertTab(n, self.emission_tabs[sector3], sector_name)
            self.tabs_mapping.setCurrentIndex(n)
            n += 1
        else:
            sector3 = None

        if self.checkBox_rec.isChecked():
            sector4 = 'receptors'
            sector_name = emission_sectors[sector4]['tab_name']
            self.tabs_mapping.insertTab(n, self.emission_tabs[sector4], sector_name)
            self.tabs_mapping.setCurrentIndex(n)
            n += 1
        else:
            sector4 = None

        # Enable/disable widgets per country
        if country == '' or crs_setting == '':
            return
            # TODO: Raise error

        for sector in [sector1, sector2, sector3, sector4]:
            if sector is None:
                pass
            if sector in emission_sectors and 'ui_settings' in emission_sectors[sector]:
                # Running this loop twice because looping all objects of the QWidget
                # class resulted in a frozen dialog.
                for widget in self.findChildren(QgsFieldComboBox):
                    if widget.objectName() in emission_sectors[sector]['ui_settings'][country]['disable_widgets']:
                        widget.setVisible(False)
                    else:
                        widget.setVisible(True)
                for widget in self.findChildren(QLabel):
                    if widget.objectName() in emission_sectors[sector]['ui_settings'][country]['disable_widgets']:
                        widget.setVisible(False)
                    else:
                        widget.setVisible(True)
                if 'emission_tab' in emission_sectors[sector]:
                    vehicle_page = emission_sectors[sector]['ui_settings'][country]['vehicle_page']
                    # print(vehicle_page)
                    stack = getattr(self, 'stack_rd_veh')
                    page = getattr(self, vehicle_page)
                    stack.setCurrentWidget(page)

    def update_field_combos(self):
        for fcb in self.findChildren(QgsFieldComboBox):
            if 'es' in fcb.objectName():
                fcb.setLayer(self.combo_layer_es.currentLayer())
            if '_rd' in fcb.objectName():
                fcb.setLayer(self.combo_layer_rd.currentLayer())
            if '_bld' in fcb.objectName():
                fcb.setLayer(self.combo_layer_bld.currentLayer())
            if '_rec' in fcb.objectName():
                fcb.setLayer(self.combo_layer_rec.currentLayer())
            if '_em_' in fcb.objectName():
                fcb.setLayer(self.combo_layer_es.currentLayer())
        print(self.combo_layer_bld.currentLayer().geometryType())
        # if bld is a point layer then show the diameter field
        if self.combo_layer_bld.currentLayer().geometryType() != 0:
            self.fcb_bld_diameter.setVisible(False)
            self.label_bld_diameter.setVisible(False)
        else:
            self.fcb_bld_diameter.setVisible(True)
            self.label_bld_diameter.setVisible(True)

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

    def update_adms_vehicle_page(self):
        self.stack_rd_veh_adms.setCurrentWidget(self.sender().page)

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

        country = self.combo_country.currentData()
        crs_dest_srid = self.combo_crs.currentData()
        # print(crs_dest_srid)
        crs_dest = QgsCoordinateReferenceSystem(crs_dest_srid)

        crs_transform_list = []
        if self.checkBox_es.isChecked():
            input_layer_es = self.combo_layer_es.currentLayer()
            crs_source = input_layer_es.crs()
            if crs_source == crs_dest:
                crs_transform = None
            else:
                crs_transform = QgsCoordinateTransform(crs_source, crs_dest, QgsProject.instance())
            crs_transform_list.append(crs_transform)
        if self.checkBox_rd.isChecked():
            input_layer_rd = self.combo_layer_rd.currentLayer()
            crs_source = input_layer_rd.crs()
            if crs_source == crs_dest:
                crs_transform = None
            else:
                crs_transform = QgsCoordinateTransform(crs_source, crs_dest, QgsProject.instance())
                crs_transform_list.append(crs_transform)
        if self.checkBox_bld.isChecked():
            input_layer_bld = self.combo_layer_bld.currentLayer()
            crs_source = input_layer_bld.crs()
            if crs_source == crs_dest:
                crs_transform = None
            else:
                crs_transform = QgsCoordinateTransform(crs_source, crs_dest, QgsProject.instance())
                crs_transform_list.append(crs_transform)
        if self.checkBox_rec.isChecked():
            input_layer_rec = self.combo_layer_rec.currentLayer()
            crs_source = input_layer_rec.crs()
            if crs_source == crs_dest:
                crs_transform = None
            else:
                crs_transform = QgsCoordinateTransform(crs_source, crs_dest, QgsProject.instance())
                crs_transform_list.append(crs_transform)

        # remove any None values from the crs_transform_list
        crs_transform_list = [x for x in crs_transform_list if x is not None]
        # keep only unique values in the crs_transform_list
        crs_transform_list = list(set(crs_transform_list))
        # if length of the list is more than one raise error
        print(crs_transform_list)
        if len(crs_transform_list) == 0:
            pass # no crs transformation needed
        elif len(crs_transform_list) == 1:
            crs_transform = crs_transform_list[0] # only single crs transformation needed
        else:
            raise Exception('Different crs provided for input layers selected')

        # Loop all features
        list_input_layers_to_process = []
        if self.checkBox_es.isChecked():
            list_input_layers_to_process.append(input_layer_es)
        if self.checkBox_rd.isChecked():
            list_input_layers_to_process.append(input_layer_rd)
        if self.checkBox_bld.isChecked():
            list_input_layers_to_process.append(input_layer_bld)
        if self.checkBox_rec.isChecked():
            list_input_layers_to_process.append(input_layer_rec)

        #for input_layer in [input_layer_es, input_layer_rd, input_layer_bld, input_layer_rec]:
        for input_layer in list_input_layers_to_process:
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

                # if it is the emissions source layer, process this
                if self.checkBox_es.isChecked() and input_layer == input_layer_es:
                    es = self.get_emission_source_from_gui(feat, geom, crs_dest_srid, local_id)

                # if it is the road layer process as such
                if self.checkBox_rd.isChecked() and input_layer == input_layer_rd:
                    if country == 'NL':
                        es = self.get_srm2_road_from_gui(feat, geom, crs_dest_srid, local_id)
                    elif country == 'UK':
                        es = self.get_adms_road_from_gui(feat, geom, crs_dest_srid, local_id)
                    else:
                        print('This should never happen. (No country selected.)')

                # if it is a building layer
                if self.checkBox_bld.isChecked() and input_layer == input_layer_bld:
                    raise Exception('Not implemented yet')

                # if it is a receptor layer
                if self.checkBox_rec.isChecked() and input_layer == input_layer_rec:
                    raise Exception('Not implemented yet')

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
            prim_bld = self.get_feature_value(self.fcb_es_prim_bld, feat)

            hc_value = self.get_feature_value(self.fcb_es_hc_value, feat)
            if hc_value is not None:
                hc = SpecifiedHeatContent(value=hc_value)
            else:
                hc = None
            if prim_bld is None:
                es.emission_source_characteristics = EmissionSourceCharacteristics(
                    emission_height=esc_height,
                    spread=esc_spread,
                    heat_content=hc,
                )
            else:
               es.emission_source_characteristics = EmissionSourceCharacteristics(
                    building = prim_bld,
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
                rsb = Srm2RoadSideBarrier(b_type, b_height, b_distance)
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

    # ADMSRoad
    def get_adms_road_from_gui(self, feat, geom, epsg_id, local_id):
        sector_id = 3100  # This is the only option in NL
        # sector_id = self.get_feature_value(self.fcb_rd_sector_id, feat)
        label = self.get_feature_value(self.fcb_rd_label, feat)

        road_area_type = self.get_feature_value(self.fcb_rd_area_type, feat)
        road_type = self.get_feature_value(self.fcb_rd_type, feat)

        es = ADMSRoad(
            local_id=local_id,
            sector_id=sector_id,
            label=label,
            geom=geom,
            epsg_id=epsg_id,
            road_area_type=road_area_type,
            road_type=road_type)

        es.description = self.get_feature_value(self.fcb_rd_description, feat)

        es.width = self.get_feature_value(self.fcb_rd_width, feat)
        es.elevation = self.get_feature_value(self.fcb_rd_elevation, feat)
        es.gradient = self.get_feature_value(self.fcb_rd_gradient, feat)
        es.coverage = self.get_feature_value(self.fcb_rd_coverage, feat)
        es.tunnel_factor = self.get_feature_value(self.fcb_rd_tunnel_factor, feat)
        es.elevation_height = self.get_feature_value(self.fcb_rd_elevation_height, feat)

        # barriers
        for side in ['left', 'right']:
            fcb = getattr(self, f'fcb_rd_b_{side}_type')
            b_type = self.get_feature_value(fcb, feat)
            fcb = getattr(self, f'fcb_rd_b_{side}_height_av')
            b_height_av = self.get_feature_value(fcb, feat)
            fcb = getattr(self, f'fcb_rd_b_{side}_height_max')
            b_height_max = self.get_feature_value(fcb, feat)
            fcb = getattr(self, f'fcb_rd_b_{side}_height_min')
            b_height_min = self.get_feature_value(fcb, feat)
            fcb = getattr(self, f'fcb_rd_b_{side}_distance')
            b_distance = self.get_feature_value(fcb, feat)
            fcb = getattr(self, f'fcb_rd_b_{side}_porosity')
            b_porosity = self.get_feature_value(fcb, feat)

            if not (b_type is None):
                rsb = AdmsRoadSideBarrier(
                    b_type, b_distance, b_height_av,
                    b_height_max, b_height_min, b_porosity
                )
                if side == 'left':
                    es.barrier_left = rsb
                else:
                    es.barrier_right = rsb

        # vehicles
        vehicles = []

        if self.radio_veh_page_eft.isChecked():
            fcb = getattr(self, f'fcb_rd_v_eft_link_speed')
            link_speed = self.get_feature_value(fcb, feat)
            link_speed = int(link_speed)

            vehicle_types = {
                'car': 'Car',
                'taxi': 'Tax',
                'motor': 'Mot',
                'lgv': 'LGV',
                'hgv': 'HGV',
                'bus': 'Bus'
            }

            # get the time unit from the gui
            time_unit_ui = self.fcb_rd_v_eft_units.currentText()

            if time_unit_ui == 'p/hour':
                time_unit = 'HOUR'
            elif time_unit_ui == 'p/24 hour':
                time_unit = 'DAY'
            elif time_unit_ui == 'p/month':
                time_unit = 'MONTH'
            elif time_unit_ui == 'p/year':
                time_unit = 'YEAR'

            for veh_type_key, veh_type_name in vehicle_types.items():
                fcb = getattr(self, f'fcb_rd_v_eft_n_{veh_type_key}')
                veh_number = self.get_feature_value(fcb, feat)

                if not (veh_number is None):
                    vehicle = StandardVehicle(
                        vehicles_per_time_unit=veh_number,
                        time_unit=time_unit,
                        stagnation_factor=0.0,
                        vehicle_type=veh_type_name,
                        maximum_speed=link_speed,
                        strict_enforcement='false'
                    )
                    vehicles.append(vehicle)

        # Custom vehicles
        if self.radio_veh_page_custom.isChecked():
            description = self.get_feature_value(self.fcb_rd_v_custom_description, feat)
            movements = self.get_feature_value(self.fcb_rd_v_custom_movements, feat)
            em_nox = self.get_feature_value(self.fcb_rd_v_custom_em_nox, feat)
            em_nh3 = self.get_feature_value(self.fcb_rd_v_custom_em_nh3, feat)

            # get the time unit from the gui
            time_unit_ui = self.fcb_rd_v_custom_movements_units.currentText()

            if time_unit_ui == 'p/hour':
                time_unit = 'HOUR'
            elif time_unit_ui == 'p/24 hour':
                time_unit = 'DAY'
            elif time_unit_ui == 'p/month':
                time_unit = 'MONTH'
            elif time_unit_ui == 'p/year':
                time_unit = 'YEAR'

            emission = []
            if em_nox is not None:
                emission.append(Emission('NOX', em_nox))
            if em_nh3 is not None:
                emission.append(Emission('NH3', em_nh3))

            veh = CustomVehicle(
                vehicles_per_time_unit=movements,
                time_unit=time_unit,
                description=description,
                emission=emission
            )
            vehicles.append(veh)

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
        print(work_dir)
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
        layer_fields_es = self.combo_layer_es.currentLayer().fields().names()
        layer_fields_rd = self.combo_layer_rd.currentLayer().fields().names()
        layer_fields_bld = self.combo_layer_bld.currentLayer().fields().names()
        layer_fields_rec = self.combo_layer_rec.currentLayer().fields().names()
        for fcb in self.findChildren(QgsFieldComboBox):
            widget_name = fcb.objectName()
            if widget_name not in field_cfg:
                continue
            new_field = field_cfg[widget_name]
            if new_field == '':
                fcb.setCurrentIndex(0)
                continue
            if new_field in layer_fields_es or new_field in layer_fields_rd or new_field in layer_fields_bld or new_field in layer_fields_rec:
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
