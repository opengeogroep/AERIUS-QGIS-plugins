# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImaerWriterDialog
                                 A QGIS plugin
 Export gml conform to the imaer schema to use in AERIUS calculator
                             -------------------
        begin                : 2015-05-28
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

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ImaerWriter_dialog_base.ui'))


class ImaerWriterDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ImaerWriterDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
