# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IMAERwriter
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
# Import debugger
# import pdb

import os.path
import xml.dom.minidom

import processing
from PyQt4.QtCore import *
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import *
from PyQt4.QtGui import QAction, QIcon

import qgis
from qgis.core import *

# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from ImaerWriter_dialog import ImaerWriterDialog

import imaerwrite as imaer

class ImaerWriter:
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
        self.plugin_dir = os.path.dirname(os.path.abspath(__file__))
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ImaerWriter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ImaerWriterDialog()
        
        # add some necessary signal and slot communication as well as disable the save button for now              
        self.dlg.cancel_save_button_box.button(QDialogButtonBox.Save).setEnabled(False)
        QObject.connect(self.dlg.fileBrowseButton, SIGNAL("clicked()"), self.chooseFile)
        QObject.connect(self.dlg.gmlFileNameBox, SIGNAL("textChanged(QString)"), self.gmlFileNameBoxChanged)
        QObject.connect(self.dlg.helpButton, SIGNAL("clicked()"), self.showHelp)
        #QObject.connect(self.dlg.point_oggLogo, SIGNAL("clicked()"), self.showOGG)
        #QObject.connect(self.dlg.line_oggLogo, SIGNAL("clicked()"), self.showOGG)
        #QObject.connect(self.dlg.polygon_oggLogo, SIGNAL("clicked()"), self.showOGG)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&IMAERwriter')
        self.toolbar = self.iface.addToolBar(u'IMAERwriter')
        self.toolbar.setObjectName(u'IMAERwriter')
        
        self.imaerInstance = imaer.ImaerWrite()
        self.uiFeatureTypes = ['point','line','polygon']
        self.qElements = {}
        
        ### update and add UI elements from object properties ###
        # first generic ui-elements        
        self.emissionSourceTypes = self.imaerInstance.EmissionSourceTypes
        for uiFT in self.uiFeatureTypes:
            self.qElements['%sSourceTypeCombo' % uiFT] = getattr(self.dlg,'%sSourceTypeCombo' % uiFT)
            self.qElements['%sSourceTypeCombo' % uiFT].addItems(self.emissionSourceTypes)
            self.qElements['%sSourceTypeCombo' % uiFT].addItem('from column: source')
            QObject.connect(self.qElements['%sSourceTypeCombo' % uiFT],SIGNAL("currentIndexChanged(QString)"), getattr(self, 'update_%sEmissionSource' % uiFT))
            QObject.connect(getattr(self.dlg, '%sDataCombo' % uiFT), SIGNAL("currentIndexChanged(QString)"), getattr(self, 'update_%sUIelements' % uiFT))
            QObject.connect(getattr(self.dlg, '%sEmissionSourceCharacteristicsCheckBox' % uiFT), SIGNAL("stateChanged(int)"), getattr(self, 'update_%sEmissionSourceCharacteristicsUIelements' % uiFT))
            getattr(self.dlg, '%sEmissionSourceCharacteristicsCheckBox' % uiFT).setEnabled(True)
            
        uiFieldDef = self.imaerInstance.getUiFields(emissionSourceType = False, emissionSourceCharacteristics = False)                      # gets the generic uiFields
        uiFieldDef.update(self.imaerInstance.getUiFields(emissionSourceType = False, emissionSourceCharacteristics = True))                 # and the emissionSourceCharacteristics as well
        for uiFT in self.uiFeatureTypes:
            for objectName, fields in uiFieldDef.items():
                for field in fields[0] + fields[1]:
                    self.qElements['%s_%s_%s_combo' % (objectName, uiFT, field) ] = QComboBox()
                    layout = getattr(self.dlg, '%s%sLayout' % (uiFT, objectName) )
                    layout.addRow(field,self.qElements['%s_%s_%s_combo' % (objectName, uiFT, field) ])
            getattr(self.dlg, '%sEmissionWidget' % uiFT ).setVisible( True )
            getattr(self.dlg, '%sEmissionSourceCharacteristicsWidget' % uiFT ).setVisible( False )
            getattr(self.dlg, '%sGroupBox' % uiFT ).setVisible( False )
        
        # then for the supported emissionSourceTypes
        # add all fields to qElements and to widgets. Hide and show %s_%s_sourceWidget's as needed.
        for emissionSourceType in self.emissionSourceTypes:
            for uiFT in self.uiFeatureTypes:
                uiFieldDef = self.imaerInstance.getUiFields(emissionSourceType = emissionSourceType, emissionSourceCharacteristics = False ) # gets the uiFields for the specific emissionSourceType
                self.qElements['%s_%s_sourceWidget' % (uiFT,emissionSourceType) ] = QWidget()
                self.qElements['%s_%s_sourceWidget' % (uiFT,emissionSourceType) ].setVisible(False)
                getattr(self.dlg,'%sSourceContainerLayout' % uiFT).addWidget(self.qElements['%s_%s_sourceWidget' % (uiFT,emissionSourceType) ])
                self.qElements['%s_%s_formLayout' % (uiFT,emissionSourceType) ] = QFormLayout()
                self.qElements['%s_%s_sourceWidget' % (uiFT,emissionSourceType) ].setLayout(self.qElements['%s_%s_formLayout' % (uiFT,emissionSourceType) ])
                for objectName, fields in uiFieldDef.items():
                    for field in fields[0] + fields[1]:
                        self.qElements['%s_%s_%s_combo' % (objectName, uiFT, field) ] = QComboBox()
                        self.qElements['%s_%s_formLayout' % (uiFT,emissionSourceType) ].addRow(field,self.qElements['%s_%s_%s_combo' % (objectName, uiFT, field) ])
                        
                        
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
        return QCoreApplication.translate('ImaerWriter', message)


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

        icon_path = ':/plugins/ImaerWriter/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Export IMAER gml'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&IMAERwriter'),
                action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar
        
    def log(self, msg):
        QgsMessageLog.logMessage(str(msg), 'IMAERwriter', QgsMessageLog.INFO)

    def transformGeometry(self, geom, coordTrans):
        """helper function to transform geometries"""
        for i in range(geom.exportToWkt().count(',')):
          vertex = coordTrans.transform(geom.vertexAt(i))
          geom.moveVertex(vertex.x(), vertex.y(), i)
        
    def run(self):
        """Run method that does all the real work"""
             
        #Add layers to the layer selectors
        layers = QgsMapLayerRegistry.instance().mapLayers()
        
        for uiFT in self.uiFeatureTypes:
            getattr(self.dlg, '%sDataCombo' % uiFT).clear()
            getattr(self.dlg, '%sDataCombo' % uiFT).addItem('')                 # so the user can choose no layer if he wants
        
        for name,layer in layers.iteritems():
            if type(layer) == QgsVectorLayer:
                if layer.geometryType() == QGis.Point:
                    self.dlg.pointDataCombo.addItem(layer.name())
                if layer.geometryType() == QGis.Line:
                    self.dlg.lineDataCombo.addItem(layer.name())
                if layer.geometryType() == QGis.Polygon:
                    self.dlg.polygonDataCombo.addItem(layer.name())
        
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            #QgsMessageLog.logMessage('Started export', 'IMAER-writer', QgsMessageLog.INFO)
            self.imaerFeatures = []
            crsDest = QgsCoordinateReferenceSystem(28992, QgsCoordinateReferenceSystem.EpsgCrsId )
            
            for uiFT in self.uiFeatureTypes:
                layerName = getattr(self.dlg, '%sDataCombo' % uiFT ).currentText()
                if not layerName == '':
                    myLayer = QgsMapLayerRegistry.instance().mapLayersByName(layerName)[0]
                    # set up transformation to EPSG:28992 if needed
                    crsSrc = myLayer.crs()
                    if not crsSrc == crsDest:
                        xform = QgsCoordinateTransform(crsSrc, crsDest)
                    else:
                        xform = False
                    
                    # use only selected features
                    numFeatures = myLayer.selectedFeatureCount ()
                    if numFeatures == 0:
                        features = myLayer.getFeatures()
                        numFeatures = myLayer.featureCount()
                    else:
                        features = myLayer.selectedFeatures()
                    
                    # get the fieldnames from the layer to use in the mapping
                    myProvider = myLayer.dataProvider()
                    fieldNames = myProvider.fieldNameMap().keys()  
                    
                    # get the Imaer fields to use in the mapping
                    sourceType = self.qElements['%sSourceTypeCombo' % uiFT].currentText()
                    if sourceType == 'from column: source':
                        uiFieldDef = []
                    else:
                        uiFieldDef = self.imaerInstance.getUiFields(emissionSourceType = sourceType, 
                            emissionSourceCharacteristics = (getattr(self.dlg, '%sEmissionSourceCharacteristicsCheckBox' % uiFT).isChecked()) )
                        uiFieldDef.update(self.imaerInstance.getUiFields(False, False))
                    
                    # set up progress bar in case we have a lot of features
                    self.iface.mainWindow().statusBar().clearMessage()  
                    progressMessageBar = self.iface.messageBar().createMessage(self.tr(u"Export to gml ..."))
                    progress = QProgressBar()
                    progress.setMaximum(numFeatures)
                    progress.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
                    progressMessageBar.layout().addWidget(progress)
                    self.iface.messageBar().pushWidget(progressMessageBar, self.iface.messageBar().INFO)  
                    
                    for i, feature in enumerate(features):
                        progress.setValue(i)
                        percentageDone = i / float(numFeatures) * 100
                                                
                        # first handle geometry
                        geom = feature.geometry()
                        if xform:
                            self.transformGeometry(geom, xform)
                        
                        if (not geom.isMultipart()) and geom.isGeosValid():     
                            # then gather arguments  for EmissionSourceCharacteristics and EmissionSource object
                            # by mapping the layer fields to imaer properties
                            args = {}
                            if sourceType == 'from column: source':
                                sourceType = feature['source']
                                uiFieldDef = self.imaerInstance.getUiFields(sourceType, emissionSourceCharacteristics = True)
                                uiFieldDef.update(self.imaerInstance.getUiFields(False, False))
                                
                            for objectName, fields in uiFieldDef.items():
                                args[objectName] = {}
                                for field in fields[0] + fields[1]:                                     #required + optional fields
                                    if sourceType == 'from column: source':
                                        attrFieldName = field
                                    else:
                                        attrFieldName = self.qElements['%s_%s_%s_combo' % (objectName, uiFT, field) ].currentText()
                                    if not attrFieldName == '':
                                        args[objectName][field] = feature[attrFieldName]
                            
                            args[sourceType]['wktGeometry'] = geom.exportToWkt(3)
                            
                            try:     
                                # create the objects    
                                if 'EmissionSourceCharacteristics' in args and len(args['EmissionSourceCharacteristics']) > 0:               
                                #if 'EmissionSourceCharacteristics' in args:               
                                    args[sourceType]['emissionSourceCharacteristics'] = imaer.EmissionSource.EmissionSourceCharacteristics(**args['EmissionSourceCharacteristics'])
                                e  = imaer.EmissionSource(**args[sourceType])
                                # and add emissions to the source
                                for k,v in args['Emission'].items():
                                    e.addEmission(imaer.EmissionSource.Emission(k,v))
                                # and append to the list with features    
                                self.imaerFeatures.append(e)
                            except Exception as e:
                                self.iface.messageBar().pushMessage( self.tr(u"Warning"), self.tr(u"Skipped feature with gmlId: '%s' from layer '%s' with error: '%s'. " %(args[sourceType]['gmlId'],layerName,e)),1)
                        else:
                            self.iface.messageBar().pushMessage( self.tr(u"Warning"), self.tr(u"Skipped feature with gmlId: '%s' from layer '%s' with error: '%s'. " %(args[sourceType]['gmlId'],layerName,self.tr(u"invalid geometry"))),1)
                    
                    try:
                         # finally instantiate 
                        i = imaer.ImaerWrite(features = self.imaerFeatures)
                    except Exception as e:
                        self.iface.messageBar().pushMessage( self.tr(u"Error"), self.tr(u"Could not create gml with error: '%s'. " %e ) ,2)
                        return
                    
                    try:
                        #and save
                        i.save(self.dlg.gmlFileNameBox.displayText())
                    except Exception as e:
                        self.iface.messageBar().pushMessage( self.tr(u"Error"), self.tr(u"Could not create or save gml with error: '%s'. " %e ) ,2)
                        return
                    
                    progress.setValue(numFeatures)
                    
    ####################################################################################################
    ### routines to react on buttons and selections to show and hide widgets and populate comboboxes ###
    ####################################################################################################
    
    def update_pointEmissionSource(self, sourceType):
        """Reacts on choosing Emission Source Type"""
        self.update_Emission(uiFT = 'point')
        
    def update_lineEmissionSource(self, sourceType):
        """Reacts on choosing Emission Source Type"""
        self.update_Emission(uiFT = 'line')
        
    def update_polygonEmissionSource(self, sourceType):
        """Reacts on choosing Emission Source Type"""
        self.update_Emission(uiFT = 'polygon')
        
    def update_Emission(self, uiFT):
        """update the Emission Source Properties and Emission and adapt visibility of the GroupBox"""
        sourceType = self.qElements['%sSourceTypeCombo' % uiFT].currentText()
        if sourceType == 'from column: source':
            uiFieldDef = False
        else:
            uiFieldDef = self.imaerInstance.getUiFields(emissionSourceType = sourceType, 
                            emissionSourceCharacteristics = (getattr(self.dlg, '%sEmissionSourceCharacteristicsCheckBox' % uiFT).isChecked()) )
            uiFieldDef.update(self.imaerInstance.getUiFields(False, False))
        self.updateColumnCombos(fieldNames = self.getFieldNames(uiFT), uiFieldDef = uiFieldDef, uiFeatureTypes = [uiFT])
        # set the right widgets visible for the sourceType
        for st in self.emissionSourceTypes:
            self.qElements['%s_%s_sourceWidget' % (uiFT, st)].setVisible( (not sourceType == 'from column: source') and st == sourceType )
        # and update visibility of the groupbox
        self.toggle_GroupBox(uiFT)
        
    def update_pointUIelements(self,layerName):
        """Reacts on choosing data source"""
        self.update_UIelements(uiFT = 'point')
        
    def update_lineUIelements(self,layerName):
        """Reacts on choosing data source"""
        self.update_UIelements(uiFT = 'line')
        
    def update_polygonUIelements(self,layerName):
        """Reacts on choosing data source"""
        self.update_UIelements(uiFT = 'polygon')
        
    def update_UIelements(self, uiFT):
        """updates the Emission Source Characteristics ui elements and the Emission ui elements"""
        self.update_EmissionSourceCharacteristicsUIelements(uiFT)
        self.update_Emission(uiFT)

    def update_EmissionSourceCharacteristicsUIelements(self, uiFT):
        """updates the comboboxes for EmissionSourceCharacteristics"""
        sourceType = self.qElements['%sSourceTypeCombo' % uiFT].currentText()
        if sourceType == 'from column: source':
            uiFieldDef = False
        else:
            uiFieldDef = self.imaerInstance.getUiFields(emissionSourceCharacteristics = True)
        self.updateColumnCombos(fieldNames = self.getFieldNames(uiFT), uiFieldDef = uiFieldDef, uiFeatureTypes = [uiFT])
        
    def update_pointEmissionSourceCharacteristicsUIelements(self, checked):
        """Reacts on choosing emission source characteristics checkbox"""
        self.toggle_EmissionSourceCharacteristicsWidget(uiFT = 'point')
        
    def update_lineEmissionSourceCharacteristicsUIelements(self, checked):
        """Reacts on choosing emission source characteristics checkbox"""
        self.toggle_EmissionSourceCharacteristicsWidget(uiFT = 'line')
        
    def update_polygonEmissionSourceCharacteristicsUIelements(self, checked):
        """Reacts on choosing emission source characteristics checkbox"""
        self.toggle_EmissionSourceCharacteristicsWidget(uiFT = 'polygon')
    
    def toggle_EmissionSourceCharacteristicsWidget(self, uiFT):
        """show/ hide the EmissionSourceCharacteristicsWidget containing the comboboxes for EmissionSourceCharacteristics"""
        getattr(self.dlg, '%sEmissionSourceCharacteristicsWidget' % uiFT ).setVisible(
            getattr(self.dlg, '%sEmissionSourceCharacteristicsCheckBox' % uiFT ).checkState() == Qt.Checked)
    
    def toggle_GroupBox(self, uiFT):
        """toggles the visibility of the groupbox based on datasource and emission source type settings"""
        layerName = getattr(self.dlg, '%sDataCombo' % uiFT ).currentText()
        sourceType = self.qElements['%sSourceTypeCombo' % uiFT].currentText()
        if sourceType == 'from column: source' or layerName == '':
            getattr(self.dlg, '%sGroupBox' % uiFT ).setVisible(False)
        else:
            getattr(self.dlg, '%sGroupBox' % uiFT ).setVisible(True)

    def getFieldNames(self, uiFT):
        """returns the fieldNames for the chosen layer"""
        layerName = getattr(self.dlg, '%sDataCombo' % uiFT ).currentText()
        if layerName == '':
            fieldNames = False
        else:
            layer = QgsMapLayerRegistry.instance().mapLayersByName(layerName)[0]
            fieldNames = layer.dataProvider().fieldNameMap().keys()
        return fieldNames
        
    def updateColumnCombos(self, fieldNames, uiFieldDef, uiFeatureTypes):
        """update comboboxes with fieldnames"""
        for uiFT in uiFeatureTypes:
            if uiFieldDef:
                for objectName, fields in uiFieldDef.items():
                    for field in fields[0] + fields[1]:
                        self.qElements['%s_%s_%s_combo' % (objectName, uiFT, field) ].clear()
                        if fieldNames:
                            if field in fields[1]:
                                #add empty item for optional field
                                self.qElements['%s_%s_%s_combo' % (objectName, uiFT, field) ].addItem('')
                            self.qElements['%s_%s_%s_combo' % (objectName, uiFT, field) ].addItems(fieldNames)

    def chooseFile(self):
        """Reacts on browse button"""
        fileName = QFileDialog.getSaveFileName(caption = self.tr(u"Save gml File"), directory = '', filter = '*.gml')
        self.dlg.gmlFileNameBox.setText(fileName)
        
    def gmlFileNameBoxChanged(self, fileName):
        """Reacts on a changed filename"""
        if os.path.exists(os.path.dirname(fileName)):
            self.dlg.cancel_save_button_box.button(QDialogButtonBox.Save).setEnabled(True)
            
    def showHelp(self):
        """Reacts on help button"""
        qgis.utils.showPluginHelp(filename = 'help/index')
        
    def showOGG(self):
        """Shows ogg website on clicking the logo"""
        QDesktopServices.openUrl(QUrl('http://www.opengeogroep.nl'))
