# -*- coding: utf-8 -*-
################################################################################
#
# begin:      2020-05-08
# copyright:  (C) 2020 by OpenGeoGroep
# email:      info@opengeogroep.nl

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
################################################################################

import os

from PyQt5.QtWidgets import QAction, QFileDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon

from qgis.core import QgsMessageLog, Qgis

from .imaer_reader_dialog import ImaerReaderDialog




class ImaerPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.do_log = True
        #self.log('init')


    def initGui(self):
        self.toolbar = self.iface.addToolBar("Imaer Toolbar")

        self.reader_dlg = ImaerReaderDialog()

        reader_icon = QIcon(os.path.join(self.plugin_dir, 'icon_reader.png'))
        self.reader_action = QAction(reader_icon, 'Import IMAER result', self.iface.mainWindow())
        self.reader_action.triggered.connect(self.run)
        self.toolbar.addAction(self.reader_action)

        self.reader_dlg.fileBrowseButton.clicked.connect(self.chooseFile)
        self.reader_dlg.gmlFileNameBox.textChanged.connect(self.gmlFileNameBoxChanged)

        #self.log('initGui')


    def unload(self):
        self.reader_action.triggered.disconnect(self.run)
        self.toolbar.removeAction(self.reader_action)
        del self.reader_action
        del self.toolbar

        self.reader_dlg.fileBrowseButton.clicked.disconnect(self.chooseFile)
        self.reader_dlg.gmlFileNameBox.textChanged.disconnect(self.gmlFileNameBoxChanged)

        #self.log('unload')


    def run(self):
        self.reader_dlg.show()
        result = self.reader_dlg.exec_()
        self.log(result)


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def chooseFile(self):
        """Opens the file dialog to pick a file to open"""
        filename, filter = QFileDialog.getOpenFileName(caption = "Open IMAER gml File", filter = '*.gml')
        self.reader_dlg.gmlFileNameBox.setText(filename)


    def gmlFileNameBoxChanged(self):
        """Enables the OK button after entering a file name"""
        filename = self.reader_dlg.gmlFileNameBox.text()
        enable_open = os.path.exists(os.path.dirname(filename))
        self.reader_dlg.cancel_open_button_box.button(QDialogButtonBox.Open).setEnabled(enable_open)
