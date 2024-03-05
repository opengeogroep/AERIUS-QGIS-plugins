from PyQt5.QtCore import QXmlStreamReader
from PyQt5.QtXml import QDomDocument


class AeriusCalculatorMetadata():

    def __init__(self, project=None, situation=None, calculation=None, version=None, gml_creator=None):
        self.project = project
        # year
        # description

        self.situation = situation
        # name
        # reference

        self.calculation = calculation
        # resultType: DEPOSITION, CONCENTRATION, EXCEEDANCE_DAYS, EXCEEDANCE_HOURS (1..n)
        # substance: NH3, NOX, NO2, PM10, PM25, EC (1..n)
        # type: PERMIT, NATURE_AREA, RADIUS, CUSTOM_POINTS (1)

        self.version = version
        # aeriusVersion
        # databaseVersion

        self.gml_creator = gml_creator
        # Since IMAER 5.1.2 (0..1)

    def to_xml_elem(self, doc):
        result = doc.createElement('imaer:AeriusCalculatorMetadata')

        # project
        if self.project is not None:
            if len(self.project) > 0:
                pr = doc.createElement('imaer:project')
                pr_ele = doc.createElement('imaer:ProjectMetadata')
                if 'year' in self.project:
                    ele = doc.createElement('imaer:year')
                    ele.appendChild(doc.createTextNode(str(self.project['year'])))
                    pr_ele.appendChild(ele)
                if 'description' in self.project:
                    ele = doc.createElement('imaer:description')
                    ele.appendChild(doc.createTextNode(str(self.project['description'])))
                    pr_ele.appendChild(ele)
                pr.appendChild(pr_ele)
                result.appendChild(pr)

        # situation
        if self.situation is not None:
            sit = doc.createElement('imaer:situation')
            sit_ele = doc.createElement('imaer:SituationMetadata')
            if 'name' in self.situation:
                ele = doc.createElement('imaer:name')
                ele.appendChild(doc.createTextNode(str(self.situation['name'])))
                sit_ele.appendChild(ele)
            if 'reference' in self.situation:
                ele = doc.createElement('imaer:reference')
                ele.appendChild(doc.createTextNode(str(self.situation['reference'])))
                sit_ele.appendChild(ele)
            if 'type' in self.situation:
                ele = doc.createElement('imaer:situationType')
                ele.appendChild(doc.createTextNode(str(self.situation['type'])))
                sit_ele.appendChild(ele)
            sit.appendChild(sit_ele)
            result.appendChild(sit)

        # calculation
        if self.calculation is not None:
            calc = doc.createElement('imaer:calculation')
            calc_ele = doc.createElement('imaer:CalculationMetadata')
            if 'type' in self.calculation:
                ele = doc.createElement('imaer:method')
                ele.appendChild(doc.createTextNode(str(self.calculation['type'])))
                calc_ele.appendChild(ele)
            elif 'method' in self.calculation:
                ele = doc.createElement('imaer:method')
                ele.appendChild(doc.createTextNode(str(self.calculation['method'])))
                calc_ele.appendChild(ele)
            if 'substances' in self.calculation:
                for substance in self.calculation['substances']:
                    ele = doc.createElement('imaer:substance')
                    ele.appendChild(doc.createTextNode(str(substance)))
                    calc_ele.appendChild(ele)
            if 'result_types' in self.calculation:
                for result_type in self.calculation['result_types']:
                    ele = doc.createElement('imaer:resultType')
                    ele.appendChild(doc.createTextNode(str(result_type)))
                    calc_ele.appendChild(ele)
            calc.appendChild(calc_ele)
            result.appendChild(calc)

        # version
        if self.version is not None:
            ver = doc.createElement('imaer:version')
            ver_ele = doc.createElement('imaer:VersionMetadata')
            if 'aeriusVersion' in self.version:
                ele = doc.createElement('imaer:aeriusVersion')
                ele.appendChild(doc.createTextNode(str(self.version['aeriusVersion'])))
                ver_ele.appendChild(ele)
            if 'databaseVersion' in self.version:
                ele = doc.createElement('imaer:databaseVersion')
                ele.appendChild(doc.createTextNode(str(self.version['databaseVersion'])))
                ver_ele.appendChild(ele)
            ver.appendChild(ver_ele)
            result.appendChild(ver)

        # gml creator
        if self.gml_creator is not None:
            ele = doc.createElement('imaer:gmlCreator')
            ele.appendChild(doc.createTextNode(str(self.gml_creator)))
            result.appendChild(ele)

        return result

    def from_xml_reader(self, xml_reader):
        start_tag_name = xml_reader.name()

        while not (xml_reader.name() == start_tag_name and xml_reader.isEndElement()):
            xml_reader.readNextStartElement()

            if xml_reader.name() == 'project':
                self.project = {}
                while not (xml_reader.name() == 'project' and xml_reader.isEndElement()):
                    xml_reader.readNextStartElement()
                    if xml_reader.name() == 'year' and xml_reader.isStartElement():
                        xml_reader.readNext()
                        self.project['year'] = int(xml_reader.text())
                    elif xml_reader.name() == 'description' and xml_reader.isStartElement():
                        xml_reader.readNext()
                        self.project['descripton'] = xml_reader.text()

            elif xml_reader.name() == 'situation':
                self.situation = {}
                while not (xml_reader.name() == 'situation' and xml_reader.isEndElement()):
                    xml_reader.readNextStartElement()
                    if xml_reader.name() == 'name' and xml_reader.isStartElement():
                        xml_reader.readNext()
                        self.situation['name'] = xml_reader.text()
                    if xml_reader.name() == 'reference' and xml_reader.isStartElement():
                        xml_reader.readNext()
                        self.situation['reference'] = xml_reader.text()
                    if xml_reader.name() == 'situationType' and xml_reader.isStartElement():
                        xml_reader.readNext()
                        self.situation['type'] = xml_reader.text()

            elif xml_reader.name() == 'version':
                self.version = {}
                while not (xml_reader.name() == 'version' and xml_reader.isEndElement()):
                    xml_reader.readNextStartElement()
                    if xml_reader.name() == 'aeriusVersion' and xml_reader.isStartElement():
                        xml_reader.readNext()
                        self.version['aeriusVersion'] = xml_reader.text()
                    if xml_reader.name() == 'databaseVersion' and xml_reader.isStartElement():
                        xml_reader.readNext()
                        self.version['databaseVersion'] = xml_reader.text()

            elif xml_reader.name() == 'calculation':
                self.calculation = {'substances': [], 'result_types': []}
                while not (xml_reader.name() == 'calculation' and xml_reader.isEndElement()):
                    xml_reader.readNextStartElement()
                    if xml_reader.name() == 'method' and xml_reader.isStartElement():
                        xml_reader.readNext()
                        self.calculation['method'] = xml_reader.text()
                    if xml_reader.name() == 'substance' and xml_reader.isStartElement():
                        xml_reader.readNext()
                        self.calculation['substances'].append(xml_reader.text())
                    if xml_reader.name() == 'resultType' and xml_reader.isStartElement():
                        xml_reader.readNext()
                        self.calculation['result_types'].append(xml_reader.text())

            elif xml_reader.name() == 'gmlCreator':
                xml_reader.readNext()
                self.gml_creator = xml_reader.text()
