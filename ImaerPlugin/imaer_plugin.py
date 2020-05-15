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

from PyQt5.QtWidgets import QAction, QMessageBox
from PyQt5.QtGui import QIcon




class ImaerPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)


    def initGui(self):
        self.toolbar = self.iface.addToolBar("Imaer Toolbar")

        reader_icon = QIcon(os.path.join(self.plugin_dir, 'icon_reader.png'))
        reader_action = QAction(reader_icon, 'Import IMAER result', self.iface.mainWindow())
        reader_action.triggered.connect(self.run)
        self.toolbar.addAction(reader_action)


    def unload(self):
        reader_action.triggered.disconnect(self.run)
        self.toolbar.removeAction(reader_action)
        del self.reader_action
        del self.toolbar


    def run(self):
        QMessageBox.information(None, 'Imaer plugin', 'Do something useful here')
