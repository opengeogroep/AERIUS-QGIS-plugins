# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterMapLayer,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink)
from qgis import processing

from .relate import RelateAlgorithm


class RelateDifferenceAlgorithm(RelateAlgorithm):
    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT1 = 'INPUT1'
    INPUT2 = 'INPUT2'
    ADD_TOTALS = 'ADD_TOTALS'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Difference', string)

    def createInstance(self):
        return RelateDifferenceAlgorithm()

    def name(self):
        return 'relate_difference'

    def displayName(self):
        return self.tr('Difference')

    def group(self):
        return self.tr('Relate depositions')

    def groupId(self):
        return 'relate'

    def shortHelpString(self):
        return self.tr("Calculate difference between values of deposition layers")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMapLayer(
                self.INPUT1,
                self.tr('Input deposition layer 1'),
                [QgsProcessing.TypeVectorPolygon],
                optional=False
            )
        )
        self.addParameter(
            QgsProcessingParameterMapLayer(
                self.INPUT2,
                self.tr('Input deposition layer 2'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )
        self.addParameter(
            QgsProcessingParameterBoolean(
                self.ADD_TOTALS,
                self.tr('Add field with total depositions'),
                defaultValue=True
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Deposition difference')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        feedback.setProgress(0)

        layer_1 = self.parameterAsLayer(parameters, self.INPUT1, context)
        layer_2 = self.parameterAsLayer(parameters, self.INPUT2, context)

        step = 50 / 3
        current = 1

        self.geometry_cache = {}

        dep_dict_layers = []
        for layer in [layer_1, layer_2]:
            layer_name = layer.name()
            if not self._is_dep_layer(layer):
                raise QgsProcessingException(f'"{layer_name}" is not a valid deposition layer.')
            dep_dict_layer = self._create_receptor_dictionary(layer)
            if dep_dict_layer is None:
                raise QgsProcessingException(f'"{layer_name}" is not a valid deposition layer.')
            dep_dict_layers.append(dep_dict_layer)

            feedback.setProgress(int(current * step))
            current +=1

        add_totals = self.parameterAsBoolean(parameters, self.ADD_TOTALS, context)
        output_fields = self._get_output_fields(with_totals=add_totals)

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            output_fields,
            layer_1.wkbType(),
            layer_1.sourceCrs()
        )

        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        calc_result_dict = self._calc_dict_difference(dep_dict_layers[0], dep_dict_layers[1])
        feedback.setProgress(50)

        if len(calc_result_dict) == 0:
            raise QgsProcessingException(f'No result features to load.')

        step = 50 / len(calc_result_dict)
        current = 1

        for receptor_id in calc_result_dict:
            if feedback.isCanceled():
                break

            feat = self._create_result_feature(receptor_id, calc_result_dict[receptor_id], max_decimals=6, with_totals=add_totals)
            sink.addFeature(feat, QgsFeatureSink.FastInsert)

            feedback.setProgress(50 + int(current * step))
            current += 1

        return {self.OUTPUT: dest_id}

    def _calc_dict_difference(self, dep_dict_layer_1, dep_dict_layer_2):
        result = {}
        for receptor_id in self.geometry_cache:
            dep_dict = {}
            for dep_field_name in self.dep_field_names:
                v1 = self._get_receptor_value(dep_dict_layer_1, receptor_id, dep_field_name, no_data=0)
                v2 = self._get_receptor_value(dep_dict_layer_2, receptor_id, dep_field_name, no_data=0)
                dep_dict[dep_field_name] = v1 - v2
            result[receptor_id] = dep_dict
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
