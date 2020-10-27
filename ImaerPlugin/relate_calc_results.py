# -*- coding: utf-8 -*-
import os

from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import (
    QDialog
)
from PyQt5 import uic

from qgis.core import QgsVectorLayer, QgsField, QgsProject, QgsFeature

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'relate_calc_results_dlg.ui'))




class RelateCalcResultsDialog(QDialog, FORM_CLASS):

    def __init__(self, plugin, parent=None):
        super(RelateCalcResultsDialog, self).__init__(parent)

        self.setupUi(self)
        self.plugin = plugin
        self.iface = plugin.iface

        self.init_gui()


    def init_gui(self):
        pass


    def __del__(self):
        pass


    def create_result_layer(self, layer_name, value_fieldname, qml=None):
        crs = self.plugin.iface.mapCanvas().mapSettings().destinationCrs().authid()
        feature_type = 'Polygon?crs={}'.format(crs)
        layer = QgsVectorLayer(feature_type, layer_name, 'memory')

        provider = layer.dataProvider()

        fields = []
        fields.append(QgsField('fid', QVariant.LongLong, 'int8'))
        fields.append(QgsField(value_fieldname, QVariant.Double))
        provider.addAttributes(fields)
        layer.updateFields()

        QgsProject.instance().addMapLayer(layer)

        if qml is not None:
            layer.loadNamedStyle(qml)

        return (layer, provider)


    def create_result_feature(self, fid, value, geometry):
        feat = QgsFeature()
        feat.setGeometry(geometry)
        feat.setAttributes([fid, value])
        return feat


    def calculate_difference(self, layer1, layer2, substance='NH3'):
        receptor_dict = {}
        substance_fieldname = f'dep_{substance}'

        for feat in layer1.getFeatures():
            receptor_id = feat['fid']
            value = feat[substance_fieldname]
            receptor_dict[receptor_id] = {'value1': value, 'geom': feat.geometry()}

        for feat in layer2.getFeatures():
            receptor_id = feat['fid']
            value = feat[substance_fieldname]
            if receptor_id in receptor_dict:
                receptor_dict[receptor_id]['value2'] = value
            else:
                receptor_dict[receptor_id] = {'value2': value, 'geom': feat.geometry()}

        qml = os.path.join(self.plugin.plugin_dir, 'styles', 'calc_result_diff.qml')
        result_layer, result_provider = self.create_result_layer('difference', 'diff_NH3', qml=qml)

        for key in receptor_dict:
            if 'value1' in receptor_dict[key]:
                v1 = receptor_dict[key]['value1']
            else:
                v1 = 0
            if 'value2' in receptor_dict[key]:
                v2 = receptor_dict[key]['value2']
            else:
                v2 = 0

            feat = self.create_result_feature(key, v1-v2, receptor_dict[key]['geom'])
            result_provider.addFeatures([feat])
