import xml.dom.minidom
import re
import inspect
import sys

# constants
_gmlNS = "http://www.opengis.net/gml/3.2"
_imaerNS = "http://imaer.aerius.nl/1.0"
_imaerSchemaLocation = "http://imaer.aerius.nl/1.0/IMAER.xsd"

class ImaerWrite():
    '''The class that wraps up all features created by the other classes'''
    def __init__(self, gmlId = "NL.IMAER.Collection", features = []):
        self.features = features
        self.gmlId = gmlId
    
    @property
    def _imaerNS(self):
        return _imaerNS     
    
    @property
    def _imaerSchemaLocation(self):
        return _imaerSchemaLocation  
    
    @property
    def _gmlNS(self):
        return _gmlNS
    
    def  __str__(self):
        finaldom = self.dom
        uglyXml = finaldom.toprettyxml(indent='  ', encoding="UTF-8")
        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)
        prettyXml = text_re.sub('>\g<1></', uglyXml)
        return prettyXml
    
    @property
    def EmissionSourceTypes(self):
        '''Returns the implemented emission source types'''
        return ["EmissionSource"]

    @property
    def dom(self):
        doc = xml.dom.minidom.Document()
        fcc = doc.createElementNS(_imaerNS,"imaer:FeatureCollectionCalculator")
        fcc.setAttribute("xsi:schemaLocation",
                         "%s %s" %(self._imaerNS, self._imaerSchemaLocation))
        fcc.setAttribute("xmlns:imaer", self._imaerNS)
        fcc.setAttribute("xmlns:gml", self._gmlNS)
        fcc.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
        fcc.setAttribute("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        fcc.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink")
        fcc.setAttribute("gml:id", self.gmlId)
        _comment = doc.createComment("Created using imaerwrite.py by OpenGeoGroep")
        fcc.appendChild(_comment)
        
        _featureMembers = doc.createElementNS(_imaerNS,"imaer:featureMembers")
        for feature in self.features:
            _featureMembers.appendChild(feature.dom) 
        
        fcc.appendChild(_featureMembers)
        doc.appendChild(fcc)
        return doc

    def save(self, fn):
        '''saves xml to file'''
        with open(fn, 'w') as outfile:
            outfile.write(str(self))

    def addFeature(self, feature):
        self.features.append(feature)

    def getUiFields(self, emissionSourceType = False, emissionSourceCharacteristics = False):
        '''Returns the needed fields to provide the constructors with objects and parameters to create a feature'''
        
        ### This might suggests that it is possible to generate a gui completely from object properties. ###
        ### That is not the case. Layout and intercopnnections of gui elements are vital and cannot be   ###
        ### derived from the object properties. But things are easier to maintain in this manner.        ###
 
        uiFields = {}
        if not (emissionSourceType or emissionSourceCharacteristics):
            uiFields = {'Emission': _EmissionSourceType.Emission.UI_FIELDS}
        if emissionSourceType:
            uiFields[emissionSourceType] = (['gmlId'],['label'])
        if emissionSourceCharacteristics:
            uiFields['EmissionSourceCharacteristics'] = _EmissionSourceType.EmissionSourceCharacteristics.UI_FIELDS
                       
        return uiFields

