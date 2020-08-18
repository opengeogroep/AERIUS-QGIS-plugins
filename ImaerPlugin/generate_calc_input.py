# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
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
        self.sector_id = 0

        self.init_gui()


    def init_gui(self):
        self.combo_layer.setFilters(QgsMapLayerProxyModel.PointLayer) #VectorLayer)

        self.combo_sector.currentIndexChanged.connect(self.set_subsectors)
        self.combo_subsector.currentIndexChanged.connect(self.set_elements)
        self.edit_outfile.textChanged.connect(self.update_ok_button)
        self.set_sectors()
        self.update_ok_button()

        self.combo_layer.layerChanged.connect(self.update_field_combos)


    def __del__(self):
        self.edit_outfile.textChanged.disconnect(self.update_ok_button)
        self.combo_sector.currentIndexChanged.disconnect(self.set_subsectors)
        self.combo_subsector.currentIndexChanged.disconnect(self.set_elements)
        self.combo_layer.layerChanged.disconnect(self.update_field_combos)


    def set_sectors(self):
        self.combo_sector.addItem('<Selecteer een sector>', 0)
        for key, value in emission_sectors.items():
            #print(key, value)
            if 'sector_id' in value:
                sid = value['sector_id']
            else:
                sid = 0
            self.combo_sector.addItem(key, sid)


    def set_subsectors(self):
        sector = self.combo_sector.currentText()
        has_subsectors = sector in emission_sectors and 'subsectors' in emission_sectors[sector]
        self.combo_subsector.clear()
        self.label_subsector.setEnabled(has_subsectors)
        self.combo_subsector.setEnabled(has_subsectors)
        if has_subsectors:
            self.combo_subsector.addItem('<Selecteer een specifieke sector>', 0)
            for key, value in emission_sectors[sector]['subsectors'].items():
                self.combo_subsector.addItem(key, value['sector_id'])
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


    def get_current_sector_id(self):
        sub_sector_id = self.combo_subsector.currentData()
        if sub_sector_id is not None:
            return sub_sector_id
        sector_id = self.combo_sector.currentData()
        if sector_id is not None:
            return sector_id
        return 0


    def set_elements(self):
        self.widget_registry.remove_all_groups()

        self.clear_layout(self.grid_elements)
        #self.grid_elements.update()

        sector_id = self.get_current_sector_id()
        self.update_ok_button()

        if sector_id == 0:
            return

        row = self.grid_elements.rowCount()
        #print(emission_elements)
        for key, element in emission_elements.items():
            #print(key, element)
            if -1 in element['sector_ids'] or sector_id in element['sector_ids']:
                widgets = self.create_widgets(element)
                #print(widgets)

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
        self.update_ok_button()


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


    def update_ok_button(self):
        if self.edit_outfile.text() == '':
            self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
            return
        if self.get_current_sector_id() == 0:
            self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
            return
        self.buttonBox.button(QDialogButtonBox.Save).setEnabled(True)
