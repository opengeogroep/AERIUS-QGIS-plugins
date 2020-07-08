# -*- coding: utf-8 -*-

import os

from qgis.utils import iface
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

from qgis.gui import QgsMapLayerComboBox

from .config import emission_sectors



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'generate_calc_input_dlg.ui'))




class GenerateCalcInputDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(GenerateCalcInputDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
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
