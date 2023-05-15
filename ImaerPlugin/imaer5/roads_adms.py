from PyQt5.QtXml import QDomDocument

from .roads import RoadEmissionSource


class ADMSRoad(RoadEmissionSource):

    def __init__(self, *, tunnel_factor=None, elevation=None,
                 elevation_height=None, gradient=None, width=None,
                 coverage=None, **kwargs):
        super().__init__(**kwargs)
        self.tunnel_factor = tunnel_factor
        self.elevation = elevation
        self.elevation_height = elevation_height
        self.gradient = gradient
        self.width = width
        self.coverage = coverage
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

        if self.gradient is not None:
            elem = doc.createElement('imaer:gradient')
            elem.appendChild(doc.createTextNode(str(self.gradient)))
            result.appendChild(elem)

        if self.width is not None:
            elem = doc.createElement('imaer:width')
            elem.appendChild(doc.createTextNode(str(self.width)))
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

        return result


class AdmsRoadSideBarrier(object):

    def __init__(self, type, distance, Avheight, Maxheight, Minheight, porosity):
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


class Vehicle(object):

    def __init__(self, *, vehicles_per_time_unit=None, time_unit=None, **kwargs):
        self.vehicles_per_time_unit = vehicles_per_time_unit
        self.time_unit = time_unit

    def to_xml_elem(self, doc=QDomDocument()):

        class_name = self.__class__.__name__
        result = doc.createElement(f'imaer:{class_name}')

        elem = doc.createElement('imaer:vehiclesPerTimeUnit')
        elem.appendChild(doc.createTextNode(str(self.vehicles_per_time_unit)))
        result.appendChild(elem)

        elem = doc.createElement('imaer:timeUnit')
        elem.appendChild(doc.createTextNode(str(self.time_unit)))
        result.appendChild(elem)

        return result


class StandardVehicle(Vehicle):

    def __init__(self, *, stagnation_factor=None, vehicle_type=None, maximum_speed=None, strict_enforcement=None, **kwargs):
        super().__init__(**kwargs)
        self.stagnation_factor = stagnation_factor
        self.vehicle_type = vehicle_type
        self.maximum_speed = maximum_speed
        self.strict_enforcement = strict_enforcement

    def to_xml_elem(self, doc=QDomDocument()):
        result = super().to_xml_elem(doc)
        result.setAttribute('vehicleType', self.vehicle_type)

        if self.stagnation_factor is not None:
            elem = doc.createElement('imaer:stagnationFactor')
            elem.appendChild(doc.createTextNode(str(self.stagnation_factor)))
            result.appendChild(elem)
        else:
            elem = doc.createElement('imaer:stagnationFactor')
            elem.appendChild(doc.createTextNode('0.0'))
            result.appendChild(elem)

        if self.maximum_speed is not None:
            elem = doc.createElement('imaer:maximumSpeed')
            elem.appendChild(doc.createTextNode(str(self.maximum_speed)))
            result.appendChild(elem)

        if self.strict_enforcement is not None:
            elem = doc.createElement('imaer:strictEnforcement')
            elem.appendChild(doc.createTextNode(str(self.strict_enforcement)))
            result.appendChild(elem)
        else:
            elem = doc.createElement('imaer:strictEnforcement')
            elem.appendChild(doc.createTextNode(str('false')))
            result.appendChild(elem)

        return result
