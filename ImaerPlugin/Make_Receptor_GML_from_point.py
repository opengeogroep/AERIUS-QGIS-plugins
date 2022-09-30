# -*- coding: utf-8 -*-
import os
import time
import json

from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QSizePolicy
)
from qgis.PyQt import uic

from qgis.utils import iface
from qgis.gui import (
    QgsMapLayerComboBox,
    QgsFieldComboBox
)
from qgis.core import (
    QgsMapLayerProxyModel,
    QgsProject,
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform
)

from ImaerPlugin.config import (
    emission_sectors,
    ui_settings
)

from ImaerPlugin.imaer4 import (
    ImaerDocument,
    AeriusCalculatorMetadata,
    EmissionSourceType,
    EmissionSourceCharacteristics,
    EmissionSource,
    SpecifiedHeatContent,
    Emission,
    SRM2Road,
    RoadSideBarrier,
    StandardVehicle,
    ReceptorGMLType, 
    Receptor
)



FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'Make_Receptor_GML_from_point_dlg.ui'))


class GenerateReceptorGMLDialog(QDialog, FORM_CLASS):
    def __init__(self, plugin, parent=None):
        """Constructor."""
        super(GenerateReceptorGMLDialog, self).__init__(parent)

        self.setupUi(self)
        self.iface = iface
        self.plugin = plugin

        self.init_gui()


    def init_gui(self):
        # Add message bar

        self.combo_layer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        self.edit_outfile.textChanged.connect(self.update_ok_button)

        self.combo_layer.layerChanged.connect(self.update_field_combos)
        self.button_outfile.clicked.connect(self.browse_generate_calc_input_file)

        self.btn_save_settings.clicked.connect(self.save_settings)
        self.btn_load_settings.clicked.connect(self.load_settings)

        for fcb in self.findChildren(QgsFieldComboBox):
            fcb.setAllowEmptyFieldName(True)

        #self.set_fixed_options()
        self.update_field_combos()
        self.update_ok_button()
        self.set_emission_tab()


    def __del__(self):
        self.edit_outfile.textChanged.disconnect(self.update_ok_button)
        self.combo_sector.currentIndexChanged.disconnect(self.set_emission_tab)
        self.combo_layer.layerChanged.disconnect(self.update_field_combos)
        self.button_outfile.clicked.disconnect(self.browse_generate_calc_input_file)

        self.btn_save_settings.clicked.disconnect(self.save_settings)
        self.btn_load_settings.clicked.disconnect(self.load_settings)


    def browse_generate_calc_input_file(self):
        
        out_path = ''
        out_fn = time.strftime("calcinput_%Y%m%d_%H%M%S.gml")
        out_fn = os.path.join(out_path, out_fn)

        gml_outfn, filter = self.plugin.calc_input_file_dialog.getSaveFileName(caption="Save as receptor gml file", filter='*.gml', directory=out_fn, parent=self.iface.mainWindow())
        self.edit_outfile.setText(gml_outfn)


    '''
    def set_fixed_options(self):
        # crs
        for crs in ui_settings['crs']:
            self.combo_crs.addItem(crs['name'], crs['srid'])

        # sectors
        self.combo_sector.addItem('<Select sector>', 0)
        for sector_name in emission_sectors:
            ##print(sector_name)
            self.combo_sector.addItem(sector_name)

        # project
        for item in ui_settings['project_years']:
            self.combo_project_year.addItem(item, item)
        self.combo_project_year.setCurrentText(ui_settings['project_default_year'])

        # situation
        self.edit_situation_name.setText(ui_settings['situation_name'])
        for item in ui_settings['situation_types']:
            self.combo_situation_type.addItem(item, item)
    '''

    '''
    def set_emission_tab(self):
        # Remove all tabs but 'Metadata'
        while self.tabWidget.count() > 1:
            self.tabWidget.removeTab(1)
        # Add selected emission tab
        sector = self.combo_sector.currentText()
        if sector in self.emission_tabs:
            self.tabWidget.insertTab(1, self.emission_tabs[sector], sector)
            self.tabWidget.setCurrentIndex(1)
    '''

    def update_field_combos(self):
        for fcb in self.findChildren(QgsFieldComboBox):
            fcb.setLayer(self.combo_layer.currentLayer())


    def update_ok_button(self):
        if self.edit_outfile.text() == '':
            self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
            return
        ##if self.get_current_sector_id() == 0:
        ##    self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
        ##    return
        self.buttonBox.button(QDialogButtonBox.Save).setEnabled(True)


        def Nicolas_function(self):
            #
            #This function aims to take a shapefile of points and convert this to a gml file ready to load into AERIUS
            #name can be udpated later
            #

            '''
            # open a popup box and let the user select the shapefile to be converted
            shp_fn, filter = self.nicolas_function_dialog.getOpenFileName(caption="Open a point shp file ", filter='*.shp', parent=self.iface.mainWindow())
            self.log(f'run shp: {shp_fn}', user='dev')

            # load the shapefile in QGIS
            if os.path.exists(shp_fn):
                name_of_file = os.path.basename(shp_fn)[:-4]
                eq_layer=QgsVectorLayer(shp_fn,name_of_file,"ogr")
                QgsProject.instance().addMapLayer(eq_layer)
            else:
                self.log("Unable to read the shp at the path provided")
                return
            '''
            
            # get the generic gml file loaded
            imaer_doc = ImaerDocument()
            
            # setup metadata (not sure this is needed for a receptor file, using hard coded values for now)
            year = 2022 # hardcoded this just now, not sure it matters for the receptor file
            description = "na" # not sure this matters for the receptor file
            situation = "na" # not sure this matters for the receptor file
            
            metadata = AeriusCalculatorMetadata(
                project = {'year': year, 'description': description},
                situation = situation,
            )

            # add metadata to imaer document
            imaer_doc.metadata = metadata

            input_layer = self.combo_layer.currentLayer()
            crs_source = input_layer.crs()
            crs_dest_srid = self.combo_crs.currentData()
            crs_dest = QgsCoordinateReferenceSystem(crs_dest_srid)
            if crs_source == crs_dest:
                crs_transform = None
            else:
                crs_transform = QgsCoordinateTransform(crs_source, crs_dest, QgsProject.instance())

            # now to add receptor data
            # Loop all features
            
            for feat in input_layer.getFeatures():
                self.log("Starting new feature", user='dev')
                local_id = 'CP.{}'.format(feat.id())

                # geometry
                geom = feat.geometry()

                geom2 = self.generate_calc_input_dlg.make_single_part(geom)
                
                if geom2 is None:
                    self.plugin.log(f'Input data contains multipart geometry: {geom.asWkt(precision=3)}', bar=True, lvl='Critical')
                    return
                geom = geom2

                if crs_transform is not None:
                    geom.transform(crs_transform)

                # this is where need new function to write the receptor part of the gml file
                es = self.get_receptor_source_gml(feat, geom, local_id)
                
                imaer_doc.feature_members.append(es)

            return imaer_doc


    def get_receptor_source_gml(self, feat, geom, local_id):
        ''' 
        funciton to make gml parts for receports
        '''
        
        es = Receptor(local_id=local_id, geom=geom)

        return es

        '''
        from PyQt5.QtXml import QDomDocument        
        
        doc = QDomDocument()
        result = doc.createElement('imaer:CalculationPoint')
        result.setAttribute('gml:id', str("CP.{}".format(str(local_id))))
        doc.appendChild(result)

        # identifier
        ident_elem = doc.createElement('imaer:identifier')
        nen_elem = doc.createElement('imaer:NEN3610ID')

        elem = doc.createElement('imaer:namespace')
        elem.appendChild(doc.createTextNode('NL.IMAER'))
        nen_elem.appendChild(elem)

        elem = doc.createElement('imaer:localId')
        elem.appendChild(doc.createTextNode(str("CP."+ str(local_id))))

        nen_elem.appendChild(elem)
        ident_elem.appendChild(nen_elem)
        result.appendChild(ident_elem)


        # now move to the point data
        # this isn't quite right as the gml:Point is the element but with a bit of a string
        ident_elem = doc.createElement('imaer:GM_Point')
        epsg_id = 28992 ##### HARD CODED JUST NOW
        nen_elem = doc.createElement(str('gml:Point srsName="urn:ogc:def:crs:EPSG::'+str(epsg_id)+'" gml:id="CP.' + str(local_id) +'.POINT"'))
        # the above should use the get_gml_elem function from gml.py to get the string I need I think (but relies on having actual geom)
        # come back to this later when have an actual gml being written out
        elem = doc.createElement('gml:pos')
        elem.appendChild(doc.createTextNode(str(geom)))
        nen_elem.appendChild(elem)

        ident_elem.appendChild(nen_elem)
        result.appendChild(ident_elem)

        # add a label
        ident_elem = doc.createElement('imaer:label')
        ident_elem.appendChild(doc.createTextNode('Assessment point {}'.format(str(local_id))))
        result.appendChild(ident_elem)

        return result
        '''
    def make_single_part(self, geom):
        '''Returns single part geometry or None if input has more than 1 part'''
        parts = geom.asGeometryCollection()
        if len(parts) == 1:
            result = parts[0]
            # Make sure the type is Point, LineString or Polygon
            if result.wkbType() in [1, 2, 3]:
                return result
        return None