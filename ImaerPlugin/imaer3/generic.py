import xml.etree.ElementTree as ET

namespaces = {
    'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
    'xmlns:imaer': "http://imaer.aerius.nl/3.1",
    'xmlns:xlink': "http://www.w3.org/1999/xlink",
    'xmlns:gml': "http://www.opengis.net/gml/3.2",
    'gml:id': "NL.IMAER.Collection",
    'xsi:schemaLocation': "http://imaer.aerius.nl/3.1 http://imaer.aerius.nl/3.1/IMAER.xsd"
}

for name, value in namespaces.items():
    ET.register_namespace(name, value)


def remove_ns(tag):
    loc = tag.find('}')
    return tag[loc+1:]


def find_xml_value(root, tag_name, object_type='text', default_value=None):
    'Attempts to find a value in the xml doc and returns a value related to it.'
    elem = root.find(tag_name, namespaces)
    if elem is None:
        print(f'cannot find tag: {tag_name} in xml')
        return default_value
    #print(elem.attrib)
    if object_type == 'text':
        return elem.text
