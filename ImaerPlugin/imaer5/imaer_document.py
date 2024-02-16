from PyQt5.QtCore import QXmlStreamReader, QFile
from PyQt5.QtXml import QDomDocument

from .metadata import AeriusCalculatorMetadata
from .emission_source import EmissionSource
from .receptors import ReceptorPoint, SubPoint


class ImaerDocument():

    def __init__(self):
        self.metadata = None
        self.feature_members = []
        self.definitions = []

        self.doc = QDomDocument()

    def __str__(self):
        result = 'ImaerDocument[{}, feature_members:{}]'.format(
            self.metadata,
            len(self.feature_members)
        )
        return result
    
    def clear(self):
        self.metadata = None
        self.feature_members = []
        self.definitions = []

    def to_xml_elem(self):

        inst = self.doc.createProcessingInstruction('xml', 'version="1.0" encoding="utf-8" standalone="yes"')
        self.doc.appendChild(inst)

        fcc_elem = self.doc.createElement('imaer:FeatureCollectionCalculator')
        fcc_elem.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        # fcc_elem.setAttribute('xmlns:imaer', 'http://www.kadaster.nl/schemas/geovalidaties/manifestbestand/v20181101')
        fcc_elem.setAttribute('xmlns:imaer', 'http://imaer.aerius.nl/5.1')
        fcc_elem.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        fcc_elem.setAttribute('xmlns:gml', 'http://www.opengis.net/gml/3.2')
        fcc_elem.setAttribute('gml:id', 'NL.IMAER.Collection')
        fcc_elem.setAttribute('xsi:schemaLocation', 'http://imaer.aerius.nl/5.1 http://imaer.aerius.nl/5.1/IMAER.xsd')
        self.doc.appendChild(fcc_elem)

        if self.metadata is not None:
            metadata_elem = self.doc.createElement('imaer:metadata')
            fcc_elem.appendChild(metadata_elem)
            metadata_elem.appendChild(self.metadata.to_xml_elem(self.doc))

        for feature_member in self.feature_members:
            feature_member_elem = self.doc.createElement('imaer:featureMember')
            fcc_elem.appendChild(feature_member_elem)
            feature_member_elem.appendChild(feature_member.to_xml_elem(self.doc))

        if len(self.definitions) > 0:
            def_elem_1 = self.doc.createElement('imaer:definitions')
            def_elem_2 = self.doc.createElement('imaer:Definitions')

            for definition in self.definitions:
                def_elem_2.appendChild(definition.to_xml_elem(self.doc))

            def_elem_1.appendChild(def_elem_2)
            fcc_elem.appendChild(def_elem_1)

    def to_xml_file(self, fn):
        self.to_xml_elem()

        with open(fn, 'w') as out_file:
            out_file.write(self.doc.toString(4))

    def from_xml_file(self, fn):
        file = QFile(fn)
        file.open(QFile.ReadOnly | QFile.Text)
        xml_reader = QXmlStreamReader(file)

        xml_reader.readNext()
        while not xml_reader.atEnd():
            if xml_reader.isStartElement():
                tag_name = xml_reader.name()
                #print(tag_name)

                if tag_name == 'AeriusCalculatorMetadata':
                    self.metadata = AeriusCalculatorMetadata()
                    self.metadata.from_xml_reader(xml_reader)

                if tag_name == 'featureMember':
                    xml_reader.readNextStartElement()
                    tag_name = xml_reader.name()

                    if tag_name == 'ReceptorPoint':
                        #print(f'  Processing {tag_name}')
                        member = ReceptorPoint()
                        member.from_xml_reader(xml_reader)
                        if member.is_valid():
                            self.feature_members.append(member)
                    elif tag_name == 'SubPoint':
                        # print(f'  Processing {tag_name}')
                        member = SubPoint()
                        member.from_xml_reader(xml_reader)
                        if member.is_valid():
                            self.feature_members.append(member)
                    else:
                        #print(f'  Skipping {tag_name}')
                        xml_reader.skipCurrentElement()

            xml_reader.readNext()
        if xml_reader.hasError():
            pass        

    def get_statistics(self):
        feature_members = {}
        for member in self.feature_members:
            # print(member, feature_members)
            class_name = member.__class__.__name__
            if class_name in feature_members:
                feature_members[class_name] += 1
            else:
                feature_members[class_name] = 1
        return feature_members