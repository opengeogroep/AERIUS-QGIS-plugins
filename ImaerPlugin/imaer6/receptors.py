from qgis.core import QgsFeature

from .geometry import GmlPoint, GmlPolygon
from .identifier import Nen3610Id
from .gml import get_gml_element

class CalculationResult(object):

    def __init__(self, result_type=None, substance=None, value=None):
        self.result_type = result_type
        self.substance = substance
        self.value = value

    def __str__(self):
        return f'CalculationResult[{self.result_type}, {self.substance}, {self.value}]'

    def is_valid(self):
        return self.result_type is not None \
            and self.substance is not None \
            and self.value is not None

    def to_xml_elem(self, doc):
        result = doc.createElement('imaer:CalculationResult')
        result.setAttribute('resultType', self.result_type)
        result.setAttribute('substance', self.substance)

        value_elem = doc.createElement('imaer:value')
        value_elem.appendChild(doc.createTextNode(str(self.value)))
        result.appendChild(value_elem)

        return result

    def from_xml_reader(self, xml_reader):
        if not xml_reader.name() == 'CalculationResult':
            return None
        attributes = xml_reader.attributes()
        if attributes.hasAttribute('resultType'):
            self.result_type = attributes.value('resultType')
        if attributes.hasAttribute('substance'):
            self.substance = attributes.value('substance')
        xml_reader.readNextStartElement()
        if xml_reader.name() == 'value':
            xml_reader.readNext()
            text = xml_reader.text()
            self.value = float(text)


