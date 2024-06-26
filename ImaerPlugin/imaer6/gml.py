from PyQt5.QtXml import QDomDocument

from qgis.core import QgsOgcUtils


def get_gml_element(geom, gml_id_base, epsg_id):
    doc = QDomDocument()
    ogc_utils = QgsOgcUtils()
    version = QgsOgcUtils.GML_3_2_1
    srs_name = f'urn:ogc:def:crs:EPSG::{epsg_id}'

    gml_geom = ogc_utils.geometryToGML(
        geometry=geom,
        doc=doc,
        gmlVersion=QgsOgcUtils.GML_3_2_1,
        srsName=srs_name,
        invertAxisOrientation=False,
        gmlIdBase=gml_id_base,
        precision=3
    )

    return gml_geom
