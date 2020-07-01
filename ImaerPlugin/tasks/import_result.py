import os
import xml.etree.ElementTree as ET

from qgis.PyQt.QtCore import QVariant
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
    QgsExpressionContextUtils
    )

from .. task_timer import TaskTimer

_IMAER_DEPOSITION_SUBSTANCES = ['NH3', 'NOX', 'NO2']




class ImportImaerCalculatorResultTask(QgsTask):

    def __init__(self, gml_fn, gpkg_fn, load_layer_callback):
        super().__init__('Import IMAER Calculator Result', QgsTask.CanCancel)
        self.gml_fn = gml_fn
        self.gpkg_fn = gpkg_fn
        self.load_layer_callback = load_layer_callback
        self.exception = None
        self.do_log = True
        #self.log(self.gml_fn)
        self.namespaces = {}
        self.task_timer = TaskTimer()
        self.feat_timer = TaskTimer()


    def run(self):
        self.log('Started task "{}"'.format(self.description()))

        self.task_timer.log('gpkg')
        self.create_gpkg()

        self.task_timer.log('layer')
        receptors_layer = QgsVectorLayer(self.gpkg_fn, 'receptors', 'ogr')
        receptors_layer.startEditing()
        #receptors_provider = receptors_layer.dataProvider()

        rp_cnt = 0

        self.task_timer.log('get_file_size')
        with open(self.gml_fn, 'rb') as gml_file:
            gml_file_size = float(os.fstat(gml_file.fileno()).st_size)
            step = max(int(gml_file_size / 160000), 1)
            self.setProgress(0)
            self.task_timer.log('parsing')

            context = ET.iterparse(gml_file, events=('start', 'end', 'start-ns'))

            root = None
            for event, elem in context:
                self.task_timer.log('parsing')

                #self.log('{}, {}'.format(event, elem))

                # set the first element as root
                if root is None and event == 'start':
                    root = elem

                if event == 'start-ns':
                    self.namespaces[elem[0]] = elem[1]

                if event == 'end' and elem.tag == '{http://imaer.aerius.nl/2.2}featureMember':
                    child = list(elem)[0]
                    #self.log('  {}'.format(child.tag))
                    if child.tag == '{http://imaer.aerius.nl/2.2}ReceptorPoint':
                        feat = self.process_rp(child)
                        self.task_timer.log('add feature')
                        receptors_layer.addFeature(feat)
                        rp_cnt += 1
                        self.task_timer.log('clear elem')
                        elem.clear()

                self.task_timer.log('set progress')
                if (rp_cnt) % step == 0:
                    self.setProgress( (gml_file.tell() / gml_file_size) * 100)

                if self.isCanceled():
                    return False

            receptors_layer.commitChanges()
        for key in self.namespaces:
            ET.register_namespace(key, self.namespaces[key])
        xml_string = ET.tostring(root).decode('utf-8')
        xml_string = xml_string.replace('<imaer:featureMember />', '')
        #self.log(xml_string)
        self.save_metadata('xml', xml_string)
        self.save_metadata('gml_fn', self.gml_fn)
        self.save_metadata('user', QgsExpressionContextUtils().globalScope().variable('user_full_name'))

        return True


    def finished(self, result):
        self.log('finished task')
        #self.conn.close()
        if result:
            self.log(
                'ImaerResultToGpkgTask "{name}" completed'.format(
                  name=self.description()))
            self.log(self.task_timer.show())
            self.log(self.feat_timer.show())
            self.log(self.task_timer.add_feat_times)
            self.load_layer_callback(self.gpkg_fn)
        else:
            if self.exception is None:
                self.log(
                    'Task "{name}" not successful but without '\
                    'exception (probably the task was manually '\
                    'canceled by the user)'.format(
                        name=self.description()))
            else:
                self.log(
                    'Task "{name}" Exception: {exception}'.format(
                        name=self.description(),
                        exception=self.exception))
                raise self.exception
        #self.conn.close()


    def cancel(self):
        self.log(
            'Task "{name}" was canceled'.format(
                name=self.description()))
                # TODO delete gpkg file
        super().cancel()


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def create_gpkg(self):
        md = QgsProviderRegistry.instance().providerMetadata('ogr')
        self.conn = md.createConnection(self.gpkg_fn, {})

        fields = QgsFields()
        fields.append(QgsField('key', QVariant.String))
        fields.append(QgsField('value', QVariant.String))
        self.conn.createVectorTable('', 'metadata', fields, QgsWkbTypes.NoGeometry, QgsCoordinateReferenceSystem(), True, {})

        fields = QgsFields()
        fields.append(QgsField('point_x', QVariant.Double))
        fields.append(QgsField('point_y', QVariant.Double))
        for substance in _IMAER_DEPOSITION_SUBSTANCES:
            field_name = 'DEP_{}'.format(substance)
            fields.append(QgsField(field_name, QVariant.Double))
        self.conn.createVectorTable('', 'receptors', fields, QgsWkbTypes.Polygon, QgsCoordinateReferenceSystem(28992), True, {})


    def save_metadata(self, key, value):
        layer = QgsVectorLayer('{}|layername={}'.format(self.gpkg_fn, 'metadata'), 'metadata', 'ogr')
        provider = layer.dataProvider()

        feat = QgsFeature()
        feat.setAttributes([None, key, value])
        provider.addFeatures([feat])


    def process_rp(self, elem, as_dict=False, full=False):
        self.task_timer.log('rp')
        result = {}
        result['receptorPointId'] = elem.attrib['receptorPointId']

        if full:
            self.task_timer.log('full')
            pnt = elem.findall('imaer:GM_Point/gml:Point', self.namespaces)[0]
            srs = pnt.attrib['srsName']
            srs = srs.split('::')[1]
            result['epsg'] = srs

        self.task_timer.log('point')
        pos = elem.findall('imaer:GM_Point/gml:Point/gml:pos', self.namespaces)[0].text.split()
        result['point_x'] = pos[0]
        result['point_y'] = pos[1]

        self.task_timer.log('polygon')
        coords = elem.findall('imaer:representation/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList', self.namespaces)[0].text
        gml_numbers = coords.split()
        if not len(gml_numbers) == 14:
            pass
        wkt_coord_list = []
        i = 0
        while i < len(gml_numbers):
            wkt_coord_list.append('{} {}'.format(gml_numbers[i], gml_numbers[i+1]))
            i += 2
        wkt_coords = ', '.join(wkt_coord_list)
        result['polygon_wkt'] = 'POLYGON(({}))'.format(wkt_coords)

        if full:
            self.task_timer.log('full')
            result['result_fields'] = []

        self.task_timer.log('result')
        for res in elem.findall('imaer:result/imaer:Result', self.namespaces):
            substance = res.attrib['substance']
            val = res.findall('imaer:value', self.namespaces)[0].text
            field_name = 'DEP_{}'.format(substance)
            if full:
                result['result_fields'].append(field_name)
            result[field_name] = float(val)

        if as_dict:
            return result

        self.task_timer.log('feat')
        self.feat_timer.log('  init')
        feat = QgsFeature()
        self.feat_timer.log('  wkt')
        geom = QgsGeometry.fromWkt(result['polygon_wkt'])
        self.feat_timer.log('  set geom')
        feat.setGeometry(geom)

        self.feat_timer.log('  attr simple')
        attributes = []
        attributes.append(int(result['receptorPointId']))
        attributes.append(float(result['point_x']))
        attributes.append(float(result['point_y']))
        self.feat_timer.log('  attr dep')

        for substance in _IMAER_DEPOSITION_SUBSTANCES:
            field_name = 'DEP_{}'.format(substance)
            if field_name in result:
                attributes.append(float(result[field_name]))
            else:
                attributes.append(None)
        self.feat_timer.log('  set attr')
        feat.setAttributes(attributes)
        self.task_timer.log('void')
        self.feat_timer.log('  void')

        return feat
