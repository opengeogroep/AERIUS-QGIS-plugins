#from PyQt5.QtXml import QDomDocument

#from .generic import xml_reader_to_current_node
from .geometry import GmlPoint, GmlPolygon
from .identifier import Identifier

class CalculationResult(object):

    def __init__(self, result_type=None, substance=None, value=None):
        self.result_type = result_type
        self.substance = substance
        self.value = value

    def __str__(self):
        return f'CalculationResult[{self.result_type}, {self.substance}, {self.value}]'
    
    def is_valid(self):
        return self.result_type is not None \
            and self.substance is not None \
            and self.value is not None

    def from_xml_reader(self, xml_reader):
        #print('--- 1', xml_reader.name(), xml_reader.isStartElement())
        if not xml_reader.name() == 'CalculationResult':
            return
        attributes = xml_reader.attributes()
        if attributes.hasAttribute('resultType'):
            self.result_type = attributes.value('resultType')
        if attributes.hasAttribute('substance'):
            self.substance = attributes.value('substance')
        xml_reader.readNextStartElement()
        if xml_reader.name() == 'value':
            xml_reader.readNext()
            text = xml_reader.text()
            self.value = float(text)

class ReceptorPoint(object):

    def __init__(self, local_id=None, identifier= None, geom=None, epsg_id=None, results=None):
        self.local_id = local_id
        self.identifier = identifier
        self.gm_point = geom
        self.representation = None
        self.results = results or []
    
    def is_valid(self):
        return self.local_id is not None
    
    def __str__(self):
        return f'ReceptorPoint[{self.local_id}, {len(self.results)}]'

    def from_xml_reader(self, xml_reader):
        #print('        from_xml_reader()')
        #if xml_reader.isStartElement():
        tag_name = xml_reader.name()
        #print(tag_name)
        if not tag_name == 'ReceptorPoint':
            return False
        attributes = xml_reader.attributes()
        if attributes.hasAttribute('receptorPointId'):
            self.local_id = attributes.value('receptorPointId')
        while not (xml_reader.name() == 'ReceptorPoint' and xml_reader.isEndElement()):
            xml_reader.readNextStartElement()

            if xml_reader.name() == 'identifier':
                xml_reader.readNextStartElement()
                if xml_reader.name() == 'NEN3610ID':
                    identifier = Identifier()
                    identifier.from_xml_reader(xml_reader)
                    # print(identifier)
                    if identifier.is_valid():
                        self.identifier = identifier

            if xml_reader.name() == 'GM_Point':
                xml_reader.readNextStartElement()
                if xml_reader.name() == 'Point':
                    geom = GmlPoint()
                    geom.from_xml_reader(xml_reader)
                    # print(geom)
                    if geom.is_valid():
                        self.gm_point = geom

            if xml_reader.name() == 'representation':
                xml_reader.readNextStartElement()
                if xml_reader.name() == 'Polygon':
                    geom = GmlPolygon()
                    geom.from_xml_reader(xml_reader)
                    # print(geom)
                    if geom.is_valid():
                        self.representation = geom

            if xml_reader.name() == 'CalculationResult':
                result = CalculationResult()
                result.from_xml_reader(xml_reader)
                if result.is_valid():
                    self.results.append(result)
