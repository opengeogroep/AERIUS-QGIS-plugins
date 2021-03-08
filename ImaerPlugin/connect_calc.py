# -*- coding: utf-8 -*-
import os
import json

from qgis.PyQt.QtWidgets import (
    QDialog
)
from qgis.PyQt import uic

from ImaerPlugin.connect import (
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
        self.button_gml_input_browse.clicked.connect(self.browse_gml_file)
        self.button_jobs.clicked.connect(self.status_jobs)
        self.button_validate.clicked.connect(self.validate)
        self.button_calculate.clicked.connect(self.calculate)

        self.edit_gml_input.textChanged.connect(self.update_widgets)
        self.combo_calc_type.currentTextChanged.connect(self.update_widgets)

        self.update_widgets()


    def __del__(self):
        self.button_gml_input_browse.clicked.disconnect(self.browse_gml_file)
        self.button_jobs.clicked.disconnect(self.status_jobs)
        self.button_validate.clicked.disconnect(self.validate)
        self.button_calculate.clicked.disconnect(self.calculate)

        self.edit_gml_input.textChanged.disconnect(self.update_widgets)
        self.combo_calc_type.currentTextChanged.disconnect(self.update_widgets)


    def show_feedback(self, fb):
        print(type(fb))
        if isinstance(fb, dict):
            print('is dict')
            txt = json.dumps(fb, indent=4)
            print(txt)
            self.text_feedback.setText(txt)
        else:
            self.text_feedback.setText(str(fb))


    def validate(self):
        gml_fn = self.edit_gml_input.text()
        result = self.connection.validate(gml_fn)
        '''
        if result['successful']:
            print('GML file is valid')
        else:
            print('GML is NOT valid:')
            for line in result['errors']:
                print('  {}'.format(line['message']))
        '''
        self.show_feedback(result)


    def calculate(self):
        gml_fn = self.edit_gml_input.text()

        user_options = {}

        user_options['calculationType'] = self.combo_calc_type.currentText()

        if user_options['calculationType'] == 'CUSTOM_POINTS':
            user_options['receptorSetName'] = self.combo_receptor_set.currentData()

        #print(user_options)

        result = self.connection.calculate(gml_fn, user_options)
        self.show_feedback(result)


    def status_jobs(self):
        result = self.connection.status_jobs()
        self.show_feedback(result)


    def update_widgets(self):
        """logic for widget behaviour"""
        if not self.edit_gml_input.text():
            self.button_validate.setEnabled(False)
            self.button_calculate.setEnabled(False)
        else:
            self.button_validate.setEnabled(True)
            if self.combo_calc_type.currentText() == 'NBWET':
                print('nbwet')
                self.combo_receptor_set.clear()
                self.button_calculate.setEnabled(True)
                self.label_receptor_set.setEnabled(False)
                self.combo_receptor_set.setEnabled(False)
            elif self.combo_calc_type.currentText() == 'CUSTOM_POINTS':
                print('custom_points')
                self.update_combo_receptor_set()
                self.label_receptor_set.setEnabled(True)
                self.combo_receptor_set.setEnabled(True)
                if not self.combo_receptor_set.currentText():
                    self.button_calculate.setEnabled(False)


    def update_combo_receptor_set(self):
        """requests available receptor sets and fills combo box """
        self.combo_receptor_set.clear()

        result = self.connection.get_receptor_sets()

        if not 'receptorSets' in result:
            return

        for receptor_set in result['receptorSets']:
            name = receptor_set['name']
            #print(name)
            description = receptor_set['description']
            self.combo_receptor_set.addItem(f'{name}: {description}', name)


    def browse_gml_file(self):
        if self.plugin.dev:
            out_path = '/home/raymond/calcinput_20200928_165149.gml'
        else:
            out_path = ''

        gml_fn, filter = self.plugin.calc_input_file_dialog.getOpenFileName(caption="Calculation input GML file", filter='*.gml', directory=out_path, parent=self.iface.mainWindow())
        self.plugin.log(gml_fn, filter)
        self.edit_gml_input.setText(gml_fn)
