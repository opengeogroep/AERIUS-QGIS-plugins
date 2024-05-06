# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterBoolean,
                       QgsProcessingParameterMultipleLayers,
                       QgsProcessingParameterFeatureSink)
from qgis import processing

from .relate import RelateAlgorithm


class RelateSumAlgorithm(RelateAlgorithm):
    INPUT_LAYERS = 'INPUT_LAYERS'
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Sum', string)

    def createInstance(self):
        return RelateSumAlgorithm()

    def name(self):
        return 'relate_sum'

    def displayName(self):
        return self.tr('Sum')

    def group(self):
        return self.tr('Relate depositions')

    def groupId(self):
        return 'relate'

    def shortHelpString(self):
        return self.tr("Summarize values of deposition layers")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterMultipleLayers(
                self.INPUT_LAYERS,
                self.tr('Input deposition layers'),
                QgsProcessing.TypeVectorPolygon,
                optional=False
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Deposition sum')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        feedback.setProgress(0)

        layers = self.parameterAsLayerList(parameters, self.INPUT_LAYERS, context)
        step = 50 / len(layers)
        current = 1

        self.geometry_cache = {}
        result_value_dicts = []

        layer_types = self.find_layer_type(layers)
        feedback.pushInfo(repr(layer_types))

        if len(layer_types) == 0:
            raise QgsProcessingException(f'No IMAER layer type found')
        elif len(layer_types) > 1:
            raise QgsProcessingException(f'Multiple IMAER layer types found')
        
        layer_type = layer_types[0]

        for layer in layers:
            layer_name = layer.name()
            feedback.pushInfo(layer_name)
            
            value_dict = self._create_value_dictionary(layer, feedback)
            #feedback.pushInfo(repr(value_dict))

            if value_dict is None:
                raise QgsProcessingException(f'"{layer_name}" is not a valid deposition layer.')
            result_value_dicts.append(value_dict)

            feedback.setProgress(int(current * step))
            current += 1

        output_fields = self.field_factory.create_fields_for_layer_type(layer_type, value_fields_only=False)
        feedback.pushInfo(repr(output_fields))
        for f in output_fields:
            feedback.pushInfo(f.name())

        (sink, dest_id) = self.parameterAsSink(
            parameters,
            self.OUTPUT,
            context,
            output_fields,
            layers[0].wkbType(),
            layers[0].sourceCrs()
        )

        if sink is None:
            raise QgsProcessingException(self.invalidSinkError(parameters, self.OUTPUT))

        calc_result_dict = self._calc_dict_sum(result_value_dicts)

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


    def _calc_dict_sum(self, result_value_dicts):
        result = {}
        for in_dep_dict in result_value_dicts:
            for id in in_dep_dict:
                #print(id)
                for substance, value in in_dep_dict[id].items():
                    #print(substance, value)
                    if not id in result:
                        result[id] = {}
                    if not substance in result[id]:
                        result[id][substance] = value
                    else:
                        old_value = result[id][substance]
                        if old_value is None:
                            result[id][substance] = value
                        else:
                            if value is not None:
                                result[id][substance] += value
        return result