class Receptor():

    def __init__(self, local_id=None, identifier=None, geom=None, epsg_id=None, results=None):
        self.local_id = local_id
        self.identifier = identifier
        self.gm_point = geom
        self.epsg_id = epsg_id
        self.representation = None
        self.edge_effect = None
        self.level = None
        self.results = results or []

        # SubPoint attributes
        self.sub_point_id = None
        self.level = None

        # CalculationPoint attributes
        self.label = None
        self.height = None
        self.assessment_category = None
        self.road_local_fraction_no2 = None

        class_name = self.__class__.__name__
        if class_name == 'ReceptorPoint':
            self.domain = 'RP'
        elif class_name == 'SubPoint':
            self.domain = 'SP'
        elif class_name in ['CalculationPoint', 'NcaCustomCalculationPoint']:
            self.domain = 'CP'
        else:
            self.domain = 'XX'

        if identifier is None:
            self.identifier = Nen3610Id(local_id=f'{self.domain}.{self.local_id}')
        else:
            self.identifier = identifier

    def is_valid(self):
        return self.local_id is not None

    def __str__(self):
        return f'Receptor[{self.local_id}, {len(self.results)}]'

    def to_xml_elem(self, doc):
        class_name = self.__class__.__name__
        result = doc.createElement(f'imaer:{class_name}')
        result.setAttribute('gml:id', f'{self.domain}.{self.local_id}')

        if self.identifier is not None:
            ident_elem = doc.createElement('imaer:identifier')
            nen_elem = self.identifier.to_xml_elem(doc)
            ident_elem.appendChild(nen_elem)
            result.appendChild(ident_elem)

        if self.gm_point is not None:
            gmp_elem = doc.createElement('imaer:GM_Point')
            # pnt_elem = self.gm_point.to_xml_elem(doc)
            gml_type = 'POINT'
            pnt_elem = get_gml_element(self.gm_point, f'{self.domain}.{self.local_id}.{gml_type}', self.epsg_id)
            gmp_elem.appendChild(pnt_elem)
            result.appendChild(gmp_elem)

        if self.representation is not None:
            repr_elem = doc.createElement('imaer:representation')
            poly_elem = self.representation.to_xml_elem(doc)
            repr_elem.appendChild(poly_elem)
            result.appendChild(repr_elem)

        for result in self.results:
            result_elem = doc.createElement('result')
            result_elem.appendChild(result.to_xml_elem(doc))
            result.appendChild(result_elem)

        return result

    def from_xml_reader(self, xml_reader):
        start_tag_name = xml_reader.name()

        if start_tag_name not in ['ReceptorPoint', 'SubPoint', 'CalculationPoint', 'NcaCustomCalculationPoint']:
            return

        attributes = xml_reader.attributes()
        if attributes.hasAttribute('receptorPointId'):
            self.local_id = attributes.value('receptorPointId')
        if attributes.hasAttribute('subPointId'):
            self.sub_point_id = attributes.value('subPointId')
        while not (xml_reader.name() == start_tag_name and xml_reader.isEndElement()):
            xml_reader.readNextStartElement()

            if xml_reader.name() == 'identifier':
                xml_reader.readNextStartElement()
                if xml_reader.name() == 'NEN3610ID':
                    identifier = Nen3610Id()
                    identifier.from_xml_reader(xml_reader)
                    # print(identifier)
                    if identifier.is_valid():
                        self.identifier = identifier

            if xml_reader.name() == 'GM_Point':
                xml_reader.readNextStartElement()
                if xml_reader.name() == 'Point':
                    geom = GmlPoint()
                    geom.from_xml_reader(xml_reader)
                    # print(geom)
                    if geom.is_valid():
                        self.gm_point = geom

            if xml_reader.name() == 'representation':
                xml_reader.readNextStartElement()
                if xml_reader.name() == 'Polygon':
                    geom = GmlPolygon()
                    geom.from_xml_reader(xml_reader)
                    # print(geom)
                    if geom.is_valid():
                        self.representation = geom

            if xml_reader.name() == 'CalculationResult':
                result = CalculationResult()
                result.from_xml_reader(xml_reader)
                if result.is_valid():
                    self.results.append(result)

            if xml_reader.name() == 'edgeEffect' and xml_reader.isStartElement():
                xml_reader.readNext()
                text = xml_reader.text().strip()
                if text == 'true':
                    self.edge_effect = 1
                else:
                    self.edge_effect = 0

            if xml_reader.name() == 'level' and xml_reader.isStartElement():
                xml_reader.readNext()
                text = xml_reader.text().strip()
                self.level = int(text)

            if xml_reader.name() == 'label' and xml_reader.isStartElement():
                xml_reader.readNext()
                self.label = xml_reader.text()

            if xml_reader.name() == 'height' and xml_reader.isStartElement():
                xml_reader.readNext()
                text = xml_reader.text().strip()
                self.height = float(text)

            if xml_reader.name() == 'assessmentCategory' and xml_reader.isStartElement():
                xml_reader.readNext()
                self.assessment_category = xml_reader.text()

            if xml_reader.name() == 'roadLocalFractionNO2' and xml_reader.isStartElement():
                xml_reader.readNext()
                text = xml_reader.text().strip()
                self.road_local_fraction_no2 = float(text)

    def get_results_dict(self):
        results_dict = {}
        for result in self.results:
            if result.is_valid():
                key = '{}_{}'.format(result.result_type.lower(), result.substance.lower())
                results_dict[key] = result.value
        return results_dict

    def get_attributes_dict(self):
        result = {}
        result['receptor_id'] = self.local_id
        result['edge_effect'] = self.edge_effect
        result['sub_point_id'] = self.sub_point_id
        result['level'] = self.level
        result['label'] = self.label
        result['height'] = self.height
        result['assessment_category'] = self.assessment_category
        result['deposition_nh3'] = None
        result['deposition_nox'] = None
        result['deposition_nox_nh3_sum'] = None
        result['concentration_nh3'] = None
        result['concentration_nox'] = None
        result['concentration_no2'] = None
        result['concentration_pm25'] = None
        result['concentration_pm10'] = None
        result['exceedance_days_pm25'] = None
        result['exceedance_days_pm10'] = None
        result['exceedance_hours_pm25'] = None
        result['exceedance_hours_pm10'] = None

        result.update(self.get_results_dict())

        # Add sum for depositions
        if result['deposition_nh3'] is None and result['deposition_nox'] is None:
            result['deposition_nox_nh3_sum']
        else:
            result['deposition_nox_nh3_sum'] = (result['deposition_nh3'] or 0) + (result['deposition_nox'] or 0)

        return result


