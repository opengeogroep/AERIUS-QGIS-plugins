# -*- coding: utf-8 -*-
import os
import json

from PyQt5.QtWidgets import (
    QDialog
)
from PyQt5 import uic

from .connect import (
    AeriusConnection
)


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'connect_receptorsets_dlg.ui'))




class ConnectReceptorSetsDialog(QDialog, FORM_CLASS):

    def __init__(self, plugin, parent=None):
        super(ConnectReceptorSetsDialog, self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.iface = plugin.iface
        api_key = self.plugin.settings.value('variables/imaer_plugin_connect_key', defaultValue='')
        self.connection = AeriusConnection(api_key=api_key)

        self.init_gui()


    def init_gui(self):
        self.button_receptorsets.clicked.connect(self.receptor_sets)


    def __del__(self):
        self.button_receptorsets.clicked.disconnect(self.receptor_sets)


    def show_feedback(self, fb):
        print(type(fb))
        if isinstance(fb, dict):
            print('is dict')
            txt = json.dumps(fb, indent=4)
            print(txt)
            self.text_feedback.setText(txt)
        else:
            self.text_feedback.setText(str(fb))


    def receptor_sets(self):
        result = self.connection.receptor_sets()
        self.show_feedback(result)
