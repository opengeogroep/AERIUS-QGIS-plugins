import sys

from PyQt5.QtXml import QDomDocument

#path_qgis_python_folder = "/home/raymond/programs/qgis/qgis-master/share/qgis/python/"
#sys.path.append(path_qgis_python_folder)
#from qgis.core import QgsGeometry


class Identifier():

    def __init__(self, namespace=None, local_id=None):
        self.namespace = namespace
        self.local_id = local_id

    def __str__(self):
        return f'Identifier[{self.namespace}, {self.local_id}]'

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