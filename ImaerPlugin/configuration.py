# -*- coding: utf-8 -*-
import os

from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import (
    QDialog
)
from PyQt5 import uic

#from qgis.utils import iface
from qgis.gui import (
    QgsMapLayerComboBox,
    QgsFieldComboBox
)

from .connect import (
    AeriusConnection
)


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'configuration_dlg.ui'))




class ConfigurationDialog(QDialog, FORM_CLASS):

    def __init__(self, plugin, parent=None):
        super(ConfigurationDialog, self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.iface = plugin.iface
        self.connection = AeriusConnection()

        self.init_gui()


    def init_gui(self):
        self.button_get_key.clicked.connect(self.get_api_key)
        if self.plugin.dev:
            self.edit_email.setText('ray@terglobo.nl')


    def __del__(self):
        self.button_get_key.clicked.disconnect(self.get_api_key)


    def get_api_key(self):
        print(self.connection)
        email = self.edit_email.text()
        self.connection.generate_api_key(email)
