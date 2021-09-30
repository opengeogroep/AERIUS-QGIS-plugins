# -*- coding: utf-8 -*-
import os

from qgis.PyQt.QtCore import (
    QVariant,
    QStandardPaths
)
from qgis.PyQt.QtWidgets import (
    QDialog,
    QFileDialog
)
from qgis.PyQt import uic


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'configuration_dlg.ui'))




class ConfigurationDialog(QDialog, FORM_CLASS):

    def __init__(self, plugin, parent=None):
        super(ConfigurationDialog, self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.iface = plugin.iface

        self.init_default_values()
        self.init_gui()

        # Load and save settings once to make sure everything is up to date.
        self.load_ui_from_settings()
        self.save_ui_to_settings()


    def init_gui(self):
        self.combo_connect_ver.addItems(self.plugin.aerius_connection.available_versions)
        self.file_dialog = QFileDialog()
        self.button_get_key.clicked.connect(self.get_api_key)
        self.button_browse_work_dir.clicked.connect(self.browse_work_dir)


    def init_default_values(self):
        work_dir_setting = self.plugin.settings.value('imaer_plugin/work_dir', defaultValue=None)
        if work_dir_setting is None:
            work_dir_setting = QStandardPaths.writableLocation(QStandardPaths.TempLocation)
            self.plugin.settings.setValue('imaer_plugin/work_dir', work_dir_setting)

        connect_base_url = self.plugin.settings.value('imaer_plugin/connect_base_url', defaultValue=None)
        if connect_base_url is None:
            default_base_url = self.plugin.aerius_connection.default_base_url
            self.plugin.settings.setValue('imaer_plugin/connect_base_url', default_base_url)
            default_version = self.plugin.aerius_connection.default_version
            self.plugin.settings.setValue('imaer_plugin/connect_version', default_version)


    def load_ui_from_settings(self):
        #print('load_ui_from_settings')

        work_dir_setting = self.plugin.settings.value('imaer_plugin/work_dir', defaultValue='')
        self.edit_work_dir.setText(work_dir_setting)

        connect_server_setting = self.plugin.settings.value('imaer_plugin/connect_base_url', defaultValue='')
        self.edit_connect_base_url.setText(connect_server_setting)

        connect_version_setting = self.plugin.settings.value('imaer_plugin/connect_version', defaultValue='')
        self.combo_connect_ver.setCurrentText(connect_version_setting)

        email_setting = self.plugin.settings.value('imaer_plugin/connect_email', defaultValue='')
        self.edit_email.setText(email_setting)

        key_setting = self.plugin.settings.value('imaer_plugin/connect_key', defaultValue='')
        self.edit_key.setText(key_setting)


    def save_ui_to_settings(self):
        self.plugin.settings.setValue('imaer_plugin/work_dir', self.edit_work_dir.text())
        self.plugin.settings.setValue('imaer_plugin/connect_base_url', self.edit_connect_base_url.text())
        self.plugin.settings.setValue('imaer_plugin/connect_version', self.combo_connect_ver.currentText())
        self.plugin.settings.setValue('imaer_plugin/connect_email', self.edit_email.text())
        self.plugin.settings.setValue('imaer_plugin/connect_key', self.edit_key.text())
        self.plugin.aerius_connection.base_url = self.edit_connect_base_url.text()
        self.plugin.aerius_connection.version = self.combo_connect_ver.currentText()
        self.plugin.aerius_connection.api_key = self.edit_key.text()
        self.plugin.aerius_connection.check_connection()


    def get_api_key(self):
        email = self.edit_email.text()
        result = self.plugin.aerius_connection.generate_api_key(email)
        if result:
            self.edit_key.setText('')
            self.plugin.settings.setValue('imaer_plugin/connect_key', '')
            self.plugin.log('Requested new Connect API key', bar=True)
        else:
            self.plugin.log('Requesting new Connect API key failed', lvl='Critical', bar=True)


    def browse_work_dir(self):
        current_work_dir = self.edit_work_dir.text()
        self.file_dialog.setDirectory(current_work_dir)
        new_dir = self.file_dialog.getExistingDirectory(caption="Select work directory", parent=self)
        #self.log(new_dir)
        self.edit_work_dir.setText(new_dir)
