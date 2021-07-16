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


class ParameterDef():

    def __init__(self, name, type, label=None, min_occurs=0, max_occurs=1, default_value=None):
        self.name = name
        self.type = type # GROUP, VALUE

        if label is None:
            self.label = name
        else:
            self.label = label

        self.min_occurs = min_occurs
        self.max_occurs = max_occurs
        self.default_value = default_value

        self.children = []


    def __str__(self):
        result = 'ParameterDef[{}, {}, {}, ({}..{}), {}, children:{}]'.format(
            self.name,
            self.type,
            self.label,
            self.min_occurs,
            self.max_occurs,
            self.default_value,
            len(self.children)
        )
        return result

    def to_string(self, indent=0, indentation_width=2):
        result = ''
        result += (' ' * indent) + str(self) + '\n'
        for child in self.children:
            result += child.to_string(indent+indentation_width, indentation_width)
        return result


    def append_child(self, child):
        self.children.append(child)
