# -*- coding: utf-8 -*-

"""
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
from qgis.core import (
    QgsField,
    QgsFields,
    QgsFeature
)
from qgis import processing, utils

from ImaerPlugin.gpkg import ImaerGpkgFieldFactory


class RelateAlgorithm(QgsProcessingAlgorithm):
    # Abstract base class for all relate algorithms

    geometry_cache = {}
    field_factory = ImaerGpkgFieldFactory()
    output_field_names_dict = {}

    def get_layer_type(self, layer):
        plugin = utils.plugins['ImaerPlugin']
        md = plugin.get_imaer_calc_metadata(layer)
        if md['is_imaer_calc_layer']:
            return md['imaer_layer_type']
        elif md['imaer_contribution_layer'] is not None:
            return md['imaer_contribution_layer']
        else:
            return None

    def find_layer_type(self, layers, feedback=None):
        result = []
        for layer in layers:
            result.append(self.get_layer_type(layer))
        return list(set(result))

    def _create_result_feature(self, layer_type, key, value_dict, max_decimals=None):
        feat = QgsFeature()
        geometry = self.geometry_cache[key]
        feat.setGeometry(geometry)

        if layer_type not in self.output_field_names_dict:
            self.output_field_names_dict[layer_type] = self.field_factory.create_fields_for_layer_type(layer_type).names()

        output_field_names = self.output_field_names_dict[layer_type]

        attributes = []
        if layer_type == 'sub_points':
            parts = key.split('_')
            for part in parts:
                attributes.append(int(part))
        else:
            attributes.append(key)

        num_id_fields = len(attributes)

        for output_field_name in output_field_names[num_id_fields:]:
            attributes.append(value_dict.get(output_field_name, None))

        feat.setAttributes(attributes)
        return feat

    def _create_value_dictionary(self, layer, feedback=None):
        '''
        Returns a dictionary with unique keys and a dictionary with
        result field names and values. Like this:
        {288: {'deposition_nh3': 0.0, 'deposition_nox': 0.02}, 816: {'deposition_nh3': None, 'deposition_nox': 0.3}, ... }

        Also adds the feature geometry to the geometry_cache dictionary.

        Returns None if not all deposition fields and an "fid" field exist,
        which will abort the calculation.
        '''

        layer_type = self.get_layer_type(layer)
        if layer_type is None:
            return None
        if feedback is not None:
            feedback.pushInfo(repr(layer_type))

        value_fields = self.field_factory.create_fields_for_layer_type(layer_type, value_fields_only=True)
        value_field_names = value_fields.names()

        if feedback is not None:
            feedback.pushInfo(repr(value_field_names))

        result = {}
        for feat in layer.getFeatures():
            if layer_type in ['receptor_points', 'receptor_hexagons']:
                key = feat['receptor_id']
            elif layer_type == 'sub_points':
                key = f'{feat["receptor_id"]}_{feat["sub_point_id"]}_{feat["level"]}'
            elif layer_type == 'calculation_points':
                key = feat['calculation_point_id']
            else:
                raise Exception('Invalid IMAER layer type')

            value_dict = {}
            for value_field_name in value_field_names:
                v = feat[value_field_name]
                if isinstance(v, QVariant) and str(v) == 'NULL':
                    v = None
                value_dict[value_field_name] = v
            result[key] = value_dict
            if key not in self.geometry_cache:
                self.geometry_cache[key] = feat.geometry()
        return result

    def _get_receptor_value(self, receptor_dict, key, field_name, no_data=None):
        '''Returns the value for the field_name if present, or otherwise the no_data value.'''
        if receptor_id not in receptor_dict:
            return no_data
        if field_name not in receptor_dict[receptor_id]:
            return no_data
        v = receptor_dict[receptor_id][field_name]
        if v is None:
            return no_data
        return v
