import xml.etree.ElementTree as ET
import sqlite3

from imaergpkg import ImaerGpkg

from xsd_types import (
    XsdElement,
    XsdSimpleType,
    XsdComplexType,
    namespaces
)


xsd_fn = 'IMAER_2_2.xsd'
filename = '/home/raymond/tmp/imaergpkg.gpkg'

gpkg = ImaerGpkg(filename)


elements = {}
simple_types = {}

root = ET.parse(xsd_fn).getroot()
print(root)

for element in root.findall('xmlns:element', namespaces):
    #print(element)
    e = XsdElement(element)
    #print(e)

for element in root.findall('xmlns:simpleType', namespaces):
    e = XsdSimpleType(element)
    e.createTable(gpkg)

cnt = 0
for element in root.findall('xmlns:complexType', namespaces):
    cnt += 1
    print('---', cnt, '---')
    e = XsdComplexType(element)
    print(e)
    e.createTable(gpkg)
    if cnt == 1000:
        break



for child in root:#.findall('annotation'):
    pass
    #print(child.tag)
    #value = child.get('name')
    #print(value)





print(gpkg)
