# -*- coding: utf-8 -*-
import os
import json

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import (
    QDialog,
    QTableWidgetItem,
    QMessageBox,
    QComboBox,
    QPushButton,
    QLineEdit
)
from qgis.PyQt.QtCore import Qt

from qgis.core import QgsApplication

from ImaerPlugin.config import ui_settings

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'connect_jobs_dlg.ui'))


class ConnectJobsDialog(QDialog, FORM_CLASS):

    def __init__(self, plugin, parent=None):
        super(ConnectJobsDialog, self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.iface = plugin.iface

        self.data_widget_matrix = self.get_data_widget_matrix()
        self.init_gui()

    def init_gui(self):
        for widget in self.get_data_widgets_by_base_name('button_gml_input_browse'):
            widget.clicked.connect(self.browse_gml_file)
        for widget in self.get_data_widgets_by_base_name('button_validate'):
            widget.clicked.connect(self.validate)
        self.button_calculate.clicked.connect(self.calculate)

        self.button_get_jobs.clicked.connect(self.get_jobs)
        self.button_cancel.clicked.connect(self.cancel_jobs)
        self.button_delete.clicked.connect(self.delete_jobs)
        self.button_download.clicked.connect(self.download_jobs)

        for widget in self.get_data_widgets_by_base_name('edit_gml_input'):
            widget.textChanged.connect(self.update_widgets)
        self.combo_calc_type.currentTextChanged.connect(self.update_widgets)
        self.table_jobs.itemSelectionChanged.connect(self.update_widgets)

        self.set_fixed_options()

        if self.plugin.dev:
            gml_file = '/home/raymond/terglobo/projecten/aerius/202007_calc_input_plugin/demodata/gen_calc_input/calcinput_20210930_130723.gml'
            self.edit_gml_input_1.setText(gml_file)
            self.edit_gml_input_2.setText(gml_file)
            #self.combo_situation_1.setCurrentText('REFERENCE')
            #self.combo_situation_2.setCurrentText('REFERENCE')
            self.combo_year_1.setCurrentText('2022')
            self.combo_year_2.setCurrentText('2023')

        self.update_widgets()
        self.get_jobs()

    def __del__(self):
        for widget in self.get_data_widgets_by_base_name('button_gml_input_browse'):
            widget.clicked.disconnect(self.browse_gml_file)
        for widget in self.get_data_widgets_by_base_name('button_validate'):
            widget.clicked.disconnect(self.validate)
        self.button_calculate.clicked.disconnect(self.calculate)

        self.button_get_jobs.clicked.disconnect(self.get_jobs)
        self.button_cancel.clicked.disconnect(self.cancel_jobs)
        self.button_delete.clicked.disconnect(self.delete_jobs)
        self.button_download.clicked.disconnect(self.download_jobs)

        for widget in self.get_data_widgets_by_base_name('edit_gml_input'):
            widget.textChanged.disconnect(self.update_widgets)
        self.combo_calc_type.currentTextChanged.disconnect(self.update_widgets)
        self.table_jobs.itemSelectionChanged.disconnect(self.update_widgets)

    def show_feedback(self, fb):
        if not self.plugin.dev:
            return

        # self.plugin.log('show_feedback()', user='dev')
        # self.plugin.log(str(type(fb)), user='dev')

        if isinstance(fb, dict):
            txt = json.dumps(fb, indent=4)
            print(txt)
            return
            # self.text_feedback.setText(txt)

    def validate(self):
        related_widgets = self.get_related_data_widgets(self.sender())
        gml_fn = related_widgets['edit_gml_input'].text()

        QgsApplication.setOverrideCursor(Qt.WaitCursor)
        result = self.plugin.aerius_connection.post_validate(gml_fn)
        QgsApplication.restoreOverrideCursor()

        # self.plugin.resp = result # for debugging
        # print(result)
        bstr = result.readAll()
        # print(bstr)

        msg_box = QMessageBox(windowTitle='Validation result', parent=self)
        msg_box.setSizeGripEnabled(True)

        try:
            result_dict = json.loads(bytes(bstr))
            # print(result_dict)
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

            msg_box.setText('GML is NOT valid. (Errors can not be parsed)')
            error_txt = None
            if 'message' in result_dict:
                error_txt = result_dict['message']
            elif 'errors' in result_dict:
                errors = result_dict['errors']
                if len(errors) > 0:
                    error1 = errors[0]
                    if 'message' in error1:
                        error_txt = error1['message']
            if error_txt is not None:
                error_txt = error_txt.replace(' cvc-', '\ncvc-')  # Ugly bug fix for ugly response
                msg_box.setText(error_txt)
                for error_line in error_txt.split('\n'):
                    self.plugin.log(error_line, lvl='Warning')
        msg_box.exec()

    def calculate(self):
        gml_files = self.get_calculation_files()
        # print(gml_files)

        user_options = {}
        user_options['name'] = self.edit_name.text()
        user_options['calculationYear'] = int(self.combo_year_1.currentText())
        user_options['outputType'] = 'GML'  # GML or PDF
        user_options['calculationPointsType'] = self.combo_calc_type.currentText()
        if user_options['calculationPointsType'] == 'CUSTOM_POINTS':
            user_options['receptorSetName'] = self.combo_receptor_set.currentData()
        user_options['sendEmail'] = self.checkBox_send_email.isChecked()

        QgsApplication.setOverrideCursor(Qt.WaitCursor)
        result = self.plugin.aerius_connection.post_calculate(gml_files, user_options)
        QgsApplication.restoreOverrideCursor()

        # print(result)
        # self.show_feedback(result)

        self.get_jobs()

    def get_jobs(self):
        self.table_jobs.clearContents()
        while self.table_jobs.rowCount() > 0:
            self.table_jobs.removeRow(0)

        if not self.plugin.aerius_connection.api_key_is_ok:
            return

        QgsApplication.setOverrideCursor(Qt.WaitCursor)
        result = self.plugin.aerius_connection.get_jobs()
        QgsApplication.restoreOverrideCursor()
        # self.show_feedback(result)

        if result is None:
            return

        jobs_dict = result

        cols = {0: 'name', 1: 'jobKey', 2: 'startDateTime', 3: 'status', 4: 'hectareCalculated'}
        info_col = len(cols)  # Last column

        for job in jobs_dict:
            row_num = self.table_jobs.rowCount()
            self.table_jobs.insertRow(row_num)
            for k, v in cols.items():
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

        QgsApplication.setOverrideCursor(Qt.WaitCursor)
        for item in items:
            if item.column() == 1:  # jobKey column
                job_key = item.text()
                result = self.plugin.aerius_connection.cancel_job(job_key)
                # self.show_feedback(result)
        QgsApplication.restoreOverrideCursor()

        self.get_jobs()

    def delete_jobs(self):
        '''Sends a delete request to the server for the selected jobs'''
        items = self.table_jobs.selectedItems()

        QgsApplication.setOverrideCursor(Qt.WaitCursor)
        for item in items:
            if item.column() == 1:  # jobKey column
                job_key = item.text()
                result = self.plugin.aerius_connection.delete_job(job_key)
                # self.show_feedback(result)
        QgsApplication.restoreOverrideCursor()

        self.get_jobs()

    def download_jobs(self):
        '''Downloads the selected job to the work directory if COMPLETED'''
        items = self.table_jobs.selectedItems()

        QgsApplication.setOverrideCursor(Qt.WaitCursor)
        for item in items:
            if item.column() == 3:  # jobKey column
                status = item.text()
            if item.column() == 5:
                download_url = item.text()
                if status == 'COMPLETED':
                    base_name = download_url.split('/')[-1]
                    work_dir = self.plugin.settings.value('imaer_plugin/work_dir')
                    result = self.plugin.aerius_connection.download_result_zip(download_url, work_dir, base_name)
                    # print(result)
                    # self.show_feedback(result)
                    for gml_fn in result:
                        self.plugin.run_import_calc_result(gml_fn=gml_fn)
        QgsApplication.restoreOverrideCursor()

    def get_data_widget_matrix(self):
        '''Creates a matrix with all data widgets, for quickly finding related widgets.'''
        widget_types = [
            {'base_name': 'combo_situation', 'type': QComboBox},
            {'base_name': 'combo_year', 'type': QComboBox},
            {'base_name': 'edit_gml_input', 'type': QLineEdit},
            {'base_name': 'button_gml_input_browse', 'type': QPushButton},
            {'base_name': 'button_validate', 'type': QPushButton},
        ]
        result = {}
        for i in range(1, 7): #  There are 6 rows of emission data widgets
            result[i] = {}
            for widget_type in widget_types:
                widget_name = '{}_{}'.format(widget_type['base_name'], i)
                widget = self.findChild(widget_type['type'], widget_name)
                result[i][widget_type['base_name']] = widget
        return result

    def get_related_data_widgets(self, source_widget):
        '''Returns all data widgets in the same row.'''
        widget_number = source_widget.objectName()[-1:]
        return self.data_widget_matrix[int(widget_number)]

    def get_data_widgets_by_base_name(self, base_name):
        '''Returns all data widgets of the same type.'''
        result = []
        for k, v in self.data_widget_matrix.items():
            result.append(v[base_name])
        return result

    def set_fixed_options(self):
        # emission data
        for widget in self.get_data_widgets_by_base_name('combo_year'):
            for item in ui_settings['project_years']:
                widget.addItem(item, item)
            widget.setCurrentText(ui_settings['project_default_year'])

        for widget in self.get_data_widgets_by_base_name('combo_situation'):
            for item in ui_settings['situation_types']:
                widget.addItem(item, item)

    def update_widgets(self):
        """Logic for widget behaviour"""
        print('update_widgets()')
        return #  For now, while WIP on the dialog.
        if not self.edit_gml_input_1.text():
            self.button_validate_1.setEnabled(False)
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
            if item.column() == 3:  # status column
                jobs_to_delete += 1  # any job can be deleted
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
        # print(result)

        for receptor_set in result:
            name = receptor_set['name']
            # print(name)
            description = receptor_set['description']
            self.combo_receptor_set.addItem(f'{name}: {description}', name)

    def browse_gml_file(self):
        gml_fn, filter = self.plugin.calc_input_file_dialog.getOpenFileName(caption="Input GML file", filter='*.gml', parent=self)
        self.plugin.log(gml_fn, filter)
        related_widgets = self.get_related_data_widgets(self.sender())
        related_widgets['edit_gml_input'].setText(gml_fn)

    def gml_file_exists(self, fn):
        if os.path.exists(fn):
            return True
        else:
            return False

    def get_calculation_files(self):
        result = []
        for widget in self.get_data_widgets_by_base_name('edit_gml_input'):
            #print(widget)
            #print(widget.text())
            #print(self.gml_file_exists(widget.text()))
            if self.gml_file_exists(widget.text()):
                calc_file = {}
                calc_file['gml_fn'] = widget.text()
                related_widgets = self.get_related_data_widgets(widget)
                #print(related_widgets)
                calc_file['situation'] = related_widgets['combo_situation'].currentData()
                calc_file['year'] = related_widgets['combo_year'].currentData()
                #print(calc_file)
                result.append(calc_file)
        return result
