import xml.dom.minidom
from xml.dom.minidom import parseString

from constants import *

class FeatureCollectionCalculator():

    def __init__(self):
        self.metadata = None
        self.feature_members = []


    def generate_dom(self):
        doc = xml.dom.minidom.Document()
        fcc = doc.createElementNS(imaer_ns, 'imaer:FeatureCollectionCalculator')

        fcc.setAttribute('xsi:schemaLocation',
                         '{} {}'.format(imaer_ns, _imaer_schema_location))
        fcc.setAttribute('xmlns:imaer', _imaer_ns)
        fcc.setAttribute('xmlns:gml', _gml_ns)
        fcc.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        fcc.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        fcc.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        fcc.setAttribute('gml:id', _gml_id)

        doc.appendChild(fcc)

        comment = doc.createComment('Created using QGIS ImaerPlugin by OpenGeoGroep')
        doc.appendChild(comment)

        md = doc.createElementNS(_imaer_ns, 'imaer:metadata')
        if self.metadata is not None:
            md.appendChild(self.metadata.generate_dom())
        fcc.appendChild(md)

        #print(result)
        return doc


    def get_pretty_xml(self):
        data = self.generate_dom()
        return data.toprettyxml(indent='  ', newl='\n', encoding=None)




class AeriusCalculatorMetadata():

    def __init__(self, project={}, situation={}, calculation={}, version={}):
        self.project = project
        self.situation = situation
        self.calculation = calculation
        self.version = version

    def generate_dom(self):
        doc = xml.dom.minidom.Document()
        metadata = doc.createElementNS(_imaer_ns, 'imaer:AeriusCalculatorMetadata')

        # project
        if len(self.project) > 0:
            pr = doc.createElementNS(_imaer_ns, 'imaer:project')
            pr_ele = doc.createElementNS(_imaer_ns, 'imaer:ProjectMetadata')
            if 'year' in self.project:
                ele = doc.createElementNS(_imaer_ns, 'imaer:year')
                ele.appendChild(doc.createTextNode( str(self.project['year']) ))
                pr_ele.appendChild(ele)
            if 'description' in self.project:
                ele = doc.createElementNS(_imaer_ns, 'imaer:description')
                ele.appendChild(doc.createTextNode( str(self.project['description']) ))
                pr_ele.appendChild(ele)
            pr.appendChild(pr_ele)
            metadata.appendChild(pr)

        # situation
        if len(self.situation) > 0:
            sit = doc.createElementNS(_imaer_ns, 'imaer:situation')
            sit_ele = doc.createElementNS(_imaer_ns, 'imaer:SituationMetadata')
            if 'name' in self.situation:
                ele = doc.createElementNS(_imaer_ns, 'imaer:name')
                ele.appendChild(doc.createTextNode( str(self.situation['name']) ))
                sit_ele.appendChild(ele)
            if 'reference' in self.situation:
                ele = doc.createElementNS(_imaer_ns, 'imaer:reference')
                ele.appendChild(doc.createTextNode( str(self.situation['reference']) ))
                sit_ele.appendChild(ele)
            sit.appendChild(sit_ele)
            metadata.appendChild(sit)

        # calculation
        if len(self.calculation) > 0:
            calc = doc.createElementNS(_imaer_ns, 'imaer:calculation')
            calc_ele = doc.createElementNS(_imaer_ns, 'imaer:CalculationMetadata')
            if 'type' in self.calculation:
                ele = doc.createElementNS(_imaer_ns, 'imaer:type')
                ele.appendChild(doc.createTextNode( str(self.calculation['type']) ))
                calc_ele.appendChild(ele)
            if 'substances' in self.calculation:
                for substance in self.calculation['substances']:
                    ele = doc.createElementNS(_imaer_ns, 'imaer:substance')
                    ele.appendChild(doc.createTextNode( str(substance) ))
                    calc_ele.appendChild(ele)
            if 'resultType' in self.calculation:
                ele = doc.createElementNS(_imaer_ns, 'imaer:resultType')
                ele.appendChild(doc.createTextNode( str(self.calculation['resultType']) ))
                calc_ele.appendChild(ele)
            calc.appendChild(calc_ele)
            metadata.appendChild(calc)

        # version
        if len(self.version) > 0:
            ver = doc.createElementNS(_imaer_ns, 'imaer:version')
            ver_ele = doc.createElementNS(_imaer_ns, 'imaer:VersionMetadata')
            if 'aeriusVersion' in self.version:
                ele = doc.createElementNS(_imaer_ns, 'imaer:aeriusVersion')
                ele.appendChild(doc.createTextNode( str(self.version['aeriusVersion']) ))
                ver_ele.appendChild(ele)
            if 'databaseVersion' in self.version:
                ele = doc.createElementNS(_imaer_ns, 'imaer:databaseVersion')
                ele.appendChild(doc.createTextNode( str(self.version['databaseVersion']) ))
                ver_ele.appendChild(ele)
            ver.appendChild(ver_ele)
            metadata.appendChild(ver)

        return metadata
