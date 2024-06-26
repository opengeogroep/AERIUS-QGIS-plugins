from PyQt5.QtXml import QDomDocument

# from .enumerations import OutflowDirectionType
from .gml import get_gml_element


class Building(object):

    def __init__(self, *, local_id, height, geom, epsg_id, label=None, diameter=None):
        self.local_id = local_id
        self.diameter = diameter
        self.height = height
        self.label = label
        self.geometry = geom
        self.epsg_id = epsg_id

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement(f'imaer:Building')

        result.setAttribute('gml:id', f'Building.{self.local_id}')

        # identifier
        ident_elem = doc.createElement('imaer:identifier')
        nen_elem = doc.createElement('imaer:NEN3610ID')

        elem = doc.createElement('imaer:namespace')
        elem.appendChild(doc.createTextNode('NL.IMAER'))
        nen_elem.appendChild(elem)
        elem = doc.createElement('imaer:localId')
        elem.appendChild(doc.createTextNode(f'Building.{self.local_id}'))
        nen_elem.appendChild(elem)

        ident_elem.appendChild(nen_elem)
        result.appendChild(ident_elem)

        # label
        if self.label is not None:
            elem = doc.createElement('imaer:label')
            elem.appendChild(doc.createTextNode(str(self.label)))
            result.appendChild(elem)

        # height
        elem = doc.createElement('imaer:height')
        elem.appendChild(doc.createTextNode(str(self.height)))
        result.appendChild(elem)

        # geometry
        geom_elem = doc.createElement('imaer:geometry')
        es_geom_elem = doc.createElement('imaer:BuildingGeometry')

        gm_tags = {0: 'GM_Point', 2: 'GM_Surface'}
        gm_tag = gm_tags[self.geometry.type()]
        gml_types = {0: 'POINT', 2: 'SURFACE'}
        gml_type = gml_types[self.geometry.type()]

        gm_elem = doc.createElement(f'imaer:{gm_tag}')
        gml_elem = get_gml_element(self.geometry, f'Building.{self.local_id}.{gml_type}', self.epsg_id)

        gm_elem.appendChild(gml_elem)
        es_geom_elem.appendChild(gm_elem)
        geom_elem.appendChild(es_geom_elem)
        result.appendChild(geom_elem)

        # diameter
        if self.diameter is not None:
            elem = doc.createElement('imaer:diameter')
            elem.appendChild(doc.createTextNode(str(self.diameter)))
            result.appendChild(elem)

        return result
