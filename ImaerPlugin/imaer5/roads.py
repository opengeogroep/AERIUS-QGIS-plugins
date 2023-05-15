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
