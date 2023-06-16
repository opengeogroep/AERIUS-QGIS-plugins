# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox
)

from qgis.utils import iface

from ImaerPlugin.imaer5 import CustomDiurnalVariation

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'diurnal_variation_dlg.ui'))


class DiurnalVariationDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(DiurnalVariationDialog, self).__init__(parent)

        self.setupUi(self)
        self.iface = iface

        self.init_gui()

    def init_gui(self):
        self.update_ok_button()

    def __del__(self):
        pass

    def update_ok_button(self):
        if False:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
