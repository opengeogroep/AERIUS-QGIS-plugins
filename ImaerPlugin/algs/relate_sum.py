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
    ADD_TOTALS = 'ADD_TOTALS'
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
            QgsProcessingParameterBoolean(
                self.ADD_TOTALS,
                self.tr('Add field with total depositions'),
                defaultValue=True
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

        dep_dict_layers = []
        for layer in layers:
            layer_name = layer.name()
            if not self._is_dep_layer(layer):
                raise QgsProcessingException(f'"{layer_name}" is not a valid deposition layer.')
            dep_dict_layer = self._create_receptor_dictionary(layer)
            if dep_dict_layer is None:
                raise QgsProcessingException(f'"{layer_name}" is not a valid deposition layer.')
            dep_dict_layers.append(dep_dict_layer)

            feedback.setProgress(int(current * step))
            current += 1

        add_totals = self.parameterAsBoolean(parameters, self.ADD_TOTALS, context)
        output_fields = self._get_output_fields(with_totals=add_totals)

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

        calc_result_dict = self._calc_dict_sum(dep_dict_layers)

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

    def _calc_dict_sum(self, in_dep_dicts):
        result = {}
        for receptor_id in self.geometry_cache:
            out_dep_dict = {}
            for in_dep_dict in in_dep_dicts:
                for dep_field_name in self.dep_field_names:
                    v = self._get_receptor_value(in_dep_dict, receptor_id, dep_field_name, no_data=0)
                    if dep_field_name in out_dep_dict:
                        out_dep_dict[dep_field_name] += v
                    else:
                        out_dep_dict[dep_field_name] = v
            result[receptor_id] = out_dep_dict
        return result