class ReceptorPoint(Receptor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def is_valid(self):
        return self.local_id is not None

    def __str__(self):
        return f'ReceptorPoint[{self.local_id}, {len(self.results)}]'

    def to_point_feature(self, fid=None):
        if not self.is_valid():
            return

        feat = QgsFeature()
        feat.setGeometry(self.gm_point.to_qgis_geometry())

        attributes = []
        attributes.append(fid)

        attr_dict = self.get_attributes_dict()
        attributes.append(attr_dict['receptor_id'])

        first_result_attribute = len(attributes)
        attributes.append(attr_dict['concentration_nox'])
        attributes.append(attr_dict['concentration_no2'])
        attributes.append(attr_dict['concentration_nh3'])
        attributes.append(attr_dict['concentration_pm10'])
        attributes.append(attr_dict['concentration_pm25'])
        attributes.append(attr_dict['exceedance_days_pm10'])
        attributes.append(attr_dict['exceedance_days_pm25'])
        attributes.append(attr_dict['exceedance_hours_pm10'])
        attributes.append(attr_dict['exceedance_hours_pm25'])

        # Return None if feature does not have any result values
        if all(v is None for v in attributes[first_result_attribute:]):
            return None

        feat.setAttributes(attributes)
        return feat

    def to_polygon_feature(self, fid=None):
        if not self.is_valid():
            return

        feat = QgsFeature()
        feat.setGeometry(self.representation.to_qgis_geometry())

        attributes = []
        attributes.append(fid)

        attr_dict = self.get_attributes_dict()
        attributes.append(attr_dict['receptor_id'])
        attributes.append(attr_dict['edge_effect'])

        first_result_attribute = len(attributes)
        attributes.append(attr_dict['deposition_nox_nh3_sum'])
        attributes.append(attr_dict['deposition_nox'])
        attributes.append(attr_dict['deposition_nh3'])

        # Return None if feature does not have any result values
        if all(v is None for v in attributes[first_result_attribute:]):
            return None

        feat.setAttributes(attributes)
        return feat

    def to_xml_elem(self, doc):
        result = super().to_xml_elem(doc)

        if self.edge_effect is not None:
            elem = doc.createElement('imaer:edgeEffect')
            if self.edge_effect == 1:
                text = 'true'
            else:
                text = 'false'
            elem.appendChild(doc.createTextNode(text))
            result.appendChild(elem)

        return result


class SubPoint(Receptor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def is_valid(self):
        return self.local_id is not None and self.sub_point_id is not None

    def __str__(self):
        return f'SubPoint[{self.local_id}, {self.sub_point_id}, {self.level}, {len(self.results)}]'

    def to_point_feature(self, fid=None):
        if not self.is_valid():
            return

        feat = QgsFeature()
        feat.setGeometry(self.gm_point.to_qgis_geometry())

        attributes = []
        attributes.append(fid)
        attributes.append(self.local_id)
        attributes.append(self.sub_point_id)
        attributes.append(self.level)

        attr_dict = self.get_attributes_dict()

        first_result_attribute = len(attributes)
        attributes.append(attr_dict['deposition_nox_nh3_sum'])
        attributes.append(attr_dict['deposition_nox'])
        attributes.append(attr_dict['deposition_nh3'])
        attributes.append(attr_dict['concentration_nox'])
        attributes.append(attr_dict['concentration_no2'])
        attributes.append(attr_dict['concentration_nh3'])
        attributes.append(attr_dict['concentration_pm10'])
        attributes.append(attr_dict['concentration_pm25'])
        attributes.append(attr_dict['exceedance_days_pm10'])
        attributes.append(attr_dict['exceedance_days_pm25'])
        attributes.append(attr_dict['exceedance_hours_pm10'])
        attributes.append(attr_dict['exceedance_hours_pm25'])

        # Return None if feature does not have any result values
        if all(v is None for v in attributes[first_result_attribute:]):
            return None

        feat.setAttributes(attributes)
        return feat

    def to_xml_elem(self, doc):
        result = super().to_xml_elem(doc)

        if self.level is not None:
            lvl_elem = doc.createElement('imaer:level')
            lvl_elem.appendChild(doc.createTextNode(str(self.level)))
            result.appendChild(lvl_elem)

        return result


class CalculationPoint(Receptor):

    def __init__(self, label=None, height=None, assessment_category=None, description=None, road_local_fraction_no2=None, entity_reference=None, **kwargs):
        super().__init__(**kwargs)

        self.label = label
        self.height = height
        self.assessment_category = assessment_category
        self.description = description
        self.road_local_fraction_no2 = road_local_fraction_no2
        self.entity_reference = entity_reference

    def __str__(self):
        class_name = self.__class__.__name__
        return f'{class_name}[{self.identifier}, {self.label}, {self.height}, {self.assessment_category}, {self.road_local_fraction_no2}, {len(self.results)}]'

    def is_valid(self):
        return True  # self.local_id is not None

    def to_xml_elem(self, doc):
        result = super().to_xml_elem(doc)

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

        # height
        if self.height is not None:
            elem = doc.createElement('imaer:height')
            elem.appendChild(doc.createTextNode(str(self.height)))
            result.appendChild(elem)

        # assessment_category
        if self.assessment_category is not None:
            elem = doc.createElement('imaer:assessmentCategory')
            elem.appendChild(doc.createTextNode(str(self.assessment_category)))
            result.appendChild(elem)

        # road_local_fraction_no2
        if self.road_local_fraction_no2 is not None:
            elem = doc.createElement('imaer:roadLocalFractionNO2')
            elem.appendChild(doc.createTextNode(str(self.road_local_fraction_no2)))
            result.appendChild(elem)

        # entity_reference
        if self.entity_reference is not None:
            elem = doc.createElement('imaer:entityReference')
            elem.appendChild(self.entity_reference.to_xml_elem(doc))
            result.appendChild(elem)

        return result

    def to_point_feature(self, fid=None):
        if not self.is_valid():
            print('invalid')
            return

        feat = QgsFeature()
        feat.setGeometry(self.gm_point.to_qgis_geometry())

        if self.identifier is not None:
            local_id = self.identifier.local_id
        else:
            local_id = None

        attributes = []
        attributes.append(fid)
        attributes.append(local_id)
        attributes.append(self.label)
        attributes.append(self.height)
        attributes.append(self.assessment_category)
        attributes.append(self.road_local_fraction_no2)

        attr_dict = self.get_attributes_dict()

        first_result_attribute = len(attributes)
        attributes.append(attr_dict['deposition_nox_nh3_sum'])
        attributes.append(attr_dict['deposition_nox'])
        attributes.append(attr_dict['deposition_nh3'])
        attributes.append(attr_dict['concentration_nox'])
        attributes.append(attr_dict['concentration_no2'])
        attributes.append(attr_dict['concentration_nh3'])
        attributes.append(attr_dict['concentration_pm10'])
        attributes.append(attr_dict['concentration_pm25'])
        attributes.append(attr_dict['exceedance_days_pm10'])
        attributes.append(attr_dict['exceedance_days_pm25'])
        attributes.append(attr_dict['exceedance_hours_pm10'])
        attributes.append(attr_dict['exceedance_hours_pm25'])

        # Return None if feature does not have any result values
        if all(v is None for v in attributes[first_result_attribute:]):
            return None

        feat.setAttributes(attributes)
        return feat

class NcaCustomCalculationPoint(CalculationPoint):
    pass
