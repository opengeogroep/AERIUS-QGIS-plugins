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

    INPUT1 = 'INPUT_1'
    INPUT2 = 'INPUT_2'
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
        result_value_dicts = []

        layer_types = self.find_layer_type([layer_1, layer_2])
        feedback.pushInfo(repr(layer_types))

        if len(layer_types) == 0:
            raise QgsProcessingException(f'No IMAER layer type found')
        elif len(layer_types) > 1:
            raise QgsProcessingException(f'Multiple IMAER layer types found')
        
        layer_type = layer_types[0]

        for layer in [layer_1, layer_2]:
            layer_name = layer.name()

            value_dict = self._create_value_dictionary(layer, feedback)

            if value_dict is None:
                raise QgsProcessingException(f'"{layer_name}" is not a valid deposition layer.')
            
            result_value_dicts.append(value_dict)

            feedback.setProgress(int(current * step))
            current += 1

        output_fields = self.field_factory.create_fields_for_layer_type(layer_type, value_fields_only=False)
        feedback.pushInfo(repr(output_fields))

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

        calc_result_dict = self._calc_dict_difference(result_value_dicts[0], result_value_dicts[1])
        feedback.setProgress(50)

        if len(calc_result_dict) == 0:
            raise QgsProcessingException(f'No result features to load.')

        step = 50 / len(calc_result_dict)
        current = 1

        for key in calc_result_dict:
            if feedback.isCanceled():
                break

            feat = self._create_result_feature(layer_type, key, calc_result_dict[key], max_decimals=6)
            sink.addFeature(feat, QgsFeatureSink.FastInsert)

            feedback.setProgress(50 + int(current * step))
            current += 1

        return {self.OUTPUT: dest_id}


    def _calc_dict_difference(self, result_value_dict_1, result_value_dict_2):
        result = {}

        for id in result_value_dict_1:
            for substance, value in result_value_dict_1[id].items():
                if not id in result:
                    result[id] = {}
                if not substance in result[id]:
                    result[id][substance] = value

        for id in result_value_dict_2:
            for substance, value in result_value_dict_2[id].items():
                if not id in result:
                    result[id] = {}
                    if not substance in result[id]:
                        if value is None:
                            result[id][substance] = value
                        else:
                            result[id][substance] = -value
                else:
                    if value is not None:
                        old_value = result[id].get(substance)
                        if old_value is None:
                            result[id][substance] = -value
                        else:
                            result[id][substance] = old_value - value
        return result
