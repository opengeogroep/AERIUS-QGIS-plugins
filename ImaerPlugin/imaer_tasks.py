import random
from time import sleep
import os

import xml.etree.ElementTree as ET

from qgis.PyQt.QtCore import QVariant

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsTask,
    QgsMessageLog,
    QgsProviderRegistry,
    QgsCoordinateReferenceSystem,
    QgsFields,
    QgsField,
    QgsWkbTypes,
    QgsFeature,
    QgsGeometry,
    QgsVectorLayer
    )

IMAER_RESULT_ATTRIBUTES = ['DEP_NH3','DEP_NH3']




class ImaerResultToGpkgTask(QgsTask):
    """This shows how to subclass QgsTask"""

    def __init__(self, gml_fn, gpkg_fn):
        super().__init__('Imaer Result To Gpkg Task', QgsTask.CanCancel)
        self.gml_fn = gml_fn
        self.gpkg_fn = gpkg_fn
        self.exception = None
        self.do_log = True
        self.log('doet de log het?')
        self.log(self.gml_fn)
        self.namespaces = {}


    def run(self):
        """Here you implement your heavy lifting.
        Should periodically test for isCanceled() to gracefully
        abort.
        This method MUST return True or False.
        Raising exceptions will crash QGIS, so we handle them
        internally and raise them in self.finished
        """
        self.log('Started task "{}"'.format(
                                     self.description()))

        self.create_gpkg()

        receptors_layer = QgsVectorLayer(self.gpkg_fn, 'receptors', 'ogr')
        receptors_provider = receptors_layer.dataProvider()

        rp_cnt = 0
        es_cnt = 0

        with open(self.gml_fn, 'rb') as gml_file:
            gml_file_size = float(os.fstat(gml_file.fileno()).st_size)

            context = ET.iterparse(gml_file, events=('start', 'end', 'start-ns'))
            #context = iter(context)
            #while not eventevent, root = context.__next__()
            #self.log(ET.dump(root))

            root = None
            for event, elem in context:
                #self.log('{}, {}'.format(event, elem))

                # set the first elemant as root
                if root is None and event == 'start':
                    root = elem

                if event == 'start-ns':
                    self.namespaces[elem[0]] = elem[1]
                    self.log(self.namespaces)

                if event == 'end' and elem.tag == '{http://imaer.aerius.nl/2.2}featureMember':
                    child = list(elem)[0]
                    self.log('  {}'.format(child.tag))
                    if child.tag == '{http://imaer.aerius.nl/2.2}ReceptorPoint':
                        feat = self.process_rp(child)
                        receptors_provider.addFeatures([feat])
                        rp_cnt += 1
                        elem.clear()
                    elif child.tag == '{http://imaer.aerius.nl/2.2}EmissionSource':
                        self.process_es(child)
                        es_cnt += 1

                if (es_cnt + rp_cnt) % 100 == 0:
                    #self.log('{}, {}'.format(es_cnt, rp_cnt))
                    self.setProgress( (gml_file.tell() / gml_file_size) * 100)

                if self.isCanceled():
                    return False

        for key in self.namespaces:
            self.log(key)
            ET.register_namespace(key, self.namespaces[key])
        xml_string = ET.tostring(root).decode('utf-8')
        self.log(len(xml_string))
        xml_string = xml_string.replace('<imaer:featureMember />', '')
        self.log(len(xml_string))
        #self.log(xml_string)
        self.save_metadata('xml', xml_string)

        return True


    def finished(self, result):
        """
        This function is automatically called when the task has
        completed (successfully or not).
        You implement finished() to do whatever follow-up stuff
        should happen after the task is complete.
        finished is always called from the main thread, so it's safe
        to do GUI operations and raise Python exceptions here.
        result is the return value from self.run.
        """
        self.log('finished task')
        if result:
            self.log(
                'RandomTask "{name}" completed\n' \
                'RandomTotal: {total} (with {iterations} '\
              'iterations)'.format(
                  name=self.description(),
                  total=self.total,
                  iterations=self.iterations))
        else:
            if self.exception is None:
                self.log(
                    'RandomTask "{name}" not successful but without '\
                    'exception (probably the task was manually '\
                    'canceled by the user)'.format(
                        name=self.description()))
            else:
                self.log(
                    'RandomTask "{name}" Exception: {exception}'.format(
                        name=self.description(),
                        exception=self.exception))
                raise self.exception
        #self.conn.close()


    def cancel(self):
        self.log(
            'RandomTask "{name}" was canceled'.format(
                name=self.description()))
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
        fields.append(QgsField('result_NH3', QVariant.Double))
        fields.append(QgsField('result_NOX', QVariant.Double))
        self.conn.createVectorTable('', 'receptors', fields, QgsWkbTypes.Polygon, QgsCoordinateReferenceSystem(28992), True, {})


    def save_metadata(self, key, value):
        layer = QgsVectorLayer('{}|layername={}'.format(self.gpkg_fn, 'metadata'), 'metadata', 'ogr')
        provider = layer.dataProvider()

        feat = QgsFeature()
        feat.setAttributes([None, key, value])
        provider.addFeatures([feat])


    def process_es(self, elem):
        pass
        #print('EmissionSource')


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

        coords = elem.findall('imaer:representation/gml:Polygon/gml:exterior/gml:LinearRing/gml:posList', self.namespaces)[0].text
        gml_numbers = coords.split()
        if not len(gml_numbers) == 14:
            print(gml_numbers)
        wkt_coord_list = []
        i = 0
        while i < len(gml_numbers):
            wkt_coord_list.append('{} {}'.format(gml_numbers[i], gml_numbers[i+1]))
            i += 2
        wkt_coords = ', '.join(wkt_coord_list)
        result['polygon_wkt'] = 'POLYGON(({}))'.format(wkt_coords)


        if full:
            result['result_fields'] = []

        for res in elem.findall('imaer:result/imaer:Result', self.namespaces):
            substance = res.attrib['substance']
            val = res.findall('imaer:value', self.namespaces)[0].text
            field_name = 'result_{}'.format(substance)
            if full:
                result['result_fields'].append(field_name)
            result[field_name] = float(val)

        if as_dict:
            return result

        feat = QgsFeature()
        geom = QgsGeometry.fromWkt(result['polygon_wkt'])
        feat.setGeometry(geom)

        attributes = []
        attributes.append(int(result['receptorPointId']))
        attributes.append(float(result['point_x']))
        attributes.append(float(result['point_y']))
        for substance in ['NH3', 'NOX']:
            field_name = 'result_{}'.format(substance)
            if field_name in result:
                attributes.append(float(result[field_name]))
            else:
                attributes.append(None)

        feat.setAttributes(attributes)

        return feat
