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
    return tag[loc + 1:]


def find_xml_value(root, tag_name, object_type='text', default_value=None):
    'Attempts to find a value in the xml doc and returns a value related to it.'
    elem = root.find(tag_name, namespaces)
    if elem is None:
        print(f'cannot find tag: {tag_name} in xml')
        return default_value
    # print(elem.attrib)
    if object_type == 'text':
        return elem.text


def __get_attribute_string(attributes):
    if len(attributes) == 0:
        return ''
    attribute_strings = []
    for attribute in attributes:
        name = attribute.name()
        value = attribute.value()
        attribute_strings.append(f'{name}="{value}"')
    return ' '.join(attribute_strings)


def xml_reader_to_current_node(xml_reader):
    result = ''
    start_name = xml_reader.name()
    while not (xml_reader.name() == start_name and xml_reader.isEndElement()):
        name = xml_reader.name()
        attributes = __get_attribute_string(xml_reader.attributes())
        if xml_reader.isEndElement():
            slash = '/'
        else:
            slash = ''
        if not name == '':
            result += f'<{slash}{name} {attributes}>'
        text = xml_reader.text()
        if not text == '':
            result += text
        xml_reader.readNext()
    result += f'</{xml_reader.name()}>'
    print(result)