class _EmissionSourceType():
    '''Base class for subclassing'''

    def __init__(self, wktGeometry, gmlId, sectorId, label = None, emissionSourceCharacteristics = None):
        if not gmlId:
            raise ValueError("EmissionSource:gmlId cannot be empty")
        if not gmlId[0:3] == 'ES.':
            gmlId = 'ES.%s' % gmlId
        _idCheck = re.compile(r'^[a-zA-Z_][\w.-]*$')
        if not _idCheck.match(str(gmlId)):
            raise ValueError("EmissionSource:gmlId of '%s' not allowed (It can only contain letters, digits, underscores, hyphens, and periods)" % gmlId)
        self.emissionSourceCharacteristics = emissionSourceCharacteristics
        self.wktGeometry = wktGeometry
        self.label = label
        if label:
            self.label = str(label)
        self.sectorId = str(sectorId)
        self.gmlId = str(gmlId)
        self.emissions = []

    @property
    def sourceLabel(self):
        if self.label:
            doc = xml.dom.minidom.Document()
            label = doc.createElementNS(_imaerNS,"imaer:label")
            label.appendChild(doc.createTextNode(self.label))
        return label

    @property
    def identifier(self):
        _idCheck = re.compile(r'^[a-zA-Z_][\w.-]*$')
        if not _idCheck.match(str(self.gmlId)):
            raise ValueError("EmissionSource:gmlId of '%s' not allowed (It can only contain letters, digits, underscores, hyphens, and periods)" % self.gmlId)

        doc = xml.dom.minidom.Document()
        identifier = doc.createElementNS(_imaerNS,"imaer:identifier")
        _nen3610ID = doc.createElementNS(_imaerNS,"imaer:NEN3610ID")
        
        _namespace = doc.createElementNS(_imaerNS,"imaer:namespace")
        _namespace.appendChild(doc.createTextNode('NL.IMAER'))
        _nen3610ID.appendChild(_namespace)
        
        _localid = doc.createElementNS(_imaerNS,"imaer:localId")
        _localid.appendChild(doc.createTextNode(self.gmlId))
        _nen3610ID.appendChild(_localid)

        identifier.appendChild(_nen3610ID)
        return identifier

    @property
    def geometry(self):
        '''
        Returns a domNode containing Imaer gml geometry'''
              
        if self.wktGeometry:
            return self.getImaerGeomFromWkt(self.wktGeometry, self.gmlId)

    def getImaerGeomFromWkt(self, wktGeometry, gmlId):
        '''
        Creates a valid IMAER geometry domNode from a wkt geometry.
        This wkt geometry must be in EPSG:28992, 
        have a type of 'POINT','LINESTRING' or 'POLYGON'
        and have a precision of 3.'''

        doc = xml.dom.minidom.Document()
        geometry = doc.createElementNS(_imaerNS,"imaer:geometry")
        _emissionSourceGeometry = doc.createElementNS(_imaerNS,"imaer:EmissionSourceGeometry")
        _point = doc.createElementNS(_imaerNS,"imaer:GM_Point")
        _curve = doc.createElementNS(_imaerNS,"imaer:GM_Curve")
        _surface = doc.createElementNS(_imaerNS,"imaer:GM_Surface")

        _wkt = _WKTParser()
        _wktGeomType, _posLists = _wkt(self.wktGeometry, True)

        if _wktGeomType == 'point':
            _gmlPoint = doc.createElementNS(_gmlNS,"gml:Point")
            _gmlPoint.setAttributeNS(_gmlNS, 'gml:id', '%s.POINT' % self.gmlId)
            _gmlPos = doc.createElementNS(_gmlNS, "gml:pos")
            _gmlPos.appendChild(doc.createTextNode(_posLists))
            _gmlPoint.appendChild(_gmlPos)
            _point.appendChild(_gmlPoint)
            _emissionSourceGeometry.appendChild(_point)
        if _wktGeomType == 'linestring':
            _gmlLine = doc.createElementNS(_gmlNS,"gml:LineString")
            _gmlLine.setAttributeNS(_gmlNS, 'gml:id', '%s.LINE' % self.gmlId)
            _gmlPosList = doc.createElementNS(_gmlNS, "gml:posList")
            _gmlPosList.appendChild(doc.createTextNode(_posLists))
            _gmlLine.appendChild(_gmlPosList)
            _curve.appendChild(_gmlLine)
            _emissionSourceGeometry.appendChild(_curve)
        if _wktGeomType == 'polygon':
            _gmlPoly = doc.createElementNS(_gmlNS,"gml:Polygon")
            _gmlPoly.setAttributeNS(_gmlNS, 'gml:id', '%s.POLYGON' % self.gmlId)
            _gmlExterior = doc.createElementNS(_gmlNS,"gml:exterior")
            _gmlRing = doc.createElementNS(_gmlNS,"gml:LinearRing")
            _gmlPosList = doc.createElementNS(_gmlNS, "gml:posList")
            _gmlPosList.appendChild(doc.createTextNode(_posLists[0]))
            _gmlRing.appendChild(_gmlPosList)
            _gmlExterior.appendChild(_gmlRing)
            _gmlPoly.appendChild(_gmlExterior)
            for _posList in _posLists[1:]:
                _gmlInterior = doc.createElementNS(_gmlNS,"gml:interior")
                _gmlRing = doc.createElementNS(_gmlNS,"gml:LinearRing")
                _gmlPosList = doc.createElementNS(_gmlNS, "gml:posList")
                _gmlPosList.appendChild(doc.createTextNode(_posList))
                _gmlRing.appendChild(_gmlPosList)
                _gmlInterior.appendChild(_gmlRing)
                _gmlPoly.appendChild(_gmlInterior)
                
            _surface.appendChild(_gmlPoly)
            _emissionSourceGeometry.appendChild(_surface)

        geometry.appendChild(_emissionSourceGeometry)
        return geometry
    
    def addEmission(self, emission):
        self.emissions.append(emission)
                
    class Emission():
        UI_FIELDS = ([],['NH3','NO2','NOX','PM10','PM25'])
          
        def __init__(self,substance,value):
            _SUBSTANCES = ['NH3','NO2','NOX','PM10','PM25']
            if not substance in _SUBSTANCES:
                raise ValueError("Emission: Substance must be one of %s" % _SUBSTANCES)
            self.substance = substance
            self.value = str(value)
        
        def  __str__(self):
            return self.dom.toprettyxml(indent='  ', encoding="UTF-8")
        
        @property
        def dom(self):
            doc = xml.dom.minidom.Document()
            emission = doc.createElementNS(_imaerNS,"imaer:emission")
            _Emission = doc.createElementNS(_imaerNS,"imaer:Emission")
            _Emission.setAttribute('substance', self.substance)
            
            _value = doc.createElementNS(_imaerNS,"imaer:value")
            _value.appendChild(doc.createTextNode( self.value ))
            
            _Emission.appendChild(_value)
            emission.appendChild(_Emission)
            return emission
        
    class EmissionSourceCharacteristics():
        UI_FIELDS = (['heatContent', 'emissionHeight'],['buildingHeight','spread','diurnalVariation'])
        
        def __init__(self, heatContent,
                           emissionHeight,
                           buildingHeight = None,
                           spread = None,
                           diurnalVariation = None ):
            _DIURNAL_VARIATIONS = ["CONTINUOUS","INDUSTRIAL_ACTIVITY","SPACE_HEATING","TRAFFIC","ANIMAL_HOUSING","FERTILISER"]
            if diurnalVariation and not diurnalVariation in _DIURNAL_VARIATIONS:
                raise ValueError("EmissionSourceCharacteristics:diurnalVariation value must be one of %s" % _DIURNAL_VARIATIONS)
            if not heatContent and not heatContent == 0:
                raise ValueError("EmissionSourceCharacteristics:heatContent cannot be empty")
            if not emissionHeight and not emissionHeight == 0:
                raise ValueError("EmissionSourceCharacteristics:emissionHeight cannot be empty")
            
            self.heatContent = heatContent
            self.emissionHeight = emissionHeight
            self.buildingHeight = buildingHeight
            self.spread = spread
            self.diurnalVariation = diurnalVariation
            
        def  __str__(self):
            return self.dom.toprettyxml(indent='  ', encoding="UTF-8")
        
        @property
        def dom(self):
            doc = xml.dom.minidom.Document()
            emissionSourceCharacteristics = doc.createElementNS(_imaerNS,"imaer:emissionSourceCharacteristics")
            _EmissionSourceCharacteristics = doc.createElementNS(_imaerNS,"imaer:EmissionSourceCharacteristics")
            if self.heatContent or self.heatContent == 0:
                _heatContent = doc.createElementNS(_imaerNS,"imaer:heatContent")
                _heatContent.appendChild(doc.createTextNode( str(self.heatContent) ))
                _EmissionSourceCharacteristics.appendChild(_heatContent)
            if self.emissionHeight or self.emissionHeight == 0:
                _emissionHeight = doc.createElementNS(_imaerNS,"imaer:emissionHeight")
                _emissionHeight.appendChild(doc.createTextNode( str(self.emissionHeight) ))
                _EmissionSourceCharacteristics.appendChild(_emissionHeight)
            if self.buildingHeight or self.buildingHeight == 0:
                _buildingHeight = doc.createElementNS(_imaerNS,"imaer:buildingHeight")
                _buildingHeight.appendChild(doc.createTextNode( str(self.buildingHeight) ))
                _EmissionSourceCharacteristics.appendChild(_buildingHeight)    
            if self.spread or self.spread == 0:
                _spread = doc.createElementNS(_imaerNS,"imaer:spread")
                _spread.appendChild(doc.createTextNode( str(self.spread) ))
                _EmissionSourceCharacteristics.appendChild(_spread)    
            if self.diurnalVariation:
                _diurnalVariation = doc.createElementNS(_imaerNS,"imaer:diurnalVariation")
                _diurnalVariation.appendChild(doc.createTextNode( str(self.diurnalVariation) ))
                _EmissionSourceCharacteristics.appendChild(_diurnalVariation)
            emissionSourceCharacteristics.appendChild(_EmissionSourceCharacteristics)
            return emissionSourceCharacteristics
                 
