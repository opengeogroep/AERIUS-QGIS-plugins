from PyQt5.QtXml import QDomDocument

from .gml import get_gml_element


class CalculationPoint(object):

    def __init__(self, *, local_id, geom, epsg_id, label=None, description=None):
        self.local_id = local_id
        self.geometry = geom
        self.epsg_id = epsg_id
        self.label = label
        self.description = description

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement(f'imaer:CalculationPoint')
        result.setAttribute('gml:id', f'CP.{self.local_id}')

        # identifier
        ident_elem = doc.createElement('imaer:identifier')
        nen_elem = doc.createElement('imaer:NEN3610ID')

        elem = doc.createElement('imaer:namespace')
        elem.appendChild(doc.createTextNode('NL.IMAER'))
        nen_elem.appendChild(elem)
        elem = doc.createElement('imaer:localId')
        elem.appendChild(doc.createTextNode(str(self.local_id)))
        nen_elem.appendChild(elem)

        ident_elem.appendChild(nen_elem)
        result.appendChild(ident_elem)

        # geometry
        gml_types = {0: 'POINT', 1: 'CURVE', 2: 'SURFACE'}
        gml_type = gml_types[self.geometry.type()]

        gm_elem = doc.createElement(f'imaer:GM_Point')
        gml_elem = get_gml_element(self.geometry, f'CP.{self.local_id}.{gml_type}', self.epsg_id)

        gm_elem.appendChild(gml_elem)
        result.appendChild(gm_elem)

        # label
        if self.label is not None:
            elem = doc.createElement('imaer:label')
            elem.appendChild(doc.createTextNode(str(self.label)))
            result.appendChild(elem)

        # description
        if self.description is not None:
            elem = doc.createElement('imaer:description')
            elem.appendChild(doc.createTextNode(str(self.description)))
            result.appendChild(elem)

        return result
