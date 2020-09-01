import xml.etree.ElementTree as ET
import xml.dom.minidom

#from .enumerations import OutflowDirectionType


# constants
_gml_ns = 'http://www.opengis.net/gml/3.2'
_imaer_ns = 'http://imaer.aerius.nl/3.1'
_imaer_schema_location = 'http://imaer.aerius.nl/3.1/IMAER.xsd'
_gml_id = 'NL.IMAER.Collection'




class EmissionSourceCharacteristics(object):

    def __init__(self, heat_content, emission_height, spread=None, diurnal_variation=None, building=None):
        self.heat_content = heat_content
        self.emission_height = emission_height
        self.spread = spread
        self.diurnal_variation = diurnal_variation
        self.building = building

    def generate_dom(self):
        doc = xml.dom.minidom.Document()
        esc1 = doc.createElementNS(_imaer_ns, 'imaer:emissionSourceCharacteristics')
        esc2 = doc.createElementNS(_imaer_ns, 'imaer:EmissionSourceCharacteristics')

        hc = self.heat_content.generate_dom()
        esc2.appendChild(hc)

        eh = doc.createElementNS(_imaer_ns, 'imaer:emissionHeight')
        eh.appendChild(doc.createTextNode( str(self.emission_height) ))
        esc2.appendChild(eh)

        if self.spread is not None:
            spr = doc.createElementNS(_imaer_ns, 'imaer:spread')
            spr.appendChild(doc.createTextNode( str(self.emission_height) ))
            esc2.appendChild(eh)

        if self.diurnal_variation is not None:
            dv = doc.createElementNS(_imaer_ns, 'imaer:diurnalVariation')
            dv.appendChild(doc.createTextNode( str(self.diurnal_variation) ))
            esc2.appendChild(dv)

        if self.building is not None:
            dv = self.building.generate_dom()
            esc2.appendChild(dv)

        esc1.appendChild(esc2)
        return esc1




class HeatContent(object):

    def generate_dom(self):
        doc = xml.dom.minidom.Document()
        hc = doc.createElementNS(_imaer_ns, 'imaer:heatContent')
        return hc




class SpecifiedHeatContent(HeatContent):

    def __init__(self, value):
        self.value = value


    def generate_dom(self):
        hc = super().generate_dom()
        doc = xml.dom.minidom.Document()
        shc = doc.createElementNS(_imaer_ns, 'imaer:SpecifiedHeatContent')
        v = doc.createElementNS(_imaer_ns, 'imaer:value')
        v.appendChild(doc.createTextNode( str(self.value) ))

        shc.appendChild(v)
        hc.appendChild(shc)

        return hc




class CalculatedHeatContent(HeatContent):

    def __init__(self, emission_temperature, outflow_diameter, outflow_velocity, outflow_direction):
        self.emission_temperature = emission_temperature
        self.outflow_diameter = outflow_diameter
        self.outflow_velocity = outflow_velocity
        self.outflow_direction = outflow_direction


    def generate_dom(self):
        hc = super().generate_dom()
        doc = xml.dom.minidom.Document()

        chc = doc.createElementNS(_imaer_ns, 'imaer:CalculatedHeatContent')

        em_t = doc.createElementNS(_imaer_ns, 'imaer:emissionTemperature')
        em_t.appendChild(doc.createTextNode( str(self.emission_temperature) ))
        chc.appendChild(em_t)

        of_diam = doc.createElementNS(_imaer_ns, 'imaer:outflow_diameter')
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

    def generate_dom(self):
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
        orientation = doc.createElementNS(_imaer_ns, 'imaer:orientation')
        orientation.appendChild(doc.createTextNode( str(self.orientation) ))
        bld2.appendChild(orientation)

        bld1.appendChild(bld2)

        return bld1
