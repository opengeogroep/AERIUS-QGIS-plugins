from .generic import namespaces, ET, find_xml_value




class FeatureCollectionCalculator():

    def __init__(self, elem=None):
        self.metadata = None
        self.feature_members = []

        if elem is not None: # and isinstance()
            self.from_xml_element_base(elem)


    def __str__(self):
        result = 'FeatureCollectionCalculator[{}, feature_members:{}]'.format(
            self.metadata,
            len(self.feature_members)
        )
        return result


    def from_xml_element_base(self, elem): # _base added to prevent overriding by the child classes
        self.metadata = find_xml_value(elem, 'imaer:metadata')


    def get_gui_nodes(self):
        result = GuiNode('main', 'GROUP')

        metadata_nodes = AeriusCalculatorMetadata().get_gui_nodes()
        metadata_nodes.min_occurs = 1
        result.append_child(metadata_nodes)

        return result
