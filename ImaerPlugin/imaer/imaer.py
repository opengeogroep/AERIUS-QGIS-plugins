import xml.etree.ElementTree as ET
import xml.dom.minidom
from xml.dom.minidom import parseString



# constants
_gml_ns = 'http://www.opengis.net/gml/3.2'
_imaer_ns = 'http://imaer.aerius.nl/2.2'
_imaer_schema_location = 'http://imaer.aerius.nl/2.2/IMAER.xsd'
_gml_id = 'NL.IMAER.Collection'


class FeatureCollectionCalculator():

    def __init__(self):
        self.metadata = None
        self.feature_members = []

    def generate_dom(self):
        doc = xml.dom.minidom.Document()
        fcc = doc.createElementNS(_imaer_ns, 'imaer:FeatureCollectionCalculator')

        fcc.setAttribute('xsi:schemaLocation',
                         '{} {}'.format(_imaer_ns, _imaer_schema_location))
        fcc.setAttribute('xmlns:imaer', _imaer_ns)
        fcc.setAttribute('xmlns:gml', _gml_ns)
        fcc.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        fcc.setAttribute('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        fcc.setAttribute('xmlns:xlink', 'http://www.w3.org/1999/xlink')
        fcc.setAttribute('gml:id', _gml_id)

        doc.appendChild(fcc)

        comment = doc.createComment('Created using QGIS ImaerPlugin by OpenGeoGroep')
        doc.appendChild(comment)

        #print(result)
        return doc

    def get_pretty_xml(self):
        data = self.generate_dom()
        return data.toprettyxml(indent='  ', newl='\n', encoding=None)
