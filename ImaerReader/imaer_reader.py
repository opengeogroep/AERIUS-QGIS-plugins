# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImaerReader
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
from PyQt4.QtCore import *
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QDialogButtonBox
from qgis.core import *
from qgis.utils import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialogs
from imaer_reader_dialog import ImaerReaderDialog
from progress_dialog import ProgressDialog

import imaerread as IR

import os.path
import time

class ImaerReader:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        #self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ImaerReader_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ImaerReaderDialog()

        # add some necessary signal and slot communication as well as disable the save button for now              
        self.dlg.cancel_open_button_box.button(QDialogButtonBox.Open).setEnabled(False)
        QObject.connect(self.dlg.fileBrowseButton, SIGNAL("clicked()"), self.chooseFile)
        QObject.connect(self.dlg.gmlFileNameBox, SIGNAL("textChanged(QString)"), self.gmlFileNameBoxChanged)
        QObject.connect(self.dlg.help_pushButton, SIGNAL("clicked()"), self.showHelp)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&ImaerReader')
        self.toolbar = self.iface.addToolBar(u'ImaerReader')
        self.toolbar.setObjectName(u'ImaerReader')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ImaerReader', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ImaerReader/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Import imaer gml'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&ImaerReader'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

    def log(self, msg):
        QgsMessageLog.logMessage(str(msg), 'ImaerReader', QgsMessageLog.INFO)


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        if result:
           
            t0 = time.time()
            #self.progress = ProgressDialog()
            #self.progress.show()
            #self.progress.progressBar.maximum = 0
            #self.progress.progressBar.value = 0
            self.featureCount = 0
            #self.updateFeatureCounter()
            
            featureCollection = IR.ImaerRead(gmlFile = self.dlg.gmlFileNameBox.text())
            self.attributes = featureCollection.AttributeFields
            
            self.doPoint = self.dlg.point_checkBox.checkState()
            self.doHexagon = self.dlg.hexagon_checkBox.checkState()
            
            #create layers
            if self.doPoint:
                (self.pointLayer, self.pointProvider) = self.createLayer(dim=0, name="Depositie rekenpunt")
            if self.doHexagon:
                (self.hexagonLayer, self.hexagonProvider) = self.createLayer(dim=2, name="Depositie hexagoon")

            # create features
            ft = featureCollection.nextFeature(doPoints=self.doPoint, doHexagons=self.doHexagon)
            while ft:
                self.featureCount += 1
                #self.updateFeatureCounter()
                if self.doPoint:
                    feat = self.getFeature(ft, dim=0)
                    self.pointProvider.addFeatures([feat])
                if self.doHexagon:
                    feat = self.getFeature(ft, dim=2)
                    self.hexagonProvider.addFeatures([feat])
        
                ft = featureCollection.nextFeature()
            
            #self.progress.progressBar.maximum = 100
            #self.progress.progressBar.value = 100
            #self.updateFeatureCounter()
            
            # add layers to map
            canvas = iface.mapCanvas()
            if self.doHexagon:
                #hexagonQml = os.path.join(self.plugin_dir,'imaer_hexagon.qml')
                #self.hexagonLayer.loadNamedStyle(hexagonQml)
                self.hexagonLayer.updateExtents()
                QgsMapLayerRegistry.instance().addMapLayer(self.hexagonLayer)
                canvas.setExtent(self.hexagonLayer.extent())
            if self.doPoint:
                # TODO: create some point style too
                #self.pointLayer.loadNamedStyle()
                self.pointLayer.updateExtents()
                QgsMapLayerRegistry.instance().addMapLayer(self.pointLayer)
                if not self.doHexagon:
                    canvas.setExtent(self.pointLayer.extent())

            self.log('import time: ' + str(time.time() - t0) + ' sec')
                
    def getFeature(self, ft, dim=2):
        """Creates a QGIS feature from a feature returned by the imaerread parser

        :param ft: feature returned by the imaerread parser
        :type ft: dict

        :param dim: dimension of the geometry
        :type dim: int
        """
        feat = QgsFeature()
        if dim == 2:
            feat.setGeometry(QgsGeometry.fromWkt(ft['hexagon']))
        else:
            feat.setGeometry(QgsGeometry.fromWkt(ft['point']))
        featureAttributes = [ft['id']]
        for attr in self.attributes:
            try:
                featureAttributes.append(ft[attr])
            except:
                featureAttributes.append(None)
        #self.log(str(featureAttributes))
        feat.setAttributes(featureAttributes)
        return feat
        

    def createLayer(self, dim=2, name="imaer layer"):
        """Creates a map layer of polygon (2) or point (0) type, and returns both the layer and the provider as a tuple.

        :param dim: dimension of the geometry
        :type dim: int

        :param name: layer name (defaults to 'imaer layer'
        :type ft: str
        """
        # create layer
        if dim == 2:
            vl = QgsVectorLayer("Polygon?crs=EPSG:28992", name, "memory")
        else:
            vl = QgsVectorLayer("Point?crs=EPSG:28992", name, "memory")
        pr = vl.dataProvider()
        
        # add fields
        pr.addAttributes([QgsField("id", QVariant.String)])
        for subst in self.attributes:
            pr.addAttributes([QgsField(subst, QVariant.Double)])
        vl.updateFields()
        return (vl,pr)
        
    def updateFeatureCounter(self):
        """Updates the feature count in the progress dialog."""
        self.progress.feature_count_label.setText(str(self.featureCount))
        self.log(self.featureCount)
    
    def chooseFile(self):
        """Opens the file dialog to pick a file to open"""
        fileName = QFileDialog.getOpenFileName(caption = "Open gml File", directory = '', filter = '*.gml')
        self.dlg.gmlFileNameBox.setText(fileName)
        
    def gmlFileNameBoxChanged(self, fileName):
        """Enables the OK button after entering a file name"""
        if os.path.exists(os.path.dirname(fileName)):
            self.dlg.cancel_open_button_box.button(QDialogButtonBox.Open).setEnabled(True)
    
    def showHelp(self):
        """Reacts on help button"""
        showPluginHelp(filename = 'help/build/html/index')    
        
