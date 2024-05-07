from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsFields, QgsField

field_config = {
    'deposition': {
        'deposition_nox_nh3_sum': QVariant.Double,
        'deposition_nox': QVariant.Double,
        'deposition_nh3': QVariant.Double
    },
    'concentration': {
        'concentration_nox': QVariant.Double,
        'concentration_no2': QVariant.Double,
        'concentration_nh3': QVariant.Double,
        'concentration_pm10': QVariant.Double,
        'concentration_pm25': QVariant.Double
    },
    'exceedance': {
        'exceedance_days_pm10': QVariant.LongLong,
        'exceedance_days_pm25': QVariant.LongLong,
        'exceedance_hours_pm10': QVariant.LongLong,
        'exceedance_hours_pm25': QVariant.LongLong
    },
    'receptor_points': {
        'receptor_id': QVariant.LongLong
    },
    'receptor_hexagons': {
        'receptor_id': QVariant.LongLong,
        'edge_effect': QVariant.LongLong
    },
    'sub_points': {
        'receptor_id': QVariant.LongLong,
        'sub_point_id': QVariant.LongLong,
        'level': QVariant.LongLong
    },
    'calculation_points': {
        'calculation_point_id': QVariant.String,
        'label': QVariant.String,
        'height': QVariant.Double,
        'assessment_category': QVariant.String
    }
}

layer_type_config = {
    'receptor_points': [
        'receptor_points',
        'concentration',
        'exceedance'
    ],
    'receptor_hexagons': [
        'receptor_hexagons',
        'deposition'
    ],
    'sub_points': [
        'sub_points',
        'deposition',
        'concentration',
        'exceedance'
    ],
    'calculation_points': [
        'calculation_points',
        'deposition',
        'concentration',
        'exceedance'
    ]
}

class ImaerGpkgFieldFactory(object):

    def _create_fields(self, categories):
        result = QgsFields()
        for category in categories:
            for field_name, field_type in field_config[category].items():
                result.append(QgsField(field_name, field_type))
        return result

    def create_fields_for_layer_type(self, layer_type, value_fields_only=False):
        categories = layer_type_config[layer_type].copy()
        #print('value_fields_only', value_fields_only)
        if value_fields_only:
            categories.pop(0)
        result = self._create_fields(categories)
        return result
