import xml.etree.ElementTree as ET
import xml.dom.minidom


_gml_ns = 'http://www.opengis.net/gml/3.2'
_imaer_ns = 'http://imaer.aerius.nl/3.1'

class GmlWriter():

    def __init__(self, geometry, local_id, epsg=28992):
        self.geometry = geometry
        self.local_id = local_id
        self.epsg = epsg


    def as_gml3(self):
        print(self.geometry.type())
        if self.geometry.type() == 0:
            gml3 = self.as_gml3_point()
        elif self.geometry.type() == 1:
            gml3 = self.as_gml3_linestring()
        elif self.geometry.type() == 2:
            gml3 = self.as_gml3_polygon()
        else:
            return None
        return gml3


    def as_gml3_point(self):
        doc = xml.dom.minidom.Document()
        gm_ele = doc.createElementNS(_imaer_ns, 'imaer:GM_Point')
        gml_ele = doc.createElementNS(_gml_ns, 'gml:Point')
        gml_ele.setAttribute('srsName', 'urn:ogc:def:crs:EPSG::{0}'.format(self.epsg))
        gml_ele.setAttribute('gml:id', '{0}.POINT'.format(self.local_id))
        pos_ele = doc.createElementNS(_gml_ns, 'gml:pos')
        coord_str = '{} {}'.format(
            self.geometry.asPoint().x(),
            self.geometry.asPoint().y())
        pos_ele.appendChild(doc.createTextNode(coord_str))
        gml_ele.appendChild(pos_ele)
        gm_ele.appendChild(gml_ele)

        return gm_ele


    def as_gml3_linestring(self):
        doc = xml.dom.minidom.Document()
        return  doc.createComment(' === LINESTRING NOT YET IMPLEMENTED :( ===')


    def as_gml3_polygon(self):
        doc = xml.dom.minidom.Document()
        return  doc.createComment(' === POLYGON NOT YET IMPLEMENTED :( ===')
