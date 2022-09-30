from PyQt5.QtXml import QDomDocument

#from .enumerations import OutflowDirectionType
from .gml import get_gml_element



class ReceptorGMLType(object):

    def __init__(self, *, local_id, sector_id, geom, label=None, description=None):
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

        ## emission source characteristics
        #if self.emission_source_characteristics is not None:
        #    esc_elem = doc.createElement('imaer:emissionSourceCharacteristics')
        #    esc_elem.appendChild(self.emission_source_characteristics.to_xml_elem(doc))
        #    result.appendChild(esc_elem)

        ## geometry
        #geom_elem = doc.createElement('imaer:geometry')
        #es_geom_elem = doc.createElement('imaer:EmissionSourceGeometry')

        #gm_tags = {0: 'GM_Point', 1: 'GM_Curve', 2: 'GM_Surface'}
        #gm_tag = gm_tags[self.geometry.type()]
        gml_types = {0: 'POINT', 1: 'CURVE', 2: 'SURFACE'}
        gml_type = gml_types[self.geometry.type()]#

        gm_elem = doc.createElement(f'imaer:GM_Point')
        gml_elem = get_gml_element(self.geometry, f'{self.local_id}.{gml_type}')

        gm_elem.appendChild(gml_elem)
        #es_geom_elem.appendChild(gm_elem)
        #geom_elem.appendChild(es_geom_elem)
        result.appendChild(gm_elem)#(geom_elem)

        return result




class Receptor(ReceptorGMLType):

    def __init__(self, *, emissions=[], **kwargs):
        super().__init__(**kwargs)
        self.emissions = emissions


    def to_xml_elem(self, doc=QDomDocument()):
        if doc is None:
            doc = QDomDocument()

        result = super().to_xml_elem(doc)

        for em in self.emissions:
            elem = em.to_xml_elem(doc)
            result.appendChild(elem)

        return result



'''
class EmissionSourceCharacteristics(object):

    def __init__(self, heat_content=None, emission_height=None, spread=None, diurnal_variation=None, building=None):
        self.heat_content = heat_content
        self.emission_height = emission_height
        self.spread = spread
        self.diurnal_variation = diurnal_variation
        self.building = building


    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:EmissionSourceCharacteristics')

        # heat content
        if self.heat_content is not None:
            elem = self.heat_content.to_xml_elem(doc)
            result.appendChild(elem)

        # emission height
        if self.emission_height is not None:
            elem = doc.createElement('imaer:emissionHeight')
            elem.appendChild(doc.createTextNode(str(self.emission_height)))
            result.appendChild(elem)

        # spread
        if self.spread is not None:
            elem = doc.createElement('imaer:spread')
            elem.appendChild(doc.createTextNode(str(self.spread)))
            result.appendChild(elem)

        # diurnal variation
        if self.diurnal_variation is not None:
            elem = doc.createElement('imaer:diurnalVariation')
            elem.appendChild(doc.createTextNode(str(self.diurnal_variation)))
            result.appendChild(elem)

        return result




class HeatContent(object):

    def __init__(self):
        pass


    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:heatContent')
        return result




class SpecifiedHeatContent(HeatContent):

    def __init__(self, *, value, **kwargs):
        super().__init__(**kwargs)
        self.value = value


    def to_xml_elem(self, doc=QDomDocument()):
        result = super().to_xml_elem(doc)

        shc = doc.createElement('imaer:SpecifiedHeatContent')
        v = doc.createElement('imaer:value')
        v.appendChild(doc.createTextNode( str(self.value) ))

        shc.appendChild(v)
        result.appendChild(shc)

        return result




class Emission(object):

    def __init__(self, substance, value):
        self.substance = substance
        self.value = value


    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:emission')

        em_elem = doc.createElement('imaer:Emission')
        em_elem.setAttribute('substance', self.substance)
        v_elem = doc.createElement('imaer:value')
        v_elem.appendChild(doc.createTextNode( str(self.value) ))

        em_elem.appendChild(v_elem)
        result.appendChild(em_elem)

        return result
'''