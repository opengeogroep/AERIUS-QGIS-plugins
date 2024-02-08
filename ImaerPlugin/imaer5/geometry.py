import sys

from PyQt5.QtXml import QDomDocument

from qgis.core import QgsPoint

#path_qgis_python_folder = "/home/raymond/programs/qgis/qgis-master/share/qgis/python/"
#sys.path.append(path_qgis_python_folder)
#from qgis.core import QgsGeometry


class GmlGeometry():

    def __init__(self, epsg_id=None, gml_id=None):
        self.epsg_id = epsg_id
        self.gml_id = gml_id

    def __str__(self):
        return f'Geometry[{self.geom}, {self.epsg_id, self.gml_id}]'

    def from_xml_reader(self, xml_reader):
        if not xml_reader.isStartElement():
            return
        attributes = xml_reader.attributes()
        if attributes.hasAttribute('srsName'):
            srs_name = attributes.value('srsName')
            self.epsg_id = srs_name.split(':')[-1] 
        if attributes.hasAttribute('gml:id'):
            self.gml_id = attributes.value('gml:id')

    def is_valid(self):
        return True


class GmlPoint(GmlGeometry):

    def __init__(self, *, x=None, y=None):
        super().__init__()
        self.x = x
        self.y = y

    def __str__(self):
        return f'GmlPoint[{self.epsg_id}, {self.gml_id}, {self.x:.3f}, {self.y:.3f}]'
    
    def from_xml_reader(self, xml_reader):
        super().from_xml_reader(xml_reader)

        start_name = xml_reader.name()
        if start_name == 'Point':
            xml_reader.readNextStartElement()
            if xml_reader.name() == 'pos':
                xml_reader.readNext()
                coords = xml_reader.text()
                parts = coords.split()
                self.x = float(parts[0])
                self.y = float(parts[1])
    
    def to_geometry(self):
        return QgsPoint(round(self.x, 3), round(self.y, 3))


class GmlLineString(GmlGeometry): # NEVER TESTED!!!

    def __init__(self, *, coords=None):
        super().__init__()
        self.coords = coords or []

    def __str__(self):
        return f'GmlLineString[{self.epsg_id}, {self.gml_id}, {len(self.coords)}, {self.coords[:4]}]'
    
    def from_xml_reader(self, xml_reader):
        super().from_xml_reader(xml_reader)

        start_name = xml_reader.name()
        if start_name == 'LineString':
            xml_reader.readNextStartElement()
            if xml_reader.name() == 'posList':
                xml_reader.readNext()
                coords = xml_reader.text()
                print(coords)
                parts = coords.split()
                for part in parts:
                    self.coords.append(float(part))


class GmlPolygon(GmlGeometry):

    def __init__(self, *, exterior=None):
        super().__init__()
        self.exterior = exterior or []

    def __str__(self):
        return f'GmlPolygon[{self.epsg_id}, {self.gml_id}, {len(self.exterior)}, {self.exterior[:4]}]'
    
    def from_xml_reader(self, xml_reader):
        super().from_xml_reader(xml_reader)
        if xml_reader.name() != 'Polygon':
            return
        xml_reader.readNextStartElement()
        if xml_reader.name() != 'exterior':
            return
        xml_reader.readNextStartElement()
        if xml_reader.name() == 'LinearRing':
            xml_reader.readNextStartElement()

            if xml_reader.name() == 'posList':
                xml_reader.readNext()
                coords = xml_reader.text()
                parts = coords.split()
                for part in parts:
                    self.exterior.append(float(parts[0]))

