# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QHBoxLayout
)
from PyQt5 import uic

from qgis.utils import iface
from qgis.gui import (
    QgsMapLayerComboBox,
    QgsFieldComboBox
)
from qgis.core import QgsMapLayerProxyModel

from .config import (
    emission_sectors,
    emission_elements
)

from .widget_registry import WidgetRegistry


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'generate_calc_input_dlg.ui'))




class GenerateCalcInputDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(GenerateCalcInputDialog, self).__init__(parent)

        self.setupUi(self)
        self.iface = iface
        self.widget_registry = WidgetRegistry(self)

        self.init_gui()


    def init_gui(self):
        self.combo_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.combo_sector.currentIndexChanged.connect(self.set_subsectors)
        self.set_sectors()

        self.combo_layer.layerChanged.connect(self.update_field_combos)


    def __del__(self):
        self.combo_sector.currentIndexChanged.disconnect(self.set_subsectors)
        self.combo_layer.layerChanged.disconnect(self.update_field_combos)


    def set_sectors(self):
        self.combo_sector.addItem('<Selecteer een sector>')
        for key in emission_sectors:
            self.combo_sector.addItem(key)


    def set_subsectors(self):
        sector = self.combo_sector.currentText()
        has_subsectors = sector in emission_sectors and 'subsectors' in emission_sectors[sector]
        self.combo_subsector.clear()
        self.label_subsector.setEnabled(has_subsectors)
        self.combo_subsector.setEnabled(has_subsectors)
        if has_subsectors:
            self.combo_subsector.addItem('<Selecteer een specifieke sector>')
            for key in emission_sectors[sector]['subsectors']:
                self.combo_subsector.addItem(key)
            # !!!
            self.set_elements()


    def clear_layout(self, layout):
        ''' recursively clears a layout from all widgets and layouts '''
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
                elif child.layout() is not None:
                    self.clear_layout(child.layout())


    def set_elements(self):
        print(self.widget_registry)
        self.widget_registry.remove_all_groups()
        print(self.widget_registry)

        self.clear_layout(self.grid_elements)
        #self.grid_elements.update()

        row = self.grid_elements.rowCount()
        print(emission_elements)
        for key, element in emission_elements.items():
            print(key, element)
            widgets = self.create_widgets(element)
            print(widgets)

            if 'label' in widgets:
                self.grid_elements.addWidget(widgets['label'], row, 0)
            if 'fixed' in widgets:
                self.grid_elements.addWidget(widgets['fixed'], row, 1)
            if 'field' in widgets:
                self.grid_elements.addWidget(widgets['field'], row, 2)

            self.widget_registry.add_widgets(key, widgets)
            row += 1

        self.widget_registry.show()
        self.update_field_combos()


    def create_widgets(self, element):
        #layout = QHBoxLayout(

        label_widget = QLabel(element['label'], self)
        fixed_widget = QLineEdit('', self)
        field_widget = QgsFieldComboBox(self)
        field_widget.setFilters(element['types'][0])
        field_widget.setAllowEmptyFieldName(True)

        result = {'label': label_widget, 'fixed': fixed_widget, 'field': field_widget}
        return result


    def update_field_combos(self):
        for name in self.widget_registry:
            for widget_key, widget in self.widget_registry[name].items():
                if widget_key == 'field':
                    if isinstance(widget, QgsFieldComboBox):
                        widget.setLayer(self.combo_layer.currentLayer())
                    else:
                        widget.setLayer(None)
