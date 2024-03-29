from PyQt5.QtCore import QXmlStreamReader
from PyQt5.QtXml import QDomDocument

from .metadata import AeriusCalculatorMetadata
from .emission_source import EmissionSource


class ImaerDocument():

    def __init__(self, fn=None):
        self.fn = fn

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
