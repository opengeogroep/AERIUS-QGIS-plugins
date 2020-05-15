# -*- coding: utf-8 -*-
'''
/***************************************************************************
 A QGIS plugin for generating AERIUS Calculator input IMAER files and
 importing AERIUS Calculator output IMAER files.
                             -------------------
        begin                : 2020-05-08
        git sha              : $Format:%H$
        copyright            : (C) 2020 by OpenGeoGroep
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
'''

from PyQt5.QtWidgets import QAction, QMessageBox

def classFactory(iface):
    return ImaerPlugin(iface)




class ImaerPlugin:
    def __init__(self, iface):
        self.iface = iface


    def initGui(self):
        self.action = QAction('Go!', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)


    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action


    def run(self):
        QMessageBox.information(None, 'Imaer plugin', 'Do something useful here')
