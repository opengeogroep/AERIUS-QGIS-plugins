from PyQt5.QtXml import QDomDocument

#from .enumerations import OutflowDirectionType
from .generic import GuiNode


class EmissionSource():

    def __init__(self, doc=None):
        self.doc = doc
        if self.doc is None:
            self.doc = QDomDocument()

        self.emission_source_characteristics = None
        self.building = None
        self.emissions = []
        self.geometry = None
        self.identifier = None
        self.sectorId = 9999


    def get_gui_nodes(self):
        result = GuiNode('EmissionSource', 'GROUP')

        result.append_child(GuiNode('description', 'STR'))
        result.append_child(EmissionSourceCharacteristics().get_gui_nodes())

        return result




class EmissionSourceCharacteristics(object):

    def __init__(self, heat_content=None, emission_height=None, spread=None, diurnal_variation=None, building=None):
        self.heat_content = heat_content
        self.emission_height = emission_height
        self.spread = spread
        self.diurnal_variation = diurnal_variation
        self.building = building


    def get_gui_nodes(self):
        result = GuiNode('EmissionSourceCharacteristics', 'GROUP')

        result.append_child(GuiNode('diurnalVariation', 'STR'))
        result.append_child(GuiNode('emissionHeight', 'FLOAT', min_occurs=1))
        result.append_child(GuiNode('spread', 'FLOAT'))

        return result



'''
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
        if self.orientation is not None:
            orientation = doc.createElementNS(_imaer_ns, 'imaer:orientation')
            orientation.appendChild(doc.createTextNode( str(self.orientation) ))
            bld2.appendChild(orientation)

        bld1.appendChild(bld2)

        return bld1
'''
