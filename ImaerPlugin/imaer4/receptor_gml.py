from PyQt5.QtXml import QDomDocument

#from .enumerations import OutflowDirectionType
from .gml import get_gml_element


class ReceptorGMLType(object):

    def __init__(self, *, local_id, geom, label=None, description=None):
        self.label = label
        self.description = description
        self.emission_source_characteristics = None
        #self.sector_id = sector_id
        #self.building = None
        #self.emissions = []
        self.geometry = geom
        self.local_id = local_id


    def to_xml_elem(self, doc=QDomDocument()):
        #print('class:', self.__class__.__name__)
        class_name = self.__class__.__name__
        result = doc.createElement(f'imaer:CalculationPoint')

        #result.setAttribute('sectorId', self.sector_id)
        result.setAttribute('gml:id', str("CP.{}".format(str(self.local_id))))

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

        # description
        if self.description is not None:
            elem = doc.createElement('imaer:description')
            elem.appendChild(doc.createTextNode(str(self.description)))
            result.appendChild(elem)

        gml_types = {0: 'POINT', 1: 'CURVE', 2: 'SURFACE'}
        gml_type = gml_types[self.geometry.type()]#

        gm_elem = doc.createElement(f'imaer:GM_Point')
        gml_elem = get_gml_element(self.geometry, f'{self.local_id}.{gml_type}')

        gm_elem.appendChild(gml_elem)
        result.appendChild(gm_elem)

        # label
        if self.label is not None:
            elem = doc.createElement('imaer:label')
            elem.appendChild(doc.createTextNode(str(self.label)))
            result.appendChild(elem)

        return result

class Receptor(ReceptorGMLType):

    def __init__(self, *, receptor=[], **kwargs):
        super().__init__(**kwargs)
        self.receptor = receptor


    def to_xml_elem(self, doc=QDomDocument()):
        if doc is None:
            doc = QDomDocument()

        result = super().to_xml_elem(doc)

        for em in self.receptor:
            elem = em.to_xml_elem(doc)
            result.appendChild(elem)

        return result