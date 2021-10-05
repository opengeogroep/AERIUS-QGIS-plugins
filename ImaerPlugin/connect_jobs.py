# -*- coding: utf-8 -*-
import os
import json

from qgis.PyQt.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QMessageBox
)
from qgis.PyQt import uic

from ImaerPlugin.config import ui_settings

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'connect_jobs_dlg.ui'))




class ConnectJobsDialog(QDialog, FORM_CLASS):

    def __init__(self, plugin, parent=None):
        super(ConnectJobsDialog, self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.iface = plugin.iface

        self.init_gui()


    def init_gui(self):
        self.button_gml_input_browse.clicked.connect(self.browse_gml_file)
        self.button_validate.clicked.connect(self.validate)
        self.button_calculate.clicked.connect(self.calculate)
        self.button_get_jobs.clicked.connect(self.get_jobs)
        self.button_cancel.clicked.connect(self.cancel_jobs)
        self.button_delete.clicked.connect(self.delete_jobs)
        self.button_download.clicked.connect(self.download_jobs)

        self.edit_gml_input.textChanged.connect(self.update_widgets)
        self.combo_calc_type.currentTextChanged.connect(self.update_widgets)
        self.table_jobs.itemSelectionChanged.connect(self.update_widgets)

        self.set_fixed_options()
        self.update_widgets()
        self.get_jobs()


    def __del__(self):
        self.button_gml_input_browse.clicked.disconnect(self.browse_gml_file)
        self.button_validate.clicked.disconnect(self.validate)
        self.button_calculate.clicked.disconnect(self.calculate)
        self.button_get_jobs.clicked.disconnect(self.get_jobs)
        self.button_cancel.clicked.disconnect(self.cancel_jobs)
        self.button_delete.clicked.disconnect(self.delete_jobs)
        self.button_download.clicked.disconnect(self.download_jobs)

        self.edit_gml_input.textChanged.disconnect(self.update_widgets)
        self.combo_calc_type.currentTextChanged.disconnect(self.update_widgets)
        self.table_jobs.itemSelectionChanged.disconnect(self.update_widgets)


    def show_feedback(self, fb):
        if not self.plugin.dev:
            return

        #self.plugin.log('show_feedback()', user='dev')
        #self.plugin.log(str(type(fb)), user='dev')

        if isinstance(fb, dict):
            txt = json.dumps(fb, indent=4)
            print(txt)
            return
            #self.text_feedback.setText(txt)


    def validate(self):
        gml_fn = self.edit_gml_input.text()
        result = self.plugin.aerius_connection.post_validate(gml_fn)

        self.plugin.resp = result # for debugging
        #print(result)
        bstr = result.readAll()

        msg_box = QMessageBox(windowTitle='Validation result', parent=self)
        msg_box.setSizeGripEnabled(True)

        try:
            result_dict = json.loads(bytes(bstr))
            #print(result_dict)
        except:
            self.plugin.log('Server error, no validation response.', lvl='Critical', bar=True)
            msg_box.setText('Server error, no validation response.')
            msg_box.exec()
            return

        if 'successful' in result_dict and result_dict['successful']:
            self.plugin.log('GML is valid', lvl='Info', bar=True)
            msg_box.setText('GML is valid')
        else:
            self.plugin.log('GML is NOT valid.', lvl='Warning', bar=True)
            if 'message' in result_dict:
                error_txt = result_dict['message']
                error_txt = error_txt.replace(' cvc-', '\ncvc-') # Ugly bug fix for ugly response
                msg_box.setText(error_txt)
                for error_line in error_txt.split('\n'):
                    self.plugin.log(error_line, lvl='Warning')
            else:
                msg_box.setText('GML is NOT valid')
        msg_box.exec()


    def calculate(self):
        gml_files = []
        gml_file = {}
        gml_file['gml_fn'] = self.edit_gml_input.text()
        gml_file['situation'] = self.combo_situation.currentText()
        gml_files.append(gml_file)

        user_options = {}
        user_options['name'] = self.edit_name.text()
        user_options['calculationYear'] = int(self.combo_year.currentText())
        user_options['outputType'] = 'GML' # GML or PDF
        user_options['calculationPointsType'] = self.combo_calc_type.currentText()
        if user_options['calculationPointsType'] == 'CUSTOM_POINTS':
            user_options['receptorSetName'] = self.combo_receptor_set.currentData()
        user_options['sendEmail'] = self.checkBox_send_email.isChecked()

        result = self.plugin.aerius_connection.post_calculate(gml_files, user_options)
        #print(result)
        #self.show_feedback(result)

        self.get_jobs()


    def get_jobs(self):
        self.table_jobs.clearContents()
        while self.table_jobs.rowCount() > 0:
            self.table_jobs.removeRow(0)

        if not self.plugin.aerius_connection.api_key_is_ok:
            return

        result = self.plugin.aerius_connection.get_jobs()
        #self.show_feedback(result)

        if result is None:
            return

        jobs_dict = result

        cols = {0: 'name', 1: 'jobKey', 2: 'startDateTime', 3: 'status', 4: 'hectareCalculated'}
        info_col = len(cols) # Last column

        for job in jobs_dict:
            #print(job)
            row_num = self.table_jobs.rowCount()
            self.table_jobs.insertRow(row_num)
            for k,v in cols.items():
                if v in job:
                    self.table_jobs.setItem(row_num, k, QTableWidgetItem(str(job[v])))
            if 'status' in job:
                info_text = None

                if job['status'] == 'ERROR' and 'errorMessage' in job:
                    info_text = job['errorMessage']
                if job['status'] == 'COMPLETED' and 'resultUrl' in job:
                    info_text = job['resultUrl']
                if info_text is not None:
                    self.table_jobs.setItem(row_num, info_col, QTableWidgetItem(info_text))


    def cancel_jobs(self):
        '''Sends a cancel request to the server for the selected jobs'''
        items = self.table_jobs.selectedItems()

        for item in items:
            if item.column() == 1: # jobKey column
                job_key = item.text()
                result = self.plugin.aerius_connection.cancel_job(job_key)
                #self.show_feedback(result)

        self.get_jobs()


    def delete_jobs(self):
        '''Sends a delete request to the server for the selected jobs'''
        items = self.table_jobs.selectedItems()

        for item in items:
            if item.column() == 1: # jobKey column
                job_key = item.text()
                result = self.plugin.aerius_connection.delete_job(job_key)
                #self.show_feedback(result)

        self.get_jobs()


    def download_jobs(self):
        '''Downloads the selected job to the work directory if COMPLETED'''
        items = self.table_jobs.selectedItems()

        for item in items:
            if item.column() == 3: # jobKey column
                status = item.text()
            if item.column() == 5:
                download_url = item.text()
                if status == 'COMPLETED':
                    base_name = download_url.split('/')[-1]
                    work_dir = self.plugin.settings.value('imaer_plugin/work_dir')
                    result = self.plugin.aerius_connection.download_result_zip(download_url, work_dir, base_name)
                    #print(result)
                    #self.show_feedback(result)
                    for gml_fn in result:
                        self.plugin.run_import_calc_result(gml_fn=gml_fn)


    def set_fixed_options(self):
        # data
        for item in ui_settings['project_years']:
            self.combo_year.addItem(item, item)
        self.combo_year.setCurrentText(ui_settings['project_default_year'])

        # calcuation
        #self.edit_name.setText(ui_settings['situation_name'])
        for item in ui_settings['situation_types']:
            self.combo_situation.addItem(item, item)


    def update_widgets(self):
        """logic for widget behaviour"""
        if not self.edit_gml_input.text():
            self.button_validate.setEnabled(False)
            self.button_calculate.setEnabled(False)
        else:
            self.button_validate.setEnabled(True)
        if self.combo_calc_type.currentText() == 'WNB_RECEPTORS':
            self.plugin.log('wnb_receptors', user='dev')
            self.combo_receptor_set.clear()
            self.button_calculate.setEnabled(True)
            self.label_receptor_set.setEnabled(False)
            self.combo_receptor_set.setEnabled(False)
        elif self.combo_calc_type.currentText() == 'CUSTOM_POINTS':
            self.plugin.log('custom_points', user='dev')
            self.update_combo_receptor_set()
            self.label_receptor_set.setEnabled(True)
            self.combo_receptor_set.setEnabled(True)
            if self.combo_receptor_set.currentText():
                self.button_calculate.setEnabled(True)
            else:
                self.button_calculate.setEnabled(False)

        items = self.table_jobs.selectedItems()

        jobs_to_delete = 0
        jobs_to_cancel = 0
        jobs_to_download = 0

        for item in items:
            if item.column() == 3: # status column
                jobs_to_delete += 1 # any job can be deleted
                status = item.text()
                if status == 'RUNNING':
                    jobs_to_cancel += 1
                if status == 'COMPLETED':
                    jobs_to_download += 1
        self.button_delete.setEnabled(jobs_to_delete > 0)
        self.button_cancel.setEnabled(jobs_to_cancel > 0)
        self.button_download.setEnabled(jobs_to_download > 0)


    def update_combo_receptor_set(self):
        """requests available receptor sets and fills combo box """
        self.combo_receptor_set.clear()

        result = self.plugin.aerius_connection.get_receptor_sets()
        #print(result)

        for receptor_set in result:
            name = receptor_set['name']
            #print(name)
            description = receptor_set['description']
            self.combo_receptor_set.addItem(f'{name}: {description}', name)


    def browse_gml_file(self):
        gml_fn, filter = self.plugin.calc_input_file_dialog.getOpenFileName(caption="Input GML file", filter='*.gml', parent=self)
        self.plugin.log(gml_fn, filter)
        self.edit_gml_input.setText(gml_fn)
