# -*- coding: utf-8 -*-
import os

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox
)

from qgis.utils import iface

from ImaerPlugin.imaer6 import CustomTimeVaryingProfile
from ImaerPlugin.config import ui_settings

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'time_varying_profile_dlg.ui'))


class TimeVaryingProfileDialog(QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(TimeVaryingProfileDialog, self).__init__(parent)

        self.setupUi(self)
        self.iface = iface

        self.init_gui()

    def init_gui(self):
        self.combo_custom_type.addItems(ui_settings['time_varying_profile_types'])
        self.combo_custom_type.currentIndexChanged.connect(self.update_ok_button)
        self.plainTextEdit_csv.textChanged.connect(self.update_ok_button)
        self.update_ok_button()

    def __del__(self):
        self.combo_custom_type.currentIndexChanged.disconnect(self.update_ok_button)
        self.plainTextEdit_csv.textChanged.disconnect(self.update_ok_button)

    def update_ok_button(self):
        tvp = self.get_tvp()
        if tvp is None:
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            return
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def set_by_tvp(self, tvp):
        self.lineEdit_id.setText(str(tvp.local_id))
        self.lineEdit_label.setText(tvp.label)
        self.combo_custom_type.setCurrentText(tvp.custom_type)
        doc = self.plainTextEdit_csv.document()
        doc.setPlainText(tvp.values_to_csv())
        self.plainTextEdit_csv.setDocument(doc)

    def get_tvp(self):
        local_id = self.lineEdit_id.text()
        label = self.lineEdit_label.text()
        doc = self.plainTextEdit_csv.document()
        csv_txt = doc.toPlainText()
        custom_type = self.combo_custom_type.currentText()
        result = CustomTimeVaryingProfile(local_id=local_id, label=label, custom_type=custom_type)
        check = result.values_from_csv(csv_txt)
        if check is True:
            return result
        else:
            return None
