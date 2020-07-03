import xml.etree.ElementTree as ET
from time import sleep

from qgis.core import (
    Qgis,
    QgsTask,
    QgsMessageLog
    )

_IMAER_DEPOSITION_SUBSTANCES = ['NH3', 'NOX', 'NO2']




class ExportImaerCalculatorResultTask(QgsTask):

    def __init__(self, receptor_layer, gml_fn, xml_lines):
        super().__init__('Export to IMAER Calculator Result', QgsTask.CanCancel)
        self.receptor_layer = receptor_layer
        self.gml_fn = gml_fn
        self.xml_lines = xml_lines
        self.exception = None
        self.do_log = True
        #self.log(self.gml_fn)


    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def run(self):
        self.log('Started task "{}"'.format(self.description()))

        feat_i = 0
        feat_cnt = self.receptor_layer.featureCount()


        with open(self.gml_fn, 'w') as gml_file:
            for line in self.xml_lines[:-1]:
                gml_file.write(line + '\n')

            for feat in self.receptor_layer.getFeatures():
                feat_i += 1
                self.log(feat)
                self.setProgress((feat_i / feat_cnt) * 100)
                sleep(0.005)

                receptor_xml = self.create_receptor_xml(feat)
                gml_file.write(receptor_xml)

                if self.isCanceled():
                    return False

            gml_file.write('    <!-- qgis generated imaer gml-->\n')

            gml_file.write(self.xml_lines[-1].strip())

        return True


    def finished(self, result):
        self.log('finished task')
        #self.conn.close()
        if result:
            self.log(
                'ImaerResultToGpkgTask "{name}" completed'.format(
                  name=self.description()))
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


    def cancel(self):
        self.log(
            'Task "{name}" was canceled'.format(
                name=self.description()))
                # TODO delete gpkg file
        super().cancel()


    def create_gml(self):
        pass


    def create_receptor_xml(self, feat):
        id = feat.attribute('fid')
        x = feat[1]
        y = feat[2]
        dep_nh3 = feat[3]
        dep_nox = feat[4]
        result = f'''
    <imaer:featureMember>
        <imaer:ReceptorPoint receptorPointId="{id}" gml:id="CP.{id}">
            <imaer:identifier>
                <imaer:NEN3610ID>
                    <imaer:namespace>NL.IMAER</imaer:namespace>
                    <imaer:localId>CP.{id}</imaer:localId>
                </imaer:NEN3610ID>
            </imaer:identifier>
            <imaer:GM_Point>
                <gml:Point srsName="urn:ogc:def:crs:EPSG::28992" gml:id="CP.{id}.POINT">
                    <gml:pos>{x} {y}</gml:pos>
                </gml:Point>
            </imaer:GM_Point>
            <imaer:representation>
                <gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992" gml:id="NL.IMAER.REPR.{id}">
                    <gml:exterior>
                        <gml:LinearRing>
                            <gml:posList>136432.0 408878.0 136463.0 408824.0 136432.0 408770.0 136370.0 408770.0 136339.0 408824.0 136370.0 408878.0 136432.0 408878.0</gml:posList>
                        </gml:LinearRing>
                    </gml:exterior>
                </gml:Polygon>
            </imaer:representation>\n'''

        for substance in _IMAER_DEPOSITION_SUBSTANCES:
            field_name = 'DEP_{}'.format(substance)
            value = feat.attribute(field_name)
            print(value, type(value))
            if isinstance(value, float):
                result += self.create_result_value_xml(substance, value)

        result += '''</imaer:ReceptorPoint>
    </imaer:featureMember>
'''
        return result


    def create_result_value_xml(self, substance, value):
        print(f'{substance}: {value}')
        result = f'''
            <imaer:result>
                <imaer:Result resultType="DEPOSITION" substance="{ substance }">
                    <imaer:value>{ value }</imaer:value>
                </imaer:Result>
            </imaer:result>
'''
        return result
