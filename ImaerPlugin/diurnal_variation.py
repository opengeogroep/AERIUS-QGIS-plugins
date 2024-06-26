# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox
)

from qgis.utils import iface

from ImaerPlugin.imaer6 import CustomDiurnalVariation

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'diurnal_variation_dlg.ui'))


class DiurnalVariationDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(DiurnalVariationDialog, self).__init__(parent)

        self.setupUi(self)
        self.iface = iface

        self.init_gui()

    def init_gui(self):
        self.plainTextEdit_csv.textChanged.connect(self.update_ok_button)
        self.update_ok_button()

    def __del__(self):
        self.plainTextEdit_csv.textChanged.disconnect(self.update_ok_button)

    def update_ok_button(self):
        dv = self.get_dv()
        if dv is None:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def set_by_dv(self, dv):
        self.lineEdit_id.setText(str(dv.local_id))
        self.lineEdit_label.setText(dv.label)
        doc = self.plainTextEdit_csv.document()
        doc.setPlainText(dv.values_to_csv())
        self.plainTextEdit_csv.setDocument(doc)

    def get_dv(self):
        local_id = self.lineEdit_id.text()
        label = self.lineEdit_label.text()
        doc = self.plainTextEdit_csv.document()
        csv_txt = doc.toPlainText()
        result = CustomDiurnalVariation(local_id=local_id, label=label, custom_type='THREE_DAY')
        check = result.values_from_csv(csv_txt)
        if check is True:
            return result
        else:
            return None
