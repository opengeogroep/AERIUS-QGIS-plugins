# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImaerReaderDialog
                                 A QGIS plugin
 Import gml conform to the imaer schema output by the AERIUS calculator
                             -------------------
        begin                : 2015-06-24
        git sha              : $Format:%H$
        copyright            : (C) 2015 by OpenGeoGroep
        email                : info@opengeogroep.nl
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from qgis.core import Qgis, QgsMessageLog, QgsApplication
#from qgis.core import QgsMessageLog

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QDialog, QProgressBar, QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore

from qgis.utils import iface




FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'imaer_reader_dialog.ui'))


class ImaerReaderDialog(QDialog, FORM_CLASS):

    def __init__(self, parent=None):
        """Constructor."""
        super(ImaerReaderDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.iface = iface
        self.do_log = True
        #self.log('ImaerReaderDialog ready :)')


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)

    def load_layer(self, gpkg_filename):
        self.log('load_layer()')
