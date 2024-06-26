import sys

from PyQt5.QtXml import QDomDocument


class Nen3610Id():

    def __init__(self, namespace='NL.IMAER', local_id=None):
        self.namespace = namespace
        self.local_id = local_id

    def __str__(self):
        return f'Identifier[{self.namespace}, {self.local_id}]'

    def to_xml_elem(self, doc):
        result = doc.createElement('imaer:NEN3610ID')

        if self.namespace is not None:
            ele = doc.createElement('imaer:namespace')
            ele.appendChild(doc.createTextNode(str(self.namespace)))
            result.appendChild(ele)
        if self.local_id is not None:
            ele = doc.createElement('imaer:localId')
            ele.appendChild(doc.createTextNode(str(self.local_id)))
            result.appendChild(ele)
        return result

    def from_xml_reader(self, xml_reader):
        if not xml_reader.isStartElement():
            return
        if xml_reader.name() != 'NEN3610ID':
            return
        while not (xml_reader.name() == 'NEN3610ID' and xml_reader.isEndElement()):
            xml_reader.readNextStartElement()
            if xml_reader.name() == 'namespace' and xml_reader.isStartElement():
                xml_reader.readNext()
                self.namespace = xml_reader.text()
            if xml_reader.name() == 'localId' and xml_reader.isStartElement():
                xml_reader.readNext()
                self.local_id = xml_reader.text()

    def is_valid(self):
        return (self.namespace is not None and self.local_id is not None)