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

#from .worker import Worker
from .imaer_tasks import ImaerResultToGpkgTask




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
        self.log('ImaerReaderDialog ready :)')


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def import_result_gml(self, gml_fn):
        task = ImaerResultToGpkgTask(gml_fn,'')
        self.log('import_result_task')
        self.log(task)
        QgsApplication.taskManager().addTask(task)
        self.log('added to task manager')
        
        #return task




    '''
    def workerFinished(self, ret):
        # clean up the worker and thread
        self.worker.deleteLater()
        self.thread.quit()
        self.thread.wait()
        self.thread.deleteLater()
        # remove widget from message bar
        self.iface.messageBar().popWidget(self.messageBar)
        if ret is not None:
            self.iface.messageBar().pushMessage('{cnt} features imported'.format(cnt=ret), duration=5)
        else:
            # notify the user that something went wrong
            self.iface.messageBar().pushMessage('Error! See the message log for more information.', level=Qgis.Critical, duration=5)
        self.workerEnd.emit()


    def workerError(self, e, exception_string):
        QgsMessageLog.logMessage('Worker thread raised an exception:\n'.format(exception_string), level=Qgis.Critical)


    def updateProgress(self, p):
        self.progressBar.setValue(p)
    '''

    # signal
    workerEnd = pyqtSignal()
