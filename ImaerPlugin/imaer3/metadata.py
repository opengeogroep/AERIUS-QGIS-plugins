from PyQt5.QtCore import QXmlStreamReader
from PyQt5.QtXml import QDomDocument

from generic import GuiNode




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


    def get_gui_nodes(self):
        result = GuiNode('metadata', 'GROUP', label='Metadata', min_occurs=1)

        # project
        group_node = GuiNode('project', 'GROUP', label='Project', min_occurs=1)
        value_node = GuiNode('metadata_project_year', 'VALUE', label='Year', min_occurs=1)
        group_node.append_child(value_node)
        value_node = GuiNode('metadata_project_description', 'VALUE', label='Description')
        group_node.append_child(value_node)
        result.append_child(group_node)

        # situation
        group_node = GuiNode('situation', 'GROUP', label='Situation')
        value_node = GuiNode('metadata_situation_name', 'VALUE', label='Name')
        group_node.append_child(value_node)
        value_node = GuiNode('metadata_situation_reference', 'VALUE', label='Reference')
        group_node.append_child(value_node)
        result.append_child(group_node)

        # calculation
        group_node = GuiNode('calculation', 'GROUP', label='Calculation')
        value_node = GuiNode('metadata_calculation_result_type', 'VALUE', label='Result type', min_occurs=1)
        group_node.append_child(value_node)
        value_node = GuiNode('metadata_calculation_type', 'VALUE', label='Type')
        group_node.append_child(value_node)
        result.append_child(group_node)



        #self.calculation = calculation
        # resultType: DEPOSITION, CONCENTRATION, EXCEEDANCE_DAYS, EXCEEDANCE_HOURS (1..n)
        # substance: NH3, NOX, NO2, PM10, PM25, EC (1..n)
        # type: PERMIT, NATURE_AREA, RADIUS, CUSTOM_POINTS (1)

        #self.version = version



        return result
