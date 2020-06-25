import random
from time import sleep
import os

import xml.etree.ElementTree as ET

from qgis.core import (
    Qgis,
    QgsApplication,
    QgsTask,
    QgsMessageLog
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


        rp_cnt = 0
        es_cnt = 0

        #for i in range(100):
        #    self.
        with open(self.gml_fn, 'rb') as gml_file:
            gml_file_size = float(os.fstat(gml_file.fileno()).st_size)
            for event, elem in ET.iterparse(gml_file):
                self.log('{}, {}'.format(event, elem.tag))
                if elem.tag == '{http://imaer.aerius.nl/2.2}featureMember':
                    child = list(elem)[0]
                    self.log('  {}'.format(child.tag))
                    if child.tag == '{http://imaer.aerius.nl/2.2}ReceptorPoint':
                        self.process_rp(child)
                        rp_cnt += 1
                        self.log(gml_file.tell())
                    elif child.tag == '{http://imaer.aerius.nl/2.2}EmissionSource':
                        self.process_es(child)
                        es_cnt += 1
                    elem.clear()
                if (es_cnt + rp_cnt) % 1 == 0:
                    self.log('{}, {}'.format(es_cnt, rp_cnt))
                    self.setProgress( (gml_file.tell() / gml_file_size) * 100)
                if self.isCanceled():
                    return False



        '''for i in range(100):
            sleep(wait_time)
            # use setProgress to report progress
            self.setProgress(i)
            arandominteger = random.randint(0, 500)
            self.total += arandominteger
            self.iterations += 1
            # check isCanceled() to handle cancellation
            if self.isCanceled():
                return False
            # simulate exceptions to show how to abort task
            if arandominteger == 42:
                # DO NOT raise Exception('bad value!')
                # this would crash QGIS
                self.exception = Exception('bad value!')
                return False'''
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


    def cancel(self):
        self.log(
            'RandomTask "{name}" was canceled'.format(
                name=self.description()))
        super().cancel()




    def log(self, message, tab='Imaer'):
        if self.do_log:
            QgsMessageLog.logMessage(str(message), tab, level=Qgis.Info)


    def create_gpkg(self, rcp):
        pass


    def process_es(self, elem):
        pass
        #print('EmissionSource')


    def process_rp(self, elem):
        pass
        self.log('ReceptorPoint')
        sleep(0.01)
