from PyQt5.QtXml import QDomDocument

from qgis.core import QgsOgcUtils



def get_gml_element(geom, gml_id_base, epsg_id=28992):
    doc = QDomDocument()
    ogc_utils = QgsOgcUtils()
    version = QgsOgcUtils.GML_3_2_1
    srs_name = f'urn:ogc:def:crs:EPSG::{epsg_id}'

    gml_geom = ogc_utils.geometryToGML(geometry=geom,
        doc=doc,
        gmlVersion=QgsOgcUtils.GML_3_2_1,
        srsName=srs_name,
        invertAxisOrientation=False,
        gmlIdBase=gml_id_base,
        precision=3)

    geom_type = gml_geom.tagName()
    if geom_type.startswith('gml:'):
        geom_type = geom_type[4:]
    print(geom_type)

    print(doc.toString())

    return doc
