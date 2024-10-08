from PyQt5.QtXml import QDomDocument

from .gml import get_gml_element
from .identifier import Nen3610Id


class EmissionSourceType(object):

    def __init__(self, *, local_id, sector_id, geom, epsg_id, label=None, description=None, identifier=None):
        self.label = label
        self.description = description
        self.emission_source_characteristics = None
        self.sector_id = sector_id
        self.building = None
        self.emissions = []
        self.geometry = geom
        self.epsg_id = epsg_id
        self.local_id = local_id
        if identifier is None:
            self.identifier = Nen3610Id(local_id=f'ES.{self.local_id}')
        else:
            self.identifier = identifier

    def to_xml_elem(self, doc=QDomDocument()):
        class_name = self.__class__.__name__
        result = doc.createElement(f'imaer:{class_name}')

        result.setAttribute('sectorId', self.sector_id)
        result.setAttribute('gml:id', f'ES.{self.local_id}')

        if class_name in ['RoadEmissionSource', 'SRM2Road', 'ADMSRoad']:  # Check by name instead of class to prevent circular import
            result.setAttribute('roadAreaType', self.road_area_type)
            result.setAttribute('roadType', self.road_type)

        # identifier
        ident_elem = doc.createElement('imaer:identifier')
        nen_elem = self.identifier.to_xml_elem(doc)
        ident_elem.appendChild(nen_elem)
        result.appendChild(ident_elem)

        # label
        if self.label is not None:
            elem = doc.createElement('imaer:label')
            elem.appendChild(doc.createTextNode(str(self.label)))
            result.appendChild(elem)

        # description
        if self.description is not None:
            elem = doc.createElement('imaer:description')
            elem.appendChild(doc.createTextNode(str(self.description)))
            result.appendChild(elem)

        # emission source characteristics
        if self.emission_source_characteristics is not None:
            esc_elem = doc.createElement('imaer:emissionSourceCharacteristics')
            esc_elem.appendChild(self.emission_source_characteristics.to_xml_elem(doc))
            result.appendChild(esc_elem)

        # geometry
        geom_elem = doc.createElement('imaer:geometry')
        es_geom_elem = doc.createElement('imaer:EmissionSourceGeometry')

        gm_tags = {0: 'GM_Point', 1: 'GM_Curve', 2: 'GM_Surface'}
        gm_tag = gm_tags[self.geometry.type()]
        gml_types = {0: 'POINT', 1: 'CURVE', 2: 'SURFACE'}
        gml_type = gml_types[self.geometry.type()]

        gm_elem = doc.createElement(f'imaer:{gm_tag}')
        gml_elem = get_gml_element(self.geometry, f'ES.{self.local_id}.{gml_type}', self.epsg_id)

        gm_elem.appendChild(gml_elem)
        es_geom_elem.appendChild(gm_elem)
        geom_elem.appendChild(es_geom_elem)
        result.appendChild(geom_elem)

        return result


class EmissionSource(EmissionSourceType):

    def __init__(self, *, emissions=None, **kwargs):
        super().__init__(**kwargs)
        self.emissions = emissions or []

    def to_xml_elem(self, doc=QDomDocument()):
        if doc is None:
            doc = QDomDocument()

        result = super().to_xml_elem(doc)

        for em in self.emissions:
            em_elem = doc.createElement('imaer:emission')

            elem = em.to_xml_elem(doc)
            em_elem.appendChild(elem)

            result.appendChild(em_elem)

        return result


class EmissionSourceCharacteristics(object):

    def __init__(self, building_id=None, heat_content=None, emission_height=None, spread=None, time_varying_profile=None):
        self.building_id = building_id
        self.heat_content = heat_content
        self.emission_height = emission_height
        self.spread = spread
        self.time_varying_profile = time_varying_profile

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:EmissionSourceCharacteristics')

        # building
        if self.building_id is not None:
            elem = doc.createElement('imaer:building')
            elem.setAttribute('xlink:href', f'#Building.{self.building_id}')
            result.appendChild(elem)

        # heat content
        if self.heat_content is not None:
            elem = self.heat_content.to_xml_elem(doc)
            result.appendChild(elem)

        # emission height
        if self.emission_height is not None:
            elem = doc.createElement('imaer:emissionHeight')
            elem.appendChild(doc.createTextNode(str(self.emission_height)))
            result.appendChild(elem)

        # spread
        if self.spread is not None:
            elem = doc.createElement('imaer:spread')
            elem.appendChild(doc.createTextNode(str(self.spread)))
            result.appendChild(elem)

        # time varying profile
        if self.time_varying_profile is not None:
            elem = doc.createElement('imaer:timeVaryingProfile')
            tvp = self.time_varying_profile.to_xml_elem(doc)
            elem.appendChild(tvp)
            result.appendChild(elem)

        return result


