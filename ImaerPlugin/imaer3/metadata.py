from PyQt5.QtCore import QXmlStreamReader
from PyQt5.QtXml import QDomDocument

from generic import ParameterDef




class AeriusCalculatorMetadata():

    def __init__(self, project={}, situation={}, calculation={}, version={}):
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


    def to_xml_elem(self, doc):
        result = doc.createElement('imaer:AeriusCalculatorMetadata')

        # project
        if len(self.project) > 0:
            pr = doc.createElement('imaer:project')
            pr_ele = doc.createElement('imaer:ProjectMetadata')
            if 'year' in self.project:
                ele = doc.createElement('imaer:year')
                ele.appendChild(doc.createTextNode( str(self.project['year']) ))
                pr_ele.appendChild(ele)
            if 'description' in self.project:
                ele = doc.createElement('imaer:description')
                ele.appendChild(doc.createTextNode( str(self.project['description']) ))
                pr_ele.appendChild(ele)
            pr.appendChild(pr_ele)
            result.appendChild(pr)


        # situation
        if len(self.situation) > 0:
            sit = doc.createElement('imaer:situation')
            sit_ele = doc.createElement('imaer:SituationMetadata')
            if 'name' in self.situation:
                ele = doc.createElement('imaer:name')
                ele.appendChild(doc.createTextNode( str(self.situation['name']) ))
                sit_ele.appendChild(ele)
            if 'reference' in self.situation:
                ele = doc.createElement('imaer:reference')
                ele.appendChild(doc.createTextNode( str(self.situation['reference']) ))
                sit_ele.appendChild(ele)
            sit.appendChild(sit_ele)
            result.appendChild(sit)

        # calculation
        if len(self.calculation) > 0:
            calc = doc.createElement('imaer:calculation')
            calc_ele = doc.createElement('imaer:CalculationMetadata')
            if 'type' in self.calculation:
                ele = doc.createElement('imaer:type')
                ele.appendChild(doc.createTextNode( str(self.calculation['type']) ))
                calc_ele.appendChild(ele)
            if 'substances' in self.calculation:
                for substance in self.calculation['substances']:
                    ele = doc.createElement('imaer:substance')
                    ele.appendChild(doc.createTextNode( str(substance) ))
                    calc_ele.appendChild(ele)
            if 'resultType' in self.calculation:
                ele = doc.createElement('imaer:resultType')
                ele.appendChild(doc.createTextNode( str(self.calculation['resultType']) ))
                calc_ele.appendChild(ele)
            calc.appendChild(calc_ele)
            result.appendChild(calc)

        # version
        if len(self.version) > 0:
            ver = doc.createElement('imaer:version')
            ver_ele = doc.createElement('imaer:VersionMetadata')
            if 'aeriusVersion' in self.version:
                ele = doc.createElement('imaer:aeriusVersion')
                ele.appendChild(doc.createTextNode( str(self.version['aeriusVersion']) ))
                ver_ele.appendChild(ele)
            if 'databaseVersion' in self.version:
                ele = doc.createElement('imaer:databaseVersion')
                ele.appendChild(doc.createTextNode( str(self.version['databaseVersion']) ))
                ver_ele.appendChild(ele)
            ver.appendChild(ver_ele)
            result.appendChild(ver)

        return result


    def get_parameter_defs(self):
        result = ParameterDef('metadata', 'GROUP', label='Metadata', min_occurs=1)
        return result
