from PyQt5.QtXml import QDomDocument

from .roads import RoadEmissionSource


class SRM2Road(RoadEmissionSource):

    def __init__(self, *, tunnel_factor=None, elevation=None, elevation_height=None, **kwargs):
        super().__init__(**kwargs)
        self.tunnel_factor = tunnel_factor
        self.elevation = elevation
        self.elevation_height = elevation_height
        self.barrier_left = None
        self.barrier_right = None

    def to_xml_elem(self, doc=QDomDocument()):
        result = super().to_xml_elem(doc)

        if self.tunnel_factor is not None:
            elem = doc.createElement('imaer:tunnelFactor')
            elem.appendChild(doc.createTextNode(str(self.tunnel_factor)))
            result.appendChild(elem)

        if self.elevation is not None:
            elem = doc.createElement('imaer:elevation')
            elem.appendChild(doc.createTextNode(str(self.elevation)))
            result.appendChild(elem)

        if self.elevation_height is not None:
            elem = doc.createElement('imaer:elevationHeight')
            elem.appendChild(doc.createTextNode(str(self.elevation_height)))
            result.appendChild(elem)

        if self.barrier_left is not None:
            b_elem = doc.createElement('imaer:barrierLeft')
            elem = self.barrier_left.to_xml_elem(doc)
            b_elem.appendChild(elem)
            result.appendChild(b_elem)

        if self.barrier_right is not None:
            b_elem = doc.createElement('imaer:barrierRight')
            elem = self.barrier_right.to_xml_elem(doc)
            b_elem.appendChild(elem)
            result.appendChild(b_elem)

        return result


class Srm2RoadSideBarrier(object):

    def __init__(self, type, height, distance):
        self.type = type
        self.height = height
        self.distance = distance

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:RoadSideBarrier')

        elem = doc.createElement('imaer:barrierType')
        elem.appendChild(doc.createTextNode(str(self.type)))
        result.appendChild(elem)

        elem = doc.createElement('imaer:height')
        elem.appendChild(doc.createTextNode(str(self.height)))
        result.appendChild(elem)

        elem = doc.createElement('imaer:distance')
        elem.appendChild(doc.createTextNode(str(self.distance)))
        result.appendChild(elem)

        return result
