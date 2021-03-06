import xml.etree.ElementTree as ET
import xml.dom.minidom


_gml_ns = 'http://www.opengis.net/gml/3.2'
_imaer_ns = 'http://imaer.aerius.nl/3.1'

class GmlWriter():

    def __init__(self, geometry, local_id, srid):
        self.geometry = geometry
        self.local_id = local_id
        self.srid = srid


    def as_gml3(self):
        #print(self.geometry.type())
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
        gml_ele.setAttribute('srsName', 'urn:ogc:def:crs:EPSG::{0}'.format(self.srid))
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
        gm_ele = doc.createElementNS(_imaer_ns, 'imaer:GM_Curve')
        gml_ele = doc.createElementNS(_gml_ns, 'gml:LineString')
        gml_ele.setAttribute('srsName', 'urn:ogc:def:crs:EPSG::{0}'.format(self.srid))
        gml_ele.setAttribute('gml:id', '{0}.CURVE'.format(self.local_id))
        pos_ele = doc.createElementNS(_gml_ns, 'gml:posList')

        polyline = self.geometry.asPolyline()
        pos_list_str = self.polyline_to_poslist(polyline)
        pos_ele.appendChild(doc.createTextNode(pos_list_str))

        gml_ele.appendChild(pos_ele)
        gm_ele.appendChild(gml_ele)

        return gm_ele


    def as_gml3_polygon(self):
        doc = xml.dom.minidom.Document()
        gm_ele = doc.createElementNS(_imaer_ns, 'imaer:GM_Surface')
        gml_ele = doc.createElementNS(_gml_ns, 'gml:Polygon')
        gml_ele.setAttribute('srsName', 'urn:ogc:def:crs:EPSG::{0}'.format(self.srid))
        gml_ele.setAttribute('gml:id', '{0}.SURFACE'.format(self.local_id))
        ext_ele = doc.createElementNS(_gml_ns, 'gml:exterior')
        ring_ele = doc.createElementNS(_gml_ns, 'gml:LinearRing')
        pos_ele = doc.createElementNS(_gml_ns, 'gml:posList')

        polyline = self.geometry.get()[0].exteriorRing()
        pos_list_str = self.polyline_to_poslist(polyline)
        pos_ele.appendChild(doc.createTextNode(pos_list_str))

        # TODO Add interior rings??

        ring_ele.appendChild(pos_ele)
        ext_ele.appendChild(ring_ele)
        gml_ele.appendChild(ext_ele)
        gm_ele.appendChild(gml_ele)

        return gm_ele


    def polyline_to_poslist(self, polyline):
        pos_list = []
        for pnt in polyline:
            pos = '{} {}'.format(pnt.x(), pnt.y())
            pos_list.append(pos)
        pos_list_str = ' '.join(pos_list)
        return pos_list_str
