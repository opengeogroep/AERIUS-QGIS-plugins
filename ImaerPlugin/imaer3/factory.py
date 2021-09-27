import os

from .generic import ET, namespaces, remove_ns, find_xml_value
#from .well import GroundwaterMonitoringWell




class ImaerFactory():

    def __init__(self):
        self.request_type = None


    def __str__(self):
        result = 'ImaerFactory[]'.format(
        )
        return result


    def from_xml_file(self, fn):
        '''Returns a feature_collection_calculator object based on the xml file.'''
        if fn is None:
            return false
        print(f'Importing xml file: {fn}')

        root = ET.parse(fn).getroot()
        self.request_type = remove_ns(root.tag)
        print(self.request_type)

        source_doc = root.find('imaer:FeatureCollectionCalculator', namespaces)
        print(source_doc)

        if source_doc is None:
            print('Not a valid IMAER XML')
            return

        children = source_doc.getchildren()
        if len(children) == 0:
            print('No registration object in XML')
            return

        self.registration_object_type = remove_ns(children[0].tag)
        #print(self.registration_object_type)

        if self.registration_object_type == 'GMW_Construction':
            reg_obj = GroundwaterMonitoringWell(root)
        else:
            print(f'Unknown registration object type in xml file: {self.registration_object_type}')
            return

        print(reg_obj)

        #reg_obj.indented_print(8, '---')
        #print(reg_obj.get_dict())

        return reg_obj


    def to_xml_file(self, imaer_obj, fn):
        '''Creates an xml file for an imaer object.'''
        print(fn)

        output = imaer_obj.to_xml_text()

        with open(fn, 'w') as fl:
            fl.write(output)