class ADMSSourceCharacteristics(object):

    def __init__(
        self, building_id=None, height=None, specific_heat_capacity=None,
        source_type=None, diameter=None, elevation_angle=None, horizontal_angle=None,
        width=None, vertical_dimension=None, buoyancy_type=None, density=None,
        temperature=None, efflux_type=None, vertical_velocity=None,
        volumetric_flow_rate=None, hourly_variation=None, monthly_variation=None
    ):
        self.building_id = building_id
        self.height = height
        self.specific_heat_capacity = specific_heat_capacity
        self.source_type = source_type
        self.diameter = diameter
        self.elevation_angle = elevation_angle
        self.horizontal_angle = horizontal_angle
        self.width = width
        self.vertical_dimension = vertical_dimension
        self.buoyancy_type = buoyancy_type
        self.density = density
        self.temperature = temperature
        self.efflux_type = efflux_type
        self.vertical_velocity = vertical_velocity
        self.volumetric_flow_rate = volumetric_flow_rate
        self.hourly_variation = hourly_variation
        self.monthly_variation = monthly_variation

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:ADMSSourceCharacteristics')

        # building
        if self.building_id is not None:
            elem = doc.createElement('imaer:building')
            elem.setAttribute('xlink:href', f'#Building.{self.building_id}')
            result.appendChild(elem)

        # height
        if self.height is not None:
            elem = doc.createElement('imaer:height')
            elem.appendChild(doc.createTextNode(str(self.height)))
            result.appendChild(elem)

        # specific heat capacity
        if self.specific_heat_capacity is not None:
            elem = doc.createElement('imaer:specificHeatCapacity')
            elem.appendChild(doc.createTextNode(str(self.specific_heat_capacity)))
            result.appendChild(elem)

        # source type
        if self.source_type is not None:
            elem = doc.createElement('imaer:sourceType')
            elem.appendChild(doc.createTextNode(str(self.source_type)))
            result.appendChild(elem)

        # diameter
        if self.diameter is not None:
            elem = doc.createElement('imaer:diameter')
            elem.appendChild(doc.createTextNode(str(self.diameter)))
            result.appendChild(elem)

        # elevation angle
        if self.elevation_angle is not None:
            elem = doc.createElement('imaer:elevationAngle')
            elem.appendChild(doc.createTextNode(str(self.elevation_angle)))
            result.appendChild(elem)

        # horizontal angle
        if self.horizontal_angle is not None:
            elem = doc.createElement('imaer:horizontalAngle')
            elem.appendChild(doc.createTextNode(str(self.horizontal_angle)))
            result.appendChild(elem)

        # width
        if self.width is not None:
            elem = doc.createElement('imaer:width')
            elem.appendChild(doc.createTextNode(str(self.width)))
            result.appendChild(elem)

        # vertical dimension
        if self.vertical_dimension is not None:
            elem = doc.createElement('imaer:verticalDimension')
            elem.appendChild(doc.createTextNode(str(self.vertical_dimension)))
            result.appendChild(elem)

        # buoyancy type
        if self.buoyancy_type is not None:
            elem = doc.createElement('imaer:buoyancyType')
            elem.appendChild(doc.createTextNode(str(self.buoyancy_type)))
            result.appendChild(elem)

        # density
        if self.density is not None:
            elem = doc.createElement('imaer:density')
            elem.appendChild(doc.createTextNode(str(self.density)))
            result.appendChild(elem)

        # temperature
        if self.temperature is not None:
            elem = doc.createElement('imaer:temperature')
            elem.appendChild(doc.createTextNode(str(self.temperature)))
            result.appendChild(elem)

        # efflux type
        if self.efflux_type is not None:
            elem = doc.createElement('imaer:effluxType')
            elem.appendChild(doc.createTextNode(str(self.efflux_type)))
            result.appendChild(elem)

        # vertical velocity
        if self.vertical_velocity is not None:
            elem = doc.createElement('imaer:verticalVelocity')
            elem.appendChild(doc.createTextNode(str(self.vertical_velocity)))
            result.appendChild(elem)

        # volumetric flow rate
        if self.volumetric_flow_rate is not None:
            elem = doc.createElement('imaer:volumetricFlowRate')
            elem.appendChild(doc.createTextNode(str(self.volumetric_flow_rate)))
            result.appendChild(elem)

        # hourly variation
        if self.hourly_variation is not None:
            elem = doc.createElement('imaer:hourlyVariation')
            tvp = self.hourly_variation.to_xml_elem(doc)
            elem.appendChild(tvp)
            result.appendChild(elem)

        # monthly variation
        if self.monthly_variation is not None:
            elem = doc.createElement('imaer:monthlyVariation')
            tvp = self.monthly_variation.to_xml_elem(doc)
            elem.appendChild(tvp)
            result.appendChild(elem)

        return result


class HeatContent(object):

    def __init__(self):
        pass

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:heatContent')
        return result


class SpecifiedHeatContent(HeatContent):

    def __init__(self, *, value, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def to_xml_elem(self, doc=QDomDocument()):
        result = super().to_xml_elem(doc)

        shc = doc.createElement('imaer:SpecifiedHeatContent')
        v = doc.createElement('imaer:value')
        v.appendChild(doc.createTextNode(str(self.value)))

        shc.appendChild(v)
        result.appendChild(shc)

        return result


class Emission(object):

    def __init__(self, substance, value):
        self.substance = substance
        self.value = value

    def to_xml_elem(self, doc=QDomDocument()):
        result = doc.createElement('imaer:Emission')
        result.setAttribute('substance', self.substance)

        v_elem = doc.createElement('imaer:value')
        v_elem.appendChild(doc.createTextNode(str(self.value)))

        result.appendChild(v_elem)

        return result
