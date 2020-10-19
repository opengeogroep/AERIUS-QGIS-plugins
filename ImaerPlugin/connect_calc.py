# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import (
    QDialog
)
from PyQt5 import uic

from .connect import (
    AeriusConnection
)


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'connect_calc_dlg.ui'))




class ConnectCalcDialog(QDialog, FORM_CLASS):

    def __init__(self, plugin, parent=None):
        super(ConnectCalcDialog, self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.iface = plugin.iface
        api_key = self.plugin.settings.value('variables/imaer_plugin_connect_key', defaultValue='')
        self.connection = AeriusConnection(api_key=api_key)

        self.init_gui()


    def init_gui(self):
        self.button_validate.clicked.connect(self.validate)
        self.button_calculate.clicked.connect(self.calculate)
        self.button_jobs.clicked.connect(self.status_jobs)


    def __del__(self):
        self.button_validate.clicked.disconnect(self.validate)
        self.button_calculate.clicked.disconnect(self.calculate)
        self.button_jobs.clicked.disconnect(self.status_jobs)


    def validate(self):
        print(self.connection)
        gml_fn = self.edit_gml_input.text()
        print(gml_fn)

        result = self.connection.validate(gml_fn)

        if result['successful']:
            print('GML file is valid')
        else:
            print('GML is NOT valid:')
            for line in result['errors']:
                print('  {}'.format(line['message']))


    def calculate(self):
        print(self.connection)
        gml_fn = self.edit_gml_input.text()
        print(gml_fn)

        result = self.connection.calculate(gml_fn)
        print(result)


    def status_jobs(self):
        print(self.connection)
        result = self.connection.status_jobs()
        print(result)
