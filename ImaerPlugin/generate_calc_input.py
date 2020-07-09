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

from .config import (
    emission_sectors,
    emission_elements
)


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'generate_calc_input_dlg.ui'))




class GenerateCalcInputDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(GenerateCalcInputDialog, self).__init__(parent)

        self.setupUi(self)
        self.iface = iface
        self.init_gui()


    def init_gui(self):
        self.combo_sector.currentIndexChanged.connect(self.set_subsectors)
        self.set_sectors()


    def __del__(self):
        self.combo_sector.currentIndexChanged.disconnect(self.set_subsectors)


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
        self.clear_layout(self.layout_elements)

        self.layout_elements.update()
        for key in emission_elements:
            print(key)
            element = emission_elements[key]
            print(element)

            layout = self.create_widgets(element)
            print(layout)
            self.layout_elements.addLayout(layout)

            #self.combo_subsector.addItem(key)


    def create_widgets(self, element):
        layout = QHBoxLayout()

        label_widget = QLabel(element['name'], self)
        layout.addWidget(label_widget)

        edit_widget = QLineEdit('', self)
        layout.addWidget(edit_widget)

        return layout
