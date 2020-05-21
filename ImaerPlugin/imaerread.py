from xml.dom import pulldom
import os

# constants
_resultTypes = ['CONCENTRATION','DEPOSITION']
_substances = ['NH3','NOX','NO2','PM10','PM25']




class ImaerRead():
    '''Exposes an IMAER-gml with calculator results as a featureCollection
       from which features can be fetched with the nextFeature Method'''

    def __init__(self, gmlFile):
        self.gmlFile = gmlFile
        _gml = open(gmlFile, 'rb')
        self.gml = _gml
        self._filesize = float(os.fstat(_gml.fileno()).st_size)
        self._doc = pulldom.parse(_gml)
        self.numFeatures = 0


    @property
    def attributeFields(self):
        """Returns the attributes which can be returned in the features"""
        attributes = []
        for result_type in _resultTypes:
            for substance in _substances:
                attributes.append("{}_{}".format(result_type[0:3], substance))
        return attributes


    def _getFullNodeValue(self, node):
        '''Get full text value and handles the case where the parser splits the text
        in parts by the read buffer:
        https://bugs.python.org/issue38011
        '''
        return ''.join(t.nodeValue for t in node.childNodes if t.nodeType == t.TEXT_NODE)


    def nextFeature(self, doPoints=True, doHexagons=True):
        """Returns the next ReceptorPoint as a feature"""
        _nextReceptorPoint = False
        for event, node in self._doc:
            if event == pulldom.START_ELEMENT and node.tagName == 'imaer:ReceptorPoint':
                self._doc.expandNode(node)
                #print(node.toxml())

                data = {}

                id = node.getAttribute('receptorPointId')
                data['id'] = id

                if doPoints:
                    ele = node.getElementsByTagName('gml:pos')[0]
                    data['point'] = 'POINT({})'.format(self._getFullNodeValue(ele))

                if doHexagons:
                    ele = node.getElementsByTagName('gml:posList')[0]
                    #pretty costly way to replace every second space by a comma...
                    gml_coords = self._getFullNodeValue(ele)
                    gml_numbers = gml_coords.split()
                    if not len(gml_numbers) == 14:
                        print(gml_numbers)
                    wkt_coord_list = []
                    i = 0
                    while i < len(gml_numbers):
                        wkt_coord_list.append('{} {}'.format(gml_numbers[i], gml_numbers[i+1]))
                        i += 2
                    wkt_coords = ', '.join(wkt_coord_list)
                    data['hexagon'] = 'POLYGON(({}))'.format(wkt_coords)

                results = node.getElementsByTagName('imaer:Result')
                for result_node in results:
                    result_type = result_node.getAttribute('resultType')
                    result_substance = result_node.getAttribute('substance')
                    key = '{}_{}'.format(result_type[:3], result_substance)
                    value_node = result_node.getElementsByTagName('imaer:value')[0]
                    data[key] = float(self._getFullNodeValue(value_node))

                # calculate parse progress by readposition and filesize
                pos = self.gml.tell()
                data['progress'] = pos / self._filesize

                self.numFeatures += 1
                return data

        return False


    def __del__(self):
        """Close gml file when cleaning up instance"""
        print('deleting ImaerRead object')
        try:
            self._gml.close()
        except:
            pass
