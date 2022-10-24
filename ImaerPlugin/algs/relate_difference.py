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

from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
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
    OUTPUT = 'OUTPUT'

    def tr(self, string):
        return QCoreApplication.translate('Difference', string)

    def createInstance(self):
        return RelateDifferenceAlgorithm()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'relate_difference'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Difference')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Relate depositions')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'relate'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Calculate difference between deposition layers")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector features source. It can have any kind of
        # geometry.
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT1,
                self.tr('Input layer 1'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT2,
                self.tr('Input layer 2'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        # We add a feature sink in which to store our processed features (this
        # usually takes the form of a newly created vector layer when the
        # algorithm is run in QGIS).
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output layer')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        layer_1 = self.parameterAsSource(parameters, self.INPUT1, context)
        if layer_1 is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        if not self._is_dep_layer(layer_1):
            feedback.pushInfo('Layer 1 is not a dep layer')
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        layer_2 = self.parameterAsSource(parameters, self.INPUT2, context)
        if layer_2 is None:
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))
        if not self._is_dep_layer(layer_2):
            feedback.pushInfo('Layer 1 is not a dep layer')
            raise QgsProcessingException(self.invalidSourceError(parameters, self.INPUT))

        output_fields = self._get_output_fields()
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

        self.geometry_cache = {}

        dep_dict_layer_1 = self._create_receptor_dictionary(layer_1)
        if dep_dict_layer_1 is None:
            layer_name = layer_1.name()
            feedback.pushError(f'"{layer_name}" is not a valid deposition layer.')

        dep_dict_layer_2 = self._create_receptor_dictionary(layer_2)
        if dep_dict_layer_2 is None:
            layer_name = layer_2.name()
            feedback.pushError(f'"{layer_name}" is not a valid deposition layer.')

        #qml_file_name = os.path.join(self.plugin.plugin_dir, 'styles', 'calc_result_diff.qml')
        calc_result_dict = self._calc_dict_difference(dep_dict_layer_1, dep_dict_layer_2)

        if len(calc_result_dict) == 0:
            feedback.pushInfo(f'No result features to load.')
            return #  TODO Find good way to terminate process.

        total = 100.0 / len(calc_result_dict)
        current = 1

        for receptor_id in calc_result_dict:
            # Stop the algorithm if cancel button has been clicked
            if feedback.isCanceled():
                break

            feat = self._create_result_feature(receptor_id, calc_result_dict[receptor_id], 6)
            sink.addFeature(feat, QgsFeatureSink.FastInsert)

            # Update the progress bar
            feedback.setProgress(int(current * total))
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
