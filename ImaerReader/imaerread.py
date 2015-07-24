from xml.dom import pulldom

# constants
_resultTypes = ['CONCENTRATION','DEPOSITION']
_substances = ['NH3','NOX','NO2','PM10','PM25']

class ImaerRead():
    '''Exposes an IMAER-gml with calculator results as a featureCollection 
       from which features can be fetched with the nextFeature Method'''
    def __init__(self, gmlFile):
        self.gmlFile = gmlFile
        _gml = open(gmlFile)
        self.events = pulldom.parse(_gml)
        self.numFeatures = 0

    @property
    def AttributeFields(self):
        """Returns the attributes which can be returned in the features"""
        attributes = []
        for type in _resultTypes:
            for substance in _substances:
                attributes.append("%s_%s" %(type[0:3],substance))
        return attributes

    def nextFeature(self, doPoints=True, doHexagons=True):
        """Returns the next ReceptorPoint as a feature"""
        event, node = self.events.next()
        _nextReceptorPoint = False
        while event:
            if event == pulldom.START_ELEMENT and node.tagName == 'imaer:ReceptorPoint':
                id = node.getAttribute('receptorPointId')
                data = {}
                data['id'] = id
                _nextReceptorPoint = True
            
            if doPoints:
                if _nextReceptorPoint and event == pulldom.START_ELEMENT and node.tagName == 'gml:pos':
                    txt = ''
                    while not event == pulldom.END_ELEMENT:
                        # we have to wait for the END event as the SAX-parser may split CHARACTER events
                        # see http://bugs.python.org/issue10026 and http://www.mail-archive.com/xml-sig@python.org/msg00263.html
                        event, node = self.events.next()
                        if event == pulldom.CHARACTERS:
                            txt = txt + node.wholeText
                    data['point'] = 'POINT(%s)' % txt

            if doHexagons:
                if _nextReceptorPoint and event == pulldom.START_ELEMENT and node.tagName == 'gml:posList':
                    txt = ''
                    while not event == pulldom.END_ELEMENT:
                        # we have to wait for the END event as the SAX-parser may split CHARACTER events
                        event, node = self.events.next()
                        if event == pulldom.CHARACTERS:
                            txt = txt + node.wholeText
                    s = txt.strip().split()
                    data['hexagon'] = 'POLYGON((%s))' %  ','.join(map(' '.join, zip(s[::2], s[1::2])))
                
            if _nextReceptorPoint and event == pulldom.START_ELEMENT and node.tagName == 'imaer:Result':
                type = node.getAttribute('resultType')
                substance = node.getAttribute('substance')
                txt = ''
                while not event == pulldom.END_ELEMENT:
                    # we have to wait for the END event as the SAX-parser may split CHARACTER events
                    event, node = self.events.next()
                    if event == pulldom.CHARACTERS:
                        txt = txt + node.wholeText
                data["%s_%s" %(type[0:3],substance)] = float(txt)

            if event == pulldom.END_ELEMENT and node.tagName == 'imaer:ReceptorPoint':
                # we have a complete feature
                self.numFeatures = self.numFeatures + 1
                return data
                
            try:
                event, node = self.events.next()
            except:
                event = False
        return False
