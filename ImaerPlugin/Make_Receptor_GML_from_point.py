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
    StandardVehicle
)

'''
def Nicolas_function(self):
        #
        #This function aims to take a shapefile of points and convert this to a gml file ready to load into AERIUS
        #name can be udpated later
        #

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
        
        
        # Now need to get info about e.g. geometry to be able to add to the gml file
        from ImaerPlugin.imaer4 import (ImaerDocument,AeriusCalculatorMetadata)

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

        # now to add receptor data
        # Loop all features
        
        for feat in eq_layer.getFeatures():
            self.log("Starting new feature", user='dev')
            local_id = 'CP.{}'.format(feat.id())

            # geometry
            geom = feat.geometry()

            geom2 = self.generate_calc_input_dlg.make_single_part(geom)
            
            if geom2 is None:
                self.plugin.log(f'Input data contains multipart geometry: {geom.asWkt(precision=3)}', bar=True, lvl='Critical')
                return
            geom = geom2

            # this is where need new function to write the receptor part of the gml file
            es = self.get_receptor_source_gml(feat, geom, local_id)
            
            imaer_doc.feature_members.append(es)

        
        if imaer_doc is None: # Something went wrong during IMAER doc generation...
                self.log('Something went wrong during IMAER doc generation.')
                return
        
        # this where the file is saved - figure out where saving is occuring (what folder, file name etc)       
        fn = os.path.join(os.path.dirname(shp_fn),str(name_of_file + ".gml"))  

        imaer_doc.to_xml_file(fn)

        self.log('Imaer GML file saved as: <a href="{0}">{0}</a>'.format(fn), lvl='Info', bar=True, duration=10)
'''        
'''
    def get_receptor_source_gml(self, feat, geom, local_id):
        # 
        funciton to make gml parts for receports
        # 
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