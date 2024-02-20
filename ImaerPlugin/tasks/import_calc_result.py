import os

from qgis.PyQt.QtCore import QVariant, QFile
from qgis.core import (
    Qgis,
    QgsTask,
    QgsMessageLog,
    QgsProviderRegistry,
    QgsCoordinateReferenceSystem,
    QgsFields,
    QgsField,
    QgsWkbTypes,
    QgsFeature,
    QgsGeometry,
    QgsVectorLayer,
    QgsExpressionContextUtils,
    QgsSettings
)

from .. task_timer import TaskTimer
from ImaerPlugin.imaer5 import ImaerDocument
from ImaerPlugin.gpkg import ImaerGpkg

_SUPPORTED_IMAER_VERSIONS = ['2.2', '3.1', '4.0', '5.0', '5.1']
_EDGE_EFFECT_VALUES = {'false': 0, 'true': 1}


class ImportImaerCalculatorResultTask(QgsTask):

    def __init__(self, plugin, gml_fn, gpkg_fn, load_layer_callback):
        super().__init__('Import IMAER Calculator Result', QgsTask.CanCancel)
        self.gml_fn = gml_fn
        self.gpkg_fn = gpkg_fn
        self.load_layer_callback = load_layer_callback
        self.exception = None
        self.settings = QgsSettings()
        self.plugin = plugin
        self.do_log = True

    def run(self):
        self.log('Started task "{}"'.format(self.description()))
        self.log(self.gml_fn)
        self.log(self.gpkg_fn)

        self.setProgress(1)  # Cause setting to 0% does not work.
        
        doc = ImaerDocument()
        doc.from_xml_file(self.gml_fn)
        self.log(str(doc))

        self.setProgress(40)

        if os.path.isfile(self.gpkg_fn):
            os.remove(self.gpkg_fn)

        gpkg = ImaerGpkg(self.gpkg_fn)
        self.log(str(gpkg))

        receptor_points_layer = None
        receptor_hexagons_layer = None
        sub_points_layer = None

        member_cnt = 0

        for member in doc.feature_members:
            if member.__class__.__name__ == 'ReceptorPoint':
                if receptor_points_layer is None:
                    epsg_id = int(member.gm_point.epsg_id)
                    gpkg.create_layer_receptor_points(epsg_id)
                    receptor_points_layer = QgsVectorLayer(f'{self.gpkg_fn}|layername=receptor_points', 'receptor_points', 'ogr')
                    receptor_points_layer.startEditing()
                if receptor_hexagons_layer is None:
                    epsg_id = int(member.representation.epsg_id)
                    gpkg.create_layer_receptor_hexagons(epsg_id)
                    receptor_hexagons_layer = QgsVectorLayer(f'{self.gpkg_fn}|layername=receptor_hexagons', 'receptor_hexagons', 'ogr')
                    receptor_hexagons_layer.startEditing()
                
                feat = member.to_point_feature()
                self.log(feat.geometry())
                receptor_points_layer.addFeature(feat)
                
                feat = member.to_polygon_feature()
                self.log(feat.geometry())
                receptor_hexagons_layer.addFeature(feat)
                
                member_cnt += 1
            elif member.__class__.__name__ == 'SubPoint':
                if sub_points_layer is None:
                    epsg_id = int(member.gm_point.epsg_id)
                    gpkg.create_layer_sub_points(epsg_id)
                    sub_points_layer = QgsVectorLayer(f'{self.gpkg_fn}|layername=sub_points', 'sub_points', 'ogr')
                    sub_points_layer.startEditing()
                feat = member.to_point_feature()
                sub_points_layer.addFeature(feat)
                member_cnt += 1

        self.setProgress(80)


        if receptor_points_layer is not None:
            receptor_points_layer.commitChanges()
            self.load_layer_callback(receptor_points_layer)
        if receptor_hexagons_layer is not None:
            receptor_hexagons_layer.commitChanges()
            self.load_layer_callback(receptor_hexagons_layer)
        if sub_points_layer is not None:
            sub_points_layer.commitChanges()
            self.load_layer_callback(sub_points_layer)

        self.setProgress(100)

        return True


    def finished(self, result):
        pass

    def cancel(self):
        self.log(
            'Task "{name}" was canceled'.format(name=self.description()))
        # TODO delete gpkg file
        super().cancel()

    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(repr(message), tab, level=Qgis.Info)

