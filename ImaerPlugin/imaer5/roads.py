from PyQt5.QtXml import QDomDocument

from .emission_source import EmissionSourceType


class RoadEmissionSource(EmissionSourceType):
    def __init__(self, *, road_area_type, road_type, vehicles=[], traffic_direction=None, **kwargs):
        super().__init__(**kwargs)
        self.road_area_type = road_area_type
        self.road_type = road_type
        self.vehicles = vehicles
        self.traffic_direction = traffic_direction

    def to_xml_elem(self, doc=QDomDocument()):
        result = super().to_xml_elem(doc)

        for veh in self.vehicles:
            veh_elem = doc.createElement('imaer:vehicles')  # Somehow every vehicle should be in it's own vehicles element.
            elem = veh.to_xml_elem(doc)
            veh_elem.appendChild(elem)
            result.appendChild(veh_elem)

        if self.traffic_direction is not None:
            elem = doc.createElement('imaer:trafficDirection')
            elem.appendChild(doc.createTextNode(str(self.traffic_direction)))
            result.appendChild(elem)

        return result


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


class RoadSideBarrier(object):

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

        elem = doc.createElement('imaer:stagnationFactor')
        elem.appendChild(doc.createTextNode(str(self.stagnation_factor)))
        result.appendChild(elem)

        if self.maximum_speed is not None:
            elem = doc.createElement('imaer:maximumSpeed')
            elem.appendChild(doc.createTextNode(str(self.maximum_speed)))
            result.appendChild(elem)

        if self.strict_enforcement is not None:
            elem = doc.createElement('imaer:strictEnforcement')
            elem.appendChild(doc.createTextNode(str(self.strict_enforcement)))
            result.appendChild(elem)

        return result
