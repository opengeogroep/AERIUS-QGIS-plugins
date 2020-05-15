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

from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from qgis.core import QgsMessageLog, Qgis




class ImaerPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.do_log = True
        #self.log('init')


    def initGui(self):
        self.toolbar = self.iface.addToolBar("Imaer Toolbar")

        reader_icon = QIcon(os.path.join(self.plugin_dir, 'icon_reader.png'))
        self.reader_action = QAction(reader_icon, 'Import IMAER result', self.iface.mainWindow())
        self.reader_action.triggered.connect(self.run)
        self.toolbar.addAction(self.reader_action)

        #self.log('initGui')


    def unload(self):
        self.reader_action.triggered.disconnect(self.run)
        self.toolbar.removeAction(self.reader_action)
        del self.reader_action
        del self.toolbar

        #self.log('unload')


    def run(self):
        self.log('Print this in the Imaer tab')


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)
