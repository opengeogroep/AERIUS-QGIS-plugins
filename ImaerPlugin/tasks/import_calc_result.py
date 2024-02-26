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

        member_info = doc.get_member_count()
        self.log(member_info)

        result_member_count = 0
        for k, v in member_info.items():
            if k in ['ReceptorPoint', 'SubPoint']:
                result_member_count += v
        self.log(result_member_count)

        if result_member_count == 0:
            self.log('No results found')
            # TODO User feedback
            return False

        gpkg = ImaerGpkg(self.gpkg_fn, plugin=self.plugin)
        self.log(str(gpkg))

        # metadata
        gpkg.set_metadata('gml_fn', doc.gml_fn)
        gpkg.set_metadata('imaer_version', doc.get_version().to_string())

        self.log(gpkg.get_all_metadata())

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
                receptor_points_layer.addFeature(feat)
                
                feat = member.to_polygon_feature()
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
        if receptor_hexagons_layer is not None:
            receptor_hexagons_layer.commitChanges()
        if sub_points_layer is not None:
            sub_points_layer.commitChanges()
        
        self.load_layer_callback(self.gpkg_fn)

        self.setProgress(100)

        return True

    def finished(self, result):
        pass

    def cancel(self):
        self.log(
            'Task "{name}" was canceled'.format(name=self.description()))
        # TODO delete gpkg file
        super().cancel()

    def log(self, message, tab='IMAER'):
        if self.do_log:
            QgsMessageLog.logMessage(repr(message), tab, level=Qgis.Info)

