# -*- coding: utf-8 -*-
import os

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox
)
from qgis.PyQt import uic

from qgis.core import (
    QgsVectorLayer,
    QgsField,
    QgsProject,
    QgsFeature,
    QgsMapLayerProxyModel,
    Qgis
)

from qgis.gui import QgsMessageBar

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'relate_calc_results_dlg.ui'))




class RelateCalcResultsDialog(QDialog, FORM_CLASS):

    def __init__(self, plugin, parent=None):
        super(RelateCalcResultsDialog, self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.iface = plugin.iface
        self.geometry_cache = {}
        self.dep_field_names = ['dep_NH3', 'dep_NOX']
        self.dep_total_field_name = 'dep_TOTAL'

        self.init_gui()


    def init_gui(self):
        self.layer_widgets = {
            1: self.combo_layer1,
            2: self.combo_layer2
        }
        for key, widget in self.layer_widgets.items():
            #print(widget)
            widget.setFilters(QgsMapLayerProxyModel.PolygonLayer)
            widget.setAllowEmptyLayer(True)
            widget.setCurrentIndex(0)
            widget.currentIndexChanged.connect(self.gui_update_layer_combo)

        self.combo_calc_type.currentIndexChanged.connect(self.gui_update_calc_type)

        self.gui_update_calc_type()
        self.gui_update_layer_combo()


    def __del__(self):
        self.combo_calc_type.currentIndexChanged.disconnect(self.gui_update_calc_type)
        for key, widget in self.layer_widgets.items():
            widget.currentIndexChanged.connect(self.gui_update_layer_combo)


    def gui_update_calc_type(self):
        calc_type = self.combo_calc_type.currentText()
        self.edit_layer_name.setText(calc_type)


    def gui_update_layer_combo(self):
        calc_type = self.combo_calc_type.currentText()
        layer_1 = self.layer_widgets[1].currentLayer()
        layer_2 = self.layer_widgets[2].currentLayer()
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(layer_1 is not None and layer_2 is not None)


    def show_error(self, msg):
        self.iface.messageBar().pushMessage('Error', msg, level=Qgis.Critical, duration=10)


    def create_result_layer(self, layer_name, qml_file_name=None):
        crs = self.plugin.iface.mapCanvas().mapSettings().destinationCrs().authid()
        feature_type = 'Polygon?crs={}'.format(crs)
        layer = QgsVectorLayer(feature_type, layer_name, 'memory')

        provider = layer.dataProvider()

        fields = []
        fields.append(QgsField('fid', QVariant.LongLong, 'int8'))
        for dep_field_name in self.dep_field_names:
            fields.append(QgsField(dep_field_name, QVariant.Double))

        if self.checkBox_add_totals.isChecked():
            fields.append(QgsField(self.dep_total_field_name, QVariant.Double))

        provider.addAttributes(fields)
        layer.updateFields()

        QgsProject.instance().addMapLayer(layer)

        if qml_file_name is not None:
            layer.loadNamedStyle(qml_file_name)

        return (layer, provider)


    def create_result_feature(self, receptor_id, dep_dict, max_decimals=None):
        feat = QgsFeature()
        geometry = self.geometry_cache[receptor_id]
        feat.setGeometry(geometry)
        attributes = [receptor_id]
        dep_total = 0
        for field_name in dep_dict:
            v = dep_dict[field_name]
            dep_total += v
            if max_decimals is not None:
                v = round(v, max_decimals)
            attributes.append(v)

        if self.checkBox_add_totals.isChecked():
            if max_decimals is not None:
                dep_total = round(dep_total, max_decimals)
            attributes.append(dep_total)

        feat.setAttributes(attributes)
        return feat


    def create_result_features(self, calc_result_dict, qml_file_name):
        layer_name = self.edit_layer_name.text()
        result_layer, result_provider = self.create_result_layer(layer_name, qml_file_name)
        for receptor_id in calc_result_dict:
            feat = self.create_result_feature(receptor_id, calc_result_dict[receptor_id], 8)
            result_provider.addFeatures([feat])


    def create_receptor_dictionary(self, layer):
        layer_field_names = [fld.name() for fld in layer.fields()]
        for field_name in ['fid'] + self.dep_field_names:
            if field_name not in layer_field_names:
                return None
        result = {}
        for feat in layer.getFeatures():
            receptor_id = feat['fid']
            dep_dict = {}
            for dep_field_name in self.dep_field_names:
                v = feat[dep_field_name]
                if isinstance(v, QVariant) and str(v) == 'NULL':
                    v = None
                dep_dict[dep_field_name] = v
            result[receptor_id] = dep_dict
            if receptor_id not in self.geometry_cache:
                self.geometry_cache[receptor_id] = feat.geometry()
        #print(result)
        return result


    def __get_receptor_value(self, receptor_dict, receptor_id, field_name):
        if receptor_id not in receptor_dict:
            return 0
        if field_name in receptor_dict[receptor_id]:
            value = receptor_dict[receptor_id][field_name]
        if value is None:
            return 0
        return value


    def __calc_dict_difference(self, dep_dict_layer_1, dep_dict_layer_2):
        result = {}
        for receptor_id in self.geometry_cache:
            dep_dict = {}
            for dep_field_name in self.dep_field_names:
                v1 = self.__get_receptor_value(dep_dict_layer_1, receptor_id, dep_field_name)
                v2 = self.__get_receptor_value(dep_dict_layer_2, receptor_id, dep_field_name)
                dep_dict[dep_field_name] = v1 - v2
            result[receptor_id] = dep_dict
        return result


    def calculate_difference(self, layer_1, layer_2):
        self.geometry_cache = {}

        dep_dict_layer_1 = self.create_receptor_dictionary(layer_1)
        if dep_dict_layer_1 is None:
            layer_name = layer_1.name()
            self.show_error(f'"{layer_name}" is not a valid deposition layer.')
            return

        dep_dict_layer_2 = self.create_receptor_dictionary(layer_2)
        if dep_dict_layer_2 is None:
            layer_name = layer_2.name()
            self.show_error(f'"{layer_name}" is not a valid deposition layer.')
            return

        qml_file_name = os.path.join(self.plugin.plugin_dir, 'styles', 'calc_result_diff.qml')
        calc_result_dict = self.__calc_dict_difference(dep_dict_layer_1, dep_dict_layer_2)
        self.create_result_features(calc_result_dict, qml_file_name)

        self.geometry_cache = {}


    def __calc_dict_sum(self, in_dep_dicts):
        result = {}
        for receptor_id in self.geometry_cache:
            out_dep_dict = {}
            for in_dep_dict in in_dep_dicts:
                for dep_field_name in self.dep_field_names:
                    v = self.__get_receptor_value(in_dep_dict, receptor_id, dep_field_name)
                    if dep_field_name in out_dep_dict:
                        out_dep_dict[dep_field_name] += v
                    else:
                        out_dep_dict[dep_field_name] = v
            result[receptor_id] = out_dep_dict
        return result


    def calculate_sum(self, layers):
        self.geometry_cache = {}

        dep_dicts = []
        for layer in layers:
            dep_dict_layer = self.create_receptor_dictionary(layer)
            if dep_dict_layer is None:
                layer_name = layer.name()
                self.show_error(f'"{layer_name}" is not a valid deposition layer.')
                return
            dep_dicts.append(dep_dict_layer)

        qml_file_name = os.path.join(self.plugin.plugin_dir, 'styles', 'calc_result_diff.qml')
        calc_result_dict = self.__calc_dict_sum(dep_dicts)
        self.create_result_features(calc_result_dict, qml_file_name)

        self.geometry_cache = {}
