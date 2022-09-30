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

        for fcb in self.findChildren(QgsFieldComboBox):
            fcb.setAllowEmptyFieldName(True)

        self.update_field_combos()
        self.update_ok_button()
        

    def __del__(self):
        self.edit_outfile.textChanged.disconnect(self.update_ok_button)
        self.combo_layer.layerChanged.disconnect(self.update_field_combos)
        self.button_outfile.clicked.disconnect(self.browse_generate_calc_input_file)


    def browse_generate_calc_input_file(self):
        
        out_path = ''
        out_fn = time.strftime("receptorGML_%Y%m%d_%H%M%S.gml")
        out_fn = os.path.join(out_path, out_fn)

        gml_outfn, filter = self.plugin.calc_input_file_dialog.getSaveFileName(caption="Save as receptor gml file", filter='*.gml', directory=out_fn, parent=self.iface.mainWindow())
        self.edit_outfile.setText(gml_outfn)


    def update_field_combos(self):
        for fcb in self.findChildren(QgsFieldComboBox):
            fcb.setLayer(self.combo_layer.currentLayer())
        
    def get_layer_list(self):
        '''Returns a list of selected deposition layers in the enabled comboBoxes'''
        result = []
        
        layerList = QgsProject.instance().mapLayers().values()
        for layer in layerList:
            
            if layer.wkbType() == 1:
                result.append(layer)

        return result

    def update_ok_button(self):
        pass
         
        '''
        if self.edit_outfile.text() == '':
            self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
            return
        ##if self.get_current_sector_id() == 0:
        ##    self.buttonBox.button(QDialogButtonBox.Save).setEnabled(False)
        ##    return
        self.buttonBox.button(QDialogButtonBox.Save).setEnabled(True)
        '''

    def Nicolas_function(self):
        #
        #This function aims to take a shapefile of points and convert this to a gml file ready to load into AERIUS
        #name can be udpated later
        #

        # get the generic gml file loaded
        imaer_doc = ImaerDocument()
        
        # setup metadata (not sure this is needed for a receptor file, using hard coded values for now)
        year = 2022 # hardcoded this just now, not sure it matters for the receptor file
        description = "na" # not sure this matters for the receptor file
        situation = {'name': 'receptors','type': 'PROPOSED'} # this is still needed else fails to load in aerius. Adding dummy data for testing (need to see if matters what is in this section)
        
        metadata = AeriusCalculatorMetadata(
            project = {'year': year, 'description': description},
            situation = situation,
        )

        # add metadata to imaer document
        imaer_doc.metadata = metadata

        input_layer = self.combo_layer.currentLayer()
        
        crs_source = input_layer.crs()
        crs_dest_srid = 'EPSG:28992' # HARDCODING FOR NOW 
        crs_dest = QgsCoordinateReferenceSystem(crs_dest_srid)
        if crs_source == crs_dest:
            crs_transform = None
        else:
            crs_transform = QgsCoordinateTransform(crs_source, crs_dest, QgsProject.instance())

        # now to add receptor data
        # Loop all features
        
        for feat in input_layer.getFeatures():
            #self.log("Starting new feature", user='dev')
            local_id = 'CP.{}'.format(feat.id())

            # geometry
            geom = feat.geometry()

            geom2 = self.make_single_part(geom)
            
            if geom2 is None:
                #self.plugin.log(f'Input data contains multipart geometry: {geom.asWkt(precision=3)}', bar=True, lvl='Critical')
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
        fcb = getattr(self, 'fcb_combo_layer')
        label = self.get_feature_value(fcb, feat)
        #es = Receptor(local_id=local_id, geom=geom)
        es = Receptor(local_id=local_id, geom=geom, label=label)

        return es

    def get_feature_value(self, widget, feat, cast_to=None):
        if not isinstance(widget, QgsFieldComboBox):
            return None
        field_name = widget.currentField()
        if field_name == '':
            return None
            #return widget_set['fixed'].text() TODO: return fixed value after data type check (or something..)
        else:
            value = feat[field_name]

        if isinstance(value, QVariant) and str(value) == 'NULL':
            return None

        if cast_to is not None:
            #if cast_to == 'double':
            #    return result.toDouble()
            if cast_to == 'float':
                if isinstance(result, float):
                    return
                if isInstance(result, QVariant):
                    result.toFloat()
            elif cast_to == 'integer':
                return result.toInt()
            elif cast_to == 'string':
                return result.toString()
        return value
        
    def make_single_part(self, geom):
        '''Returns single part geometry or None if input has more than 1 part'''
        parts = geom.asGeometryCollection()
        if len(parts) == 1:
            result = parts[0]
            # Make sure the type is Point, LineString or Polygon
            if result.wkbType() in [1, 2, 3]:
                return result
        return None