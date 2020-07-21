import xml.etree.ElementTree as ET

from imaer import FeatureCollectionCalculator, AeriusCalculatorMetadata



fcc = FeatureCollectionCalculator()
print(fcc)

md = AeriusCalculatorMetadata()
fcc.metadata = AeriusCalculatorMetadata(
    project = {'year': 2020, 'description': 'DD'},
    situation = {'name': 'Situatie 2', 'reference': 'RqC3DZvKt6ux'},
    calculation = {'type': 'PERMIT', 'substances': ['NOX', 'NO2', 'NH3'], 'resultType': 'DEPOSITION'},
    version = {'aeriusVersion': '2019A_20200610_3aefc4c15b', 'databaseVersion': '2019A_20200610_3aefc4c15b'}
)

dom = fcc.generate_dom()
print(dom)

#uglyXml = dom.toprettyxml(indent='  ', newl='\n', encoding="UTF-8")

print()
print(fcc.get_pretty_xml())