class EmissionSource(_EmissionSourceType):
    '''Class defining emission sources with emissions (sectorId 9999)'''
    
    UI_FIELDS = (['gmlId'],['label'])
        
    def __init__(self, wktGeometry, gmlId, label = None, emissionSourceCharacteristics = None):
        _EmissionSourceType.__init__(self, wktGeometry = wktGeometry, label = label, gmlId = gmlId, 
                                     sectorId = 9999, emissionSourceCharacteristics = emissionSourceCharacteristics)
                                    
    def  __str__(self):
        return self.dom.toprettyxml(indent='  ', encoding="UTF-8")
    
    @property
    def dom(self):
        doc = xml.dom.minidom.Document()
        EmissionSource = doc.createElementNS(_imaerNS,"imaer:EmissionSource")
        EmissionSource.setAttribute('sectorId', self.sectorId)
        EmissionSource.setAttribute('gml:id', self.gmlId)
        EmissionSource.appendChild(self.identifier)
        if self.label:
            EmissionSource.appendChild(self.sourceLabel)
        if self.emissionSourceCharacteristics:
            EmissionSource.appendChild(self.emissionSourceCharacteristics.dom)
        EmissionSource.appendChild(self.geometry)
        for emission in self.emissions:
            EmissionSource.appendChild(emission.dom)
    
        return EmissionSource
 
