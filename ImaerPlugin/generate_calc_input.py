# -*- coding: utf-8 -*-
import os
import time

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
    QgsCoordinateTransform)

from ImaerPlugin.config import (
    emission_sectors,
    emission_elements,
    ui_settings
)

from ImaerPlugin.widget_registry import WidgetRegistry

from ImaerPlugin.imaer2 import (
    FeatureCollectionCalculator,
    AeriusCalculatorMetadata,
    EmissionSource,
    EmissionSourceCharacteristics,
    SpecifiedHeatContent,
    CalculatedHeatContent,
    Building
)

from ImaerPlugin.imaer4 import ImaerDocument


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'generate_calc_input_dlg.ui'))




class GenerateCalcInputDialog(QDialog, FORM_CLASS):
    def __init__(self, plugin, parent=None):
        """Constructor."""
        super(GenerateCalcInputDialog, self).__init__(parent)

        self.setupUi(self)
        self.iface = iface
        self.plugin = plugin
        self.widget_registry = WidgetRegistry(self)
        self.sector_id = 0

        self.emission_tabs = {}
        self.emission_tabs['ROAD_TRANSPORTATION'] = self.tab_road_transportation
        self.emission_tabs['OTHER'] = self.tab_emission_sources

        self.init_gui()


    def init_gui(self):
        self.combo_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.combo_sector.currentIndexChanged.connect(self.set_subsectors)
        #self.combo_subsector.currentIndexChanged.connect(self.set_elements)
        self.edit_outfile.textChanged.connect(self.update_ok_button)
        self.set_fixed_options()
        self.update_ok_button()

        self.combo_layer.layerChanged.connect(self.update_field_combos)
        self.button_outfile.clicked.connect(self.browse_generate_calc_input_file)

        for fcb in self.findChildren(QgsFieldComboBox):
            fcb.setAllowEmptyFieldName(True)

        self.set_emission_tab()
        self.update_field_combos()


    def __del__(self):
        self.edit_outfile.textChanged.disconnect(self.update_ok_button)
        self.combo_sector.currentIndexChanged.disconnect(self.set_subsectors)
        #self.combo_subsector.currentIndexChanged.disconnect(self.set_elements)
        self.combo_layer.layerChanged.disconnect(self.update_field_combos)



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
            print(sector_name)
            self.combo_sector.addItem(sector_name)

        # project
        for item in ui_settings['project_years']:
            self.combo_project_year.addItem(item, item)
        self.combo_project_year.setCurrentIndex(self.combo_project_year.count() - 1)

        # situation
        self.edit_situation_name.setText(ui_settings['situation_name'])
        for item in ui_settings['situation_types']:
            self.combo_situation_type.addItem(item, item)

        # calculation
        for item in ui_settings['calculation_types']:
            self.combo_calculation_type.addItem(item, item)
        for item in ui_settings['calculation_result_types']:
            self.combo_calculation_result_type.addItem(item, item)


    def set_subsectors(self):
        sector = self.combo_sector.currentText()
        has_subsectors = sector in emission_sectors and 'subsectors' in emission_sectors[sector]
        self.combo_subsector.clear()
        self.label_subsector.setEnabled(has_subsectors)
        self.combo_subsector.setEnabled(has_subsectors)
        if has_subsectors:
            self.combo_subsector.addItem('<Select specific sector>', 0)
            for key, value in emission_sectors[sector]['subsectors'].items():
                self.combo_subsector.addItem(key, value['sector_id'])
        self.set_emission_tab()


    def set_emission_tab(self):
        # Remove all tabs but 'Metadata'
        while self.tabWidget.count() > 1:
            self.tabWidget.removeTab(1)
        # Add selected emission tab
        sector = self.combo_sector.currentText()
        if sector in self.emission_tabs:
            self.tabWidget.insertTab(1, self.emission_tabs[sector], sector)
            self.tabWidget.setCurrentIndex(1)


    def get_current_sector_id(self):
        sub_sector_id = self.combo_subsector.currentData()
        if sub_sector_id is not None:
            return sub_sector_id
        sector_id = self.combo_sector.currentData()
        if sector_id is not None:
            return sector_id
        return 0


    '''
    def create_widgets(self, element):
        #layout = QHBoxLayout(

        label_widget = QLabel(element['label'], self)
        fixed_widget = QLineEdit('', self)
        field_widget = QgsFieldComboBox(self)
        field_widget.setFilters(element['types'][0])
        field_widget.setAllowEmptyFieldName(True)

        result = {'label': label_widget, 'fixed': fixed_widget, 'field': field_widget}
        return result
    '''


    def update_field_combos(self):
        for fcb in self.findChildren(QgsFieldComboBox):
            fcb.setLayer(self.combo_layer.currentLayer())


    def update_ok_button(self):
        if self.edit_outfile.text() == '':
            self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
            return
        if self.get_current_sector_id() == 0:
            self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
            return
        self.buttonBox.button(QDialogButtonBox.Save).setEnabled(True)


    def get_fcc_from_gui(self):
        '''Maps items from GUI widgets to IMAER object'''
        result = FeatureCollectionCalculator()

        year = self.combo_project_year.currentData()
        description = self.edit_project_description.text()
        situation_name = self.edit_situation_name.text()

        metadata = AeriusCalculatorMetadata(
            project = {'year': year, 'description': description},
            situation = {'name': situation_name, 'reference': ''},
            version = {'aeriusVersion': '2019A_20200610_3aefc4c15b', 'databaseVersion': '2019A_20200610_3aefc4c15b'}
        )
        result.metadata = metadata

        input_layer = self.combo_layer.currentLayer()
        crs_source = input_layer.crs()
        crs_dest_srid = self.combo_crs.currentData()
        crs_dest = QgsCoordinateReferenceSystem(crs_dest_srid)
        if crs_source == crs_dest:
            crs_transform = None
        else:
            crs_transform = QgsCoordinateTransform(crs_source, crs_dest, QgsProject.instance())

        #print(input_layer)
        emission_sources = {}
        for feat in input_layer.getFeatures():
            local_id = 'ES.{}'.format(feat.id())
            sector_id = self.get_current_sector_id()
            loc_name = self.get_widget_value('loc_name', feat)
            geom = feat.geometry()
            if crs_transform is not None:
                geom.transform(crs_transform)

            es = EmissionSource(local_id, sector_id, loc_name, geom, crs_dest_srid)

            # emission source characteristics
            esc_height = self.get_widget_value('esc_height', feat, 'float')
            esc_heat_content = self.get_widget_value('esc_heat_content', feat, 'float')
            esc_em_temp = self.get_widget_value('esc_em_temp', feat, 'float')
            esc_of_diam = self.get_widget_value('esc_of_diam', feat, 'float')
            esc_of_vel = self.get_widget_value('esc_of_vel', feat, 'float')
            esc_of_dir = self.get_widget_value('esc_of_dir', feat, 'str')
            if esc_heat_content is not None:
                hc = SpecifiedHeatContent(esc_heat_content)
            elif esc_em_temp is not None:
                hc = CalculatedHeatContent(esc_em_temp, esc_of_diam, esc_of_vel, esc_of_dir)
            else:
                hc = None
            if hc is not None and esc_height is not None:
                esc = EmissionSourceCharacteristics(hc, esc_height)

                esc_diurnal_var = self.get_widget_value('esc_diurnal_var', feat, 'float')
                if esc_diurnal_var is not None:
                    esc.diurnal_variation = esc_diurnal_var

                esc_bld_height = self.get_widget_value('esc_bld_height', feat, 'float')
                esc_bld_width = self.get_widget_value('esc_bld_width', feat, 'float')
                esc_bld_length = self.get_widget_value('esc_bld_length', feat, 'float')
                esc_bld_orientation = self.get_widget_value('esc_bld_orientation', feat, 'float')
                if esc_bld_height is not None:
                    bld = Building(esc_bld_height, esc_bld_width, esc_bld_length, esc_bld_orientation)
                    esc.building = bld

                es.es_characteristics = esc

            # emissions
            for substance_code, substance_name in {'NH3': 'emission_nh3', 'NOX': 'emission_nox'}.items():
                em_value = self.get_widget_value(substance_name, feat)
                if em_value is not None:
                    es.add_emission(substance_code, em_value)
            result.add_feature_member(es)

        return result


    def get_widget_value(self, var_name, feat, cast_to=None):
        if not var_name in self.widget_registry:
            return None
        widget_set = self.widget_registry[var_name]
        field_name = widget_set['field'].currentField()
        if field_name == '':
            return None
            #return widget_set['fixed'].text() TODO: return fixed value after data type check (or something..)
        else:
            value = feat[field_name]

        # return None in case attribute value is NULL (empty cell)
        if isinstance(value, QVariant) and str(value) == 'NULL':
            return None

        '''if cast_to is not None:
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
                return result.toString()'''
        return value
