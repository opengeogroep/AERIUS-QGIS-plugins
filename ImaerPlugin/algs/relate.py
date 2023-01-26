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
from qgis import processing


class RelateAlgorithm(QgsProcessingAlgorithm):
    # Abstract base class for all relate algorithms
    dep_field_names = ['dep_NH3', 'dep_NOX']
    dep_total_field_name = 'dep_TOTAL'
    geometry_cache = {}

    def _is_dep_layer(self, layer):
        '''Checks if layer contains all mandatory fields'''
        mandatory_fields = ['fid'] + self.dep_field_names
        layer_field_names = [fld.name() for fld in layer.fields()]

        for mandatory_field in mandatory_fields:
            if mandatory_field not in layer_field_names:
                return False
        return True

    def _get_output_fields(self, with_totals=True):
        fields = QgsFields()
        fields.append(QgsField('fid', QVariant.LongLong, 'int8'))
        for dep_field_name in self.dep_field_names:
            fields.append(QgsField(dep_field_name, QVariant.Double))
        if with_totals:
            fields.append(QgsField(self.dep_total_field_name, QVariant.Double))
        return fields

    def _create_result_feature(self, receptor_id, dep_dict, max_decimals=None, with_totals=True):
        feat = QgsFeature()
        geometry = self.geometry_cache[receptor_id]
        feat.setGeometry(geometry)

        attributes = [receptor_id]
        dep_total = 0
        for field_name in self.dep_field_names:
            if field_name in dep_dict:
                v = dep_dict[field_name]
                if v is not None:
                    dep_total += v
                    if max_decimals is not None:
                        v = round(v, max_decimals)
            else:
                v = None
            attributes.append(v)

        if with_totals:
            if max_decimals is not None:
                dep_total = round(dep_total, max_decimals)
            attributes.append(dep_total)

        feat.setAttributes(attributes)
        return feat

    def _create_receptor_dictionary(self, layer):
        '''
        Returns a dictionary with receptor_id as key and a dictionary with
        deposition_fields and values. Like this:
        {288: {'dep_NH3': 0.0, 'dep_NOX': 0.02}, 816: {'dep_NH3': None, 'dep_NOX': 0.0}, ... }

        Also adds the feature geometry in the geometry_cache dictionary.

        Returns None if not all deposition fields and an "fid" field exist,
        which will abort the calculation.
        '''
        if not self._is_dep_layer(layer):
            return None
        result = {}
        for feat in layer.getFeatures():
            receptor_id = feat['fid']
            dep_dict = {}
            for dep_field_name in self.dep_field_names:
                v = feat[dep_field_name]
                if isinstance(v, QVariant) and str(v) == 'NULL':
                    v = None
                dep_dict[dep_field_name] = v
            result[receptor_id] = dep_dict
            if receptor_id not in self.geometry_cache:
                self.geometry_cache[receptor_id] = feat.geometry()
        return result

    def _get_receptor_value(self, receptor_dict, receptor_id, field_name, no_data=None):
        '''Returns the value for the field_name if present, or otherwise the no_data value.'''
        if receptor_id not in receptor_dict:
            return no_data
        if field_name not in receptor_dict[receptor_id]:
            return no_data
        v = receptor_dict[receptor_id][field_name]
        if v is not None:
            return v
        return no_data