class _WKTParser:
    """ Private class to grab gml posList and geoType from WKT
        Modified from pysal which is Modified from... 
        #URL: http://dev.openlayers.org/releases/OpenLayers-2.7/lib/OpenLayers/Format/WKT.js
        #Reg Ex Strings copied from OpenLayers.Format.WKT
    """
    regExes = {'typeStr': re.compile('^\s*([\w\s]+)\s*\(\s*(.*)\s*\)\s*$'),
               'spaces': re.compile('\s+'),
               'parenComma': re.compile('\)\s*,\s*\('),
               'doubleParenComma': re.compile('\)\s*\)\s*,\s*\(\s*\('),  # can't use {2} here
               'trimParens': re.compile('^\s*\(?(.*?)\)?\s*$')}

    def __init__(self):
        self.parsers = p = {}
        p['point'] = self.Point
        p['linestring'] = self.LineString
        p['polygon'] = self.Polygon

    def Point(self, geoStr):
        return geoStr.strip()

    def LineString(self, geoStr):
        return geoStr.strip().replace(',',' ')

    def Polygon(self, geoStr):
        rings = self.regExes['parenComma'].split(geoStr.strip())
        for i, ring in enumerate(rings):
            ring = self.regExes['trimParens'].match(ring).groups()[0]
            ring = self.LineString(ring)
            rings[i] = ring
        return rings
        
    def fromWKT(self, wkt, returnGeoType = False):
        matches = self.regExes['typeStr'].match(wkt)
        if matches:
            geoType, geoStr = matches.groups()
            geoType = geoType.lower().strip()
            try:
                if returnGeoType:
                    return geoType, self.parsers[geoType](geoStr)
                else:
                    return self.parsers[geoType](geoStr)
            except KeyError:
                raise NotImplementedError("Unsupported WKT Type: %s" % geoType)
        else:
            return None
    
    __call__ = fromWKT
   