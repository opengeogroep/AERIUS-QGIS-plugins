import xml.etree.ElementTree as ET
from time import sleep

from qgis.core import (
    Qgis,
    QgsTask,
    QgsMessageLog
    )

_IMAER_DEPOSITION_SUBSTANCES = ['NH3', 'NOX', 'NO2']




class ExportImaerCalculatorResultTask(QgsTask):

    def __init__(self, receptor_layer, gml_fn):
        super().__init__('Export to IMAER Calculator Result', QgsTask.CanCancel)
        self.receptor_layer = receptor_layer
        self.gml_fn = gml_fn
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

        for feat in self.receptor_layer.getFeatures():
            feat_i += 1
            self.log(feat)
            self.setProgress((feat_i / feat_cnt) * 100)
            sleep(0.01)

            if self.isCanceled():
                return False

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
        pass
