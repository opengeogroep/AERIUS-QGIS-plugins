from PyQt5.QtXml import QDomDocument

#from .enumerations import OutflowDirectionType
from .gml import get_gml_element



class EmissionSourceType(object):

    def __init__(self, *, local_id, sector_id, geom, label=None, description=None):
        self.label = label
        self.description = description
        self.emission_source_characteristics = None
        self.sector_id = sector_id
        self.building = None
        self.emissions = []
        self.geometry = geom
        self.identifier = local_id


    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:EmissionSource')
        result.setAttribute('sectorId', self.sector_id)

        # identifier
        ident_elem = doc.createElement('imaer:identifier')
        nen_elem = doc.createElement('imaer:NEN3610ID')

        elem = doc.createElement('imaer:namespace')
        elem.appendChild(doc.createTextNode('NL.IMAER'))
        nen_elem.appendChild(elem)
        elem = doc.createElement('imaer:localId')
        elem.appendChild(doc.createTextNode(str(self.identifier)))
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

        # geometry
        geom_elem = doc.createElement('imaer:geometry')
        es_geom_elem = doc.createElement('imaer:EmissionSourceGeometry')

        gm_tags = {0: 'GM_Point', 1: 'GM_Curve', 2: 'GM_Surface'}
        gm_tag = gm_tags[self.geometry.type()]
        gml_types = {0: 'POINT', 1: 'CURVE', 2: 'SURFACE'}
        gml_type = gml_types[self.geometry.type()]

        gm_elem = doc.createElement(f'imaer:{gm_tag}')
        gml_elem = get_gml_element(self.geometry, f'{self.identifier}.{gml_type}')

        gm_elem.appendChild(gml_elem)
        es_geom_elem.appendChild(gm_elem)
        geom_elem.appendChild(es_geom_elem)
        result.appendChild(geom_elem)

        # emission source characteristics
        if self.emission_source_characteristics is not None:
            esc_elem = doc.createElement('imaer:emissionSourceCharacteristics')
            esc_elem.appendChild(self.emission_source_characteristics.to_xml_elem(doc))
            result.appendChild(esc_elem)


        return result


class EmissionSourceCharacteristics(object):

    def __init__(self, heat_content=None, emission_height=None, spread=None, diurnal_variation=None, building=None):
        self.heat_content = heat_content
        self.emission_height = emission_height
        self.spread = spread
        self.diurnal_variation = diurnal_variation
        self.building = building


    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:EmissionSourceCharacteristics')

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

    def to_xml_elem(self):
        doc = xml.dom.minidom.Document()
        hc = doc.createElementNS(_imaer_ns, 'imaer:heatContent')
        return hc




class SpecifiedHeatContent(HeatContent):

    def __init__(self, value):
        self.value = value


    def to_xml_elem(self):
        hc = super().generate_dom()
        doc = xml.dom.minidom.Document()
        shc = doc.createElementNS(_imaer_ns, 'imaer:SpecifiedHeatContent')
        v = doc.createElementNS(_imaer_ns, 'imaer:value')
        v.appendChild(doc.createTextNode( str(self.value) ))

        shc.appendChild(v)
        hc.appendChild(shc)

        return hc



'''
class CalculatedHeatContent(HeatContent):

    def __init__(self, emission_temperature, outflow_diameter, outflow_velocity, outflow_direction):
        self.emission_temperature = emission_temperature
        self.outflow_diameter = outflow_diameter
        self.outflow_velocity = outflow_velocity
        self.outflow_direction = outflow_direction


    def to_xml_elem(self):
        hc = super().generate_dom()
        doc = xml.dom.minidom.Document()

        chc = doc.createElementNS(_imaer_ns, 'imaer:CalculatedHeatContent')

        em_t = doc.createElementNS(_imaer_ns, 'imaer:emissionTemperature')
        em_t.appendChild(doc.createTextNode( str(self.emission_temperature) ))
        chc.appendChild(em_t)

        of_diam = doc.createElementNS(_imaer_ns, 'imaer:outflowDiameter')
        of_diam.appendChild(doc.createTextNode( str(self.outflow_diameter) ))
        chc.appendChild(of_diam)

        of_v = doc.createElementNS(_imaer_ns, 'imaer:outflowVelocity')
        of_v.appendChild(doc.createTextNode( str(self.outflow_velocity) ))
        chc.appendChild(of_v)

        of_dir = doc.createElementNS(_imaer_ns, 'imaer:outflowDirection')
        of_dir.appendChild(doc.createTextNode( str(self.outflow_direction) ))
        chc.appendChild(of_dir)

        hc.appendChild(chc)

        return hc




class Building(object):

    def __init__(self, height, width, length, orientation=None):
        self.height = height
        self.width = width
        self.length = length
        self.orientation = orientation

    def to_xml_elem(self):
        doc = xml.dom.minidom.Document()

        bld1 = doc.createElementNS(_imaer_ns, 'imaer:building')
        bld2 = doc.createElementNS(_imaer_ns, 'imaer:Building')

        height = doc.createElementNS(_imaer_ns, 'imaer:height')
        height.appendChild(doc.createTextNode( str(self.height) ))
        bld2.appendChild(height)
        width = doc.createElementNS(_imaer_ns, 'imaer:width')
        width.appendChild(doc.createTextNode( str(self.width) ))
        bld2.appendChild(width)
        length = doc.createElementNS(_imaer_ns, 'imaer:length')
        length.appendChild(doc.createTextNode( str(self.length) ))
        bld2.appendChild(length)
        if self.orientation is not None:
            orientation = doc.createElementNS(_imaer_ns, 'imaer:orientation')
            orientation.appendChild(doc.createTextNode( str(self.orientation) ))
            bld2.appendChild(orientation)

        bld1.appendChild(bld2)

        return bld1
'''


class EmissionSource(EmissionSourceType):

    def __init__(self, *, emissions=[], **kwargs):
        super().__init__(**kwargs)
        self.emissions = emissions


    def to_xml_elem(self, doc=QDomDocument()):
        if doc is None:
            doc = QDomDocument()

        result = super().to_xml_elem(doc)

        return result
