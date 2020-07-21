import xml.etree.ElementTree as ET

from imaer import FeatureCollectionCalculator



fcc = FeatureCollectionCalculator()
print(fcc)

dom = fcc.generate_dom()
print(dom)

#uglyXml = dom.toprettyxml(indent='  ', newl='\n', encoding="UTF-8")

print()
print(fcc.get_pretty_xml())
