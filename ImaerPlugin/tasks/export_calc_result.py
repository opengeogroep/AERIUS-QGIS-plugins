import xml.etree.ElementTree as ET

# from PyQt5.QtXml import QDomDocument

from qgis.core import (
    Qgis,
    QgsTask,
    QgsMessageLog
)

from .. task_timer import TaskTimer


_IMAER_DEPOSITION_SUBSTANCES = ['NH3', 'NOX']
_SUPPORTED_IMAER_VERSIONS = ['2.2', '3.1', '4.0', '5.0']
_EDGE_EFFECT_VALUES = {0: 'false', 1: 'true'}

tab = 'Imaer'


class ExportImaerCalculatorResultTask(QgsTask):

    def __init__(self, receptor_layer, gml_fn, xml_lines, imaer_version):
        super().__init__('Export to IMAER Calculator Result', QgsTask.CanCancel)
        self.receptor_layer = receptor_layer
        self.gml_fn = gml_fn
        self.xml_lines = xml_lines
        self.imaer_version = imaer_version
        self.exception = None
        self.do_log = True
        # self.log(self.gml_fn)

        self.tt = TaskTimer()

    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)

    def run(self):
        self.tt.log('start')
        self.log('Started task "{}"'.format(self.description()))

        if self.imaer_version not in _SUPPORTED_IMAER_VERSIONS:
            self.exception = Exception(f'IMAER version {self.imaer_version} is not supported')
            return False

        feat_i = 0
        feat_cnt = self.receptor_layer.featureCount()

        with open(self.gml_fn, 'w') as gml_file:
            self.tt.log('writing header')

            gml_file.write('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n''')
            for line in self.xml_lines[:-1]:
                gml_file.write(line + '\n')

            self.tt.log('writing features')

            for feat in self.receptor_layer.getFeatures():
                feat_i += 1
                self.log(feat)
                self.setProgress((feat_i / feat_cnt) * 100)

                receptor_xml = self.create_receptor_xml(feat)
                self.tt.log('write')
                gml_file.write(receptor_xml)

                if self.isCanceled():
                    return False

            # gml_file.write('    <!-- qgis generated imaer gml-->\n')

            self.tt.log('writing footer')
            gml_file.write('\n')
            gml_file.write(self.xml_lines[-1].strip())

        return True

    def finished(self, result):
        self.log('finished task')
        # self.tt.show()
        # self.conn.close()
        if result:
            self.log(
                'ImaerResultToGpkgTask "{name}" completed'.format(
                    name=self.description()
                )
            )
        else:
            if self.exception is None:
                self.log(
                    f'Task "{name}" not successful but without '
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
            'Task "{name}" was canceled'.format(
                name=self.description()))
        # TODO delete gpkg file
        super().cancel()

    def create_receptor_xml(self, feat):
        # self.tt.log('attrs')
        id = feat['fid']
        x = feat['point_x']
        y = feat['point_y']
        # self.tt.log('poslist')
        poslist = self.poslist_from_polygon(feat)
        # self.tt.log('format')
        result = f'''
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="{ id }" gml:id="CP.{ id }">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.{ id }</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.{ id }.POINT">
                    <gml:pos>{ x } { y }</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.{ id }">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>{ poslist }</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>'''

        # self.tt.log('substances')
        for substance in _IMAER_DEPOSITION_SUBSTANCES:
            field_name = 'dep_{}'.format(substance)
            value = feat.attribute(field_name)
            if isinstance(value, float):  # empty records are returned as <class 'qgis.PyQt.QtCore.QVariant'> NULL values
                result += self.create_result_value_xml(substance, value)

        # Add edgeEffect info for IMAER >= 5.0
        if self.imaer_version in ['5.0']:
            value = feat.attribute('edge_effect')
            if value in _EDGE_EFFECT_VALUES:
                result += f'''
            <imaer:edgeEffect>{ _EDGE_EFFECT_VALUES[value] }</imaer:edgeEffect>'''

        result += '''
        </imaer:ReceptorPoint>
    </imaer:featureMember>'''
        self.tt.log('void')
        return result

    def create_result_value_xml(self, substance, value):
        if self.imaer_version == '2.2':
            result_tag = 'Result'
        elif self.imaer_version in ['3.1', '4.0', '5.0']:
            result_tag = 'CalculationResult'
        result = f'''
            <imaer:result>
                <imaer:{ result_tag } resultType="DEPOSITION" substance="{ substance }">
                    <imaer:value>{ value }</imaer:value>
                </imaer:{ result_tag }>
            </imaer:result>'''
        return result

    def poslist_from_polygon(self, feat):
        geom = feat.geometry()
        polygon = geom.asPolygon()
        outer = polygon[0]
        poslist = []
        for point in outer:
            x = round(point.x(), 1)
            poslist.append(str(x))
            y = round(point.y(), 1)
            poslist.append(str(y))
        result = ' '.join(poslist)
        return result
