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
from qgis import processing

from ImaerPlugin.styles import StyleFactory

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'relate_calc_results_dlg.ui'))


class RelateCalcResultsDialog(QDialog, FORM_CLASS):

    def __init__(self, plugin, parent=None):
        super(RelateCalcResultsDialog, self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.iface = plugin.iface
        self.style_factory = StyleFactory(plugin)

        self.init_gui()

    def init_gui(self):
        self.layer_widgets = {
            1: self.combo_layer1,
            2: self.combo_layer2,
            3: self.combo_layer3,
            4: self.combo_layer4,
            5: self.combo_layer5
        }
        for key, widget in self.layer_widgets.items():
            # print(widget)
            #widget.setFilters(LayerFilters(QgsMapLayerProxyModel.PointLayer, QgsMapLayerProxyModel.PolygonLayer))
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

        # Only enable 3+ layer combos if calc_type is not 'difference'
        for key, widget in self.layer_widgets.items():
            if key > 2:
                widget.setEnabled(calc_type != 'difference')

    def is_dep_layer(self, layer):
        '''Checks if layer contains all mandatory fields'''
        return True # TODO Make this check work again.
        mandatory_fields = ['fid', 'dep_NH3', 'dep_NOX']

        layer_field_names = [fld.name() for fld in layer.fields()]

        for mandatory_field in mandatory_fields:
            if mandatory_field not in layer_field_names:
                return False
        return True

    def get_layer_list(self):
        '''Returns a list of selected deposition layers in the enabled comboBoxes'''
        result = []
        for key, widget in self.layer_widgets.items():
            if widget.isEnabled():
                layer = widget.currentLayer()
                if layer is not None:
                    if self.is_dep_layer(layer):
                        widget.setStyleSheet("QgsMapLayerComboBox { color : black; }")
                        result.append(layer)
                    else:
                        widget.setStyleSheet("QgsMapLayerComboBox { color : red; }")
                else:
                    widget.setStyleSheet("QgsMapLayerComboBox { color : black; }")
        return result

    def gui_update_layer_combo(self):
        calc_type = self.combo_calc_type.currentText()
        layers = self.get_layer_list()
        enable_ok_button = len(layers) >= 2
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(enable_ok_button)

    def add_result_layer(self, layer, layer_name):
        layer.setName(layer_name)

        self.plugin.set_imaer_styles(layer, 'difference')

        QgsProject.instance().addMapLayer(layer)


    def calculate_difference(self, layers, layer_name):
        layer_1 = layers[0]
        layer_2 = layers[1]

        params = {
            'INPUT_1': layer_1,
            'INPUT_2': layer_2,
            'OUTPUT': 'memory:'
        }
        result = processing.run("imaer:relate_difference", params)
        layer = result['OUTPUT']

        self.add_result_layer(layer, layer_name)

    def calculate_sum(self, layers, layer_name):
        params = {
            'INPUT_LAYERS': layers,
            'OUTPUT': 'memory:'
        }
        result = processing.run("imaer:relate_sum", params)
        layer = result['OUTPUT']

        self.add_result_layer(layer, layer_name)

    def calculate_maximum(self, layers, layer_name):
        params = {
            'INPUT_LAYERS': layers,
            'OUTPUT': 'memory:'
        }
        result = processing.run("imaer:relate_maximum", params)
        layer = result['OUTPUT']

        self.add_result_layer(layer, layer_name)
