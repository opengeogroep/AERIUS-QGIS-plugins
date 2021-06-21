# -*- coding: utf-8 -*-
import os
import json
import time

from qgis.PyQt.QtWidgets import (
    QDialog,
    QTableWidgetItem
)
from qgis.PyQt import uic


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'connect_receptorsets_dlg.ui'))




class ConnectReceptorSetsDialog(QDialog, FORM_CLASS):

    def __init__(self, plugin, parent=None):
        super(ConnectReceptorSetsDialog, self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.iface = plugin.iface
        #self.open_file_dialog = QFileDialog()

        self.init_gui()


    def init_gui(self):
        self.button_gml_input_browse.clicked.connect(self.browse_gml_file)

        self.button_add_receptorset.clicked.connect(self.post_receptor_set)
        self.button_get_receptorsets.clicked.connect(self.get_receptor_sets)
        self.button_delete_receptorset.clicked.connect(self.delete_receptor_set)

        self.get_receptor_sets()


    def __del__(self):
        self.button_gml_input_browse.clicked.disconnect(self.browse_gml_file)

        self.button_add_receptorset.clicked.disconnect(self.post_receptor_set)
        self.button_get_receptorsets.clicked.disconnect(self.get_receptor_sets)
        self.button_delete_receptorset.clicked.disconnect(self.delete_receptor_set)


    def browse_gml_file(self):
        if self.plugin.dev:
            out_path = '/home/raymond/terglobo/projecten/aerius/202007_calc_input_plugin/demodata'
        else:
            out_path = ''

        gml_fn, filter = self.plugin.calc_input_file_dialog.getOpenFileName(caption="Receptor Set GML file", filter='*.gml', directory=out_path, parent=self.iface.mainWindow())
        self.plugin.log(gml_fn, filter)
        self.edit_gml_input.setText(gml_fn)


    def show_feedback(self, fb):
        print(type(fb))
        if isinstance(fb, dict):
            print('is dict')
            txt = json.dumps(fb, indent=4)
            print(txt)
            self.text_feedback.setText(txt)
        else:
            self.text_feedback.setText(str(fb))


    def get_receptor_sets(self):
        print('get_receptor_sets()')
        self.table_receptorsets.clearContents()
        while self.table_receptorsets.rowCount() > 0:
            self.table_receptorsets.removeRow(0)

        result = self.plugin.aerius_connection.get_receptor_sets()
        if result is None: # TODO check for valid response somehow and show feedback
            return

        receptor_sets_dict = result

        self.show_feedback(receptor_sets_dict)

        for receptor_set in receptor_sets_dict:
            row_num = self.table_receptorsets.rowCount()
            self.table_receptorsets.insertRow(row_num)
            if 'name' in receptor_set:
                self.table_receptorsets.setItem(row_num, 0, QTableWidgetItem(receptor_set['name']))
            if 'description' in receptor_set:
                self.table_receptorsets.setItem(row_num, 1, QTableWidgetItem(receptor_set['description']))




    def post_receptor_set(self):
        gml_fn = self.edit_gml_input.text()
        name = self.edit_name.text()
        description = self.edit_description.text()

        result = self.plugin.aerius_connection.post_receptor_set(gml_fn, name, description)
        #result = self.plugin.aerius_connection.
        self.show_feedback(result.readAll())

        if result is not None:
            self.get_receptor_sets()


    def delete_receptor_set(self):
        '''Sends a delete request to the server for the selected receptor set'''
        items = self.table_receptorsets.selectedItems()
        if len(items) == 0:
            return

        name = None
        for item in items:
            if item.column() == 0:
                name = item.text()

        if name is None:
            return

        result = self.plugin.aerius_connection.delete_receptor_set(name)
        self.show_feedback(result)

        if result is not None:
            self.get_receptor_sets()
