from PyQt5.QtXml import QDomDocument

from .roads import RoadEmissionSource


class ADMSRoad(RoadEmissionSource):

    def __init__(self, *, width=None, elevation=None,
                 gradient=None, coverage=None, barrier_left=None,
                 barrier_right=None, diurnal_variation=None, **kwargs):
        super().__init__(**kwargs)
        self.width = width
        self.elevation = elevation
        self.gradient = gradient
        self.coverage = coverage
        self.barrier_left = barrier_left
        self.barrier_right = barrier_right
        self.diurnal_variation = diurnal_variation

    def to_xml_elem(self, doc=QDomDocument()):
        result = super().to_xml_elem(doc)

        if self.width is not None:
            elem = doc.createElement('imaer:width')
            elem.appendChild(doc.createTextNode(str(self.width)))
            result.appendChild(elem)

        if self.elevation is not None:
            elem = doc.createElement('imaer:elevation')
            elem.appendChild(doc.createTextNode(str(self.elevation)))
            result.appendChild(elem)

        if self.gradient is not None:
            elem = doc.createElement('imaer:gradient')
            elem.appendChild(doc.createTextNode(str(self.gradient)))
            result.appendChild(elem)

        if self.coverage is not None:
            elem = doc.createElement('imaer:coverage')
            elem.appendChild(doc.createTextNode(str(self.coverage)))
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

        if self.diurnal_variation is not None:
            dv_elem = doc.createElement('imaer:diurnalVariation')
            elem = self.diurnal_variation.to_xml_elem(doc)
            dv_elem.appendChild(elem)
            result.appendChild(dv_elem)
            
        return result


class AdmsRoadSideBarrier(object):

    def __init__(self, type, distance, Avheight, Maxheight, Minheight, porosity):
        self.tag = 'ADMSRoad'
        self.type = type
        self.distance = distance
        self.Avheight = Avheight
        self.Maxheight = Maxheight
        self.Minheight = Minheight
        self.porosity = porosity

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:ADMSRoadSideBarrier')

        elem = doc.createElement('imaer:barrierType')
        elem.appendChild(doc.createTextNode(str(self.type)))
        result.appendChild(elem)

        elem = doc.createElement('imaer:distance')
        elem.appendChild(doc.createTextNode(str(self.distance)))
        result.appendChild(elem)

        elem = doc.createElement('imaer:averageHeight')
        elem.appendChild(doc.createTextNode(str(self.Avheight)))
        result.appendChild(elem)

        elem = doc.createElement('imaer:maximumHeight')
        elem.appendChild(doc.createTextNode(str(self.Maxheight)))
        result.appendChild(elem)

        elem = doc.createElement('imaer:minimumHeight')
        elem.appendChild(doc.createTextNode(str(self.Minheight)))
        result.appendChild(elem)

        elem = doc.createElement('imaer:porosity')
        elem.appendChild(doc.createTextNode(str(self.porosity)))
        result.appendChild(elem)

        return result
