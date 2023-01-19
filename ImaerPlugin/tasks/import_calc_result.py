import os
import xml.etree.ElementTree as ET

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

_IMAER_DEPOSITION_SUBSTANCES = ['NH3', 'NOX']
_SUPPORTED_IMAER_VERSIONS = ['2.2', '3.1', '4.0', '5.0', '5.1']
_EDGE_EFFECT_VALUES = {'false': 0, 'true': 1}


class GpkgFileExists(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message


class ImportImaerCalculatorResultTask(QgsTask):

    def __init__(self, gml_fn, gpkg_fn, load_layer_callback):
        super().__init__('Import IMAER Calculator Result', QgsTask.CanCancel)
        self.gml_fn = gml_fn
        self.gpkg_fn = gpkg_fn
        self.load_layer_callback = load_layer_callback
        self.exception = None
        self.do_log = True
        # self.log(self.gml_fn)
        self.namespaces = {}
        self.settings = QgsSettings()

    def run(self):
        self.log('Started task "{}"'.format(self.description()))

        elem_cnt = 0
        self.feat_cnt = 0
        self.rp_without_geom_cnt = 0

        errors = False

        with open(self.gml_fn, 'rb') as gml_file:
            gml_file_size = float(os.fstat(gml_file.fileno()).st_size)
            step = max(int(gml_file_size / 160000), 1)
            self.setProgress(0)

            context = ET.iterparse(gml_file, events=('start', 'end', 'start-ns'))

            root = None
            for event, elem in context:

                # self.log('{}, {}'.format(event, elem))

                # set the first element as root
                if root is None and event == 'start':
                    root = elem

                if event == 'start-ns':
                    self.namespaces[elem[0]] = elem[1]
                    if elem[0] == 'imaer':
                        self.imaer_version = self.get_imaer_version(elem[1])
                        if self.imaer_version not in _SUPPORTED_IMAER_VERSIONS:
                            self.exception = Exception(f'IMAER version {self.imaer_version} is not supported')
                            return False
                        feature_member_tag = '{{{0}}}featureMember'.format(elem[1])
                        receptor_point_tag = '{{{0}}}ReceptorPoint'.format(elem[1])
                        calculation_point_tag = '{{{0}}}CalculationPoint'.format(elem[1])
                        epsg_id = self.settings.value('imaer_plugin/crs', defaultValue=None)
                        if epsg_id is None:
                            self.log("No crs has been selected by the user")
                            self.exception = Exception(f'No crs has been selected by the user in the Configure options')
                            return False
                        if isinstance(epsg_id, str):
                            epsg_id = int(epsg_id)
                        self.create_gpkg(epsg_id)
                        receptors_layer = QgsVectorLayer(self.gpkg_fn, 'receptors', 'ogr')
                        receptors_layer.startEditing()

                if event == 'end' and elem.tag == feature_member_tag:
                    child = list(elem)[0]
                    # self.log('  {}'.format(child.tag))
                    if child.tag == receptor_point_tag:
                        feat = self.process_rp(child)
                        if feat is not None:
                            receptors_layer.addFeature(feat)
                            self.feat_cnt += 1
                        else:
                            self.rp_without_geom_cnt += 1
                        elem.clear()
                        elem_cnt += 1
                    if child.tag == calculation_point_tag:  # Also count calculation Points allthough these aren't processed (yet)
                        self.rp_without_geom_cnt += 1
                        elem_cnt += 1

                if (elem_cnt) % step == 0:
                    self.setProgress((gml_file.tell() / gml_file_size) * 100)

                if self.isCanceled():
                    return False

            receptors_layer.commitChanges()
        for key in self.namespaces:
            ET.register_namespace(key, self.namespaces[key])
        xml_string = ET.tostring(root).decode('utf-8')
        xml_string = xml_string.replace('<imaer:featureMember />', '')
        # self.log(xml_string)
        self.save_metadata('xml', xml_string)
        self.save_metadata('gml_fn', self.gml_fn)
        self.save_metadata('user', QgsExpressionContextUtils().globalScope().variable('user_full_name'))
        self.save_metadata('imaer_version', self.imaer_version)

        return True

    def finished(self, result):
        self.log('finished task')
        self.log(result)
        # self.conn.close()
        if result:
            self.log(
                'ImaerResultToGpkgTask "{name}" completed'.format(name=self.description()))
            self.load_layer_callback(self.gpkg_fn, feat_cnt=self.feat_cnt, rp_without_geom_cnt=self.rp_without_geom_cnt)
        else:
            self.log(self.exception)
            if self.exception is None:
                self.log(
                    'Task "{name}" not successful but without '
                    'exception (probably the task was manually '
                    'canceled by the user)'.format(
                        name=self.description()))
            else:
                self.log(
                    'Task "{name}" Exception: {exception}'.format(
                        name=self.description(),
                        exception=self.exception))
                raise self.exception

    def cancel(self):
        self.log(
            'Task "{name}" was canceled'.format(name=self.description()))
        # TODO delete gpkg file
        super().cancel()

    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(repr(message), tab, level=Qgis.Info)

    def get_imaer_version(self, ns_url):
        url_parts = ns_url.split('/')
        version_str = url_parts[-1]
        self.log(version_str)
        return version_str

    def create_gpkg(self, epsg_id):
        self.log(epsg_id)
        gpkg_file = QFile(self.gpkg_fn)
        if gpkg_file.exists():
            self.exception = GpkgFileExists(f'Gpkg file already exists: {self.gpkg_fn}')
            self.cancel()
            return

        md = QgsProviderRegistry.instance().providerMetadata('ogr')
        if Qgis.QGIS_VERSION_INT >= 32800:
            cdb_result = md.createDatabase(self.gpkg_fn)
            self.log(cdb_result)
            if not cdb_result[0]:  # Is false if db could not be created
                self.log(cdb_result[1])
        self.conn = md.createConnection(self.gpkg_fn, {})
        # self.log(self.conn)

        fields = QgsFields()
        fields.append(QgsField('key', QVariant.String))
        fields.append(QgsField('value', QVariant.String))
        self.conn.createVectorTable('', 'imaer_metadata', fields, QgsWkbTypes.NoGeometry, QgsCoordinateReferenceSystem(), True, {})

        fields = QgsFields()
        fields.append(QgsField('point_x', QVariant.Double))
        fields.append(QgsField('point_y', QVariant.Double))
        for substance in _IMAER_DEPOSITION_SUBSTANCES:
            field_name = 'dep_{}'.format(substance)
            fields.append(QgsField(field_name, QVariant.Double))
        if self.imaer_version in ['5.0', '5.1']:
            fields.append(QgsField('edge_effect', QVariant.LongLong))
        self.conn.createVectorTable('', 'receptors', fields, QgsWkbTypes.Polygon, QgsCoordinateReferenceSystem(epsg_id), True, {})

    def save_metadata(self, key, value):
        layer = QgsVectorLayer('{}|layername={}'.format(self.gpkg_fn, 'imaer_metadata'), 'metadata', 'ogr')
        provider = layer.dataProvider()

        feat = QgsFeature()
        feat.setAttributes([None, key, value])
        provider.addFeatures([feat])

    def process_rp(self, elem, as_dict=False, full=False):
        result = {}
        result['receptorPointId'] = elem.attrib['receptorPointId']

        if full:
            pnt = elem.findall('imaer:GM_Point/gml:Point', self.namespaces)[0]
            srs = pnt.attrib['srsName']
            srs = srs.split('::')[1]
            result['epsg'] = srs

        pos = elem.findall('imaer:GM_Point/gml:Point/gml:pos', self.namespaces)[0].text.split()
        result['point_x'] = pos[0]
        result['point_y'] = pos[1]

        coords = elem.findall('imaer:representation/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList', self.namespaces)
        if len(coords) == 1:
            coords = coords[0].text
            gml_numbers = coords.split()
            if len(gml_numbers) == 14:
                wkt_coord_list = []
                i = 0
                while i < len(gml_numbers):
                    wkt_coord_list.append('{} {}'.format(gml_numbers[i], gml_numbers[i + 1]))
                    i += 2
                wkt_coords = ', '.join(wkt_coord_list)
                result['polygon_wkt'] = 'POLYGON(({}))'.format(wkt_coords)

        if full:
            result['result_fields'] = []

        # Setting these globally when detecting the imaer_version could speed up the import. (todo)
        if self.imaer_version == '2.2':
            result_path = 'imaer:result/imaer:Result'
        elif self.imaer_version in ['3.1', '4.0', '5.0', '5.1']:
            result_path = 'imaer:result/imaer:CalculationResult'

        for res in elem.findall(result_path, self.namespaces):
            substance = res.attrib['substance']
            val = res.findall('imaer:value', self.namespaces)[0].text
            field_name = 'dep_{}'.format(substance)
            if full:
                result['result_fields'].append(field_name)
            result[field_name] = float(val)

        # edge effect
        if self.imaer_version in ['5.0', '5.1']:
            result['edge_effect'] = None
            edge_effects = elem.findall('imaer:edgeEffect', self.namespaces)
            if len(edge_effects) == 1:
                value = edge_effects[0].text
                result['edge_effect'] = _EDGE_EFFECT_VALUES.get(value, None)

        # print(result)
        if as_dict:
            return result

        if 'polygon_wkt' not in result:
            # Cannot create feature because of lacking hexagon info (TODO: Support points as well)
            return None

        feat = QgsFeature()
        geom = QgsGeometry.fromWkt(result['polygon_wkt'])
        feat.setGeometry(geom)

        attributes = []
        attributes.append(int(result['receptorPointId']))
        attributes.append(float(result['point_x']))
        attributes.append(float(result['point_y']))

        for substance in _IMAER_DEPOSITION_SUBSTANCES:
            field_name = 'dep_{}'.format(substance)
            if field_name in result:
                attributes.append(float(result[field_name]))
            else:
                attributes.append(None)
        if self.imaer_version in ['5.0', '5.1']:
            attributes.append(result['edge_effect'])

        feat.setAttributes(attributes)

        return feat
