import os.path
import sys
import unittest
import json
from pkg_resources import IMetadataProvider
import yaml

import faulthandler
faulthandler.enable()


with open('test/dev.yml') as file:
    try:
        databaseConfig = yaml.safe_load(file)   
        #print(databaseConfig)
    except yaml.YAMLError as exc:
        print(exc)


sys.path.append(databaseConfig['path_qgis_python_folder'])

from qgis.core import QgsGeometry, Qgis

from imaer4 import *
from connect import *

_GEOM0 = QgsGeometry.fromWkt('POINT(148458.0 411641.0)')
_GEOM1 = QgsGeometry.fromWkt('LINESTRING((1 0, 2 1, 3 0))')
_GEOM2 = QgsGeometry.fromWkt('MULTIPOLYGON(((1 0, 2 1, 3 0, 2 -1, 1 0)))')


class TestImaer(unittest.TestCase):

    def compare_files(self, fn1, fn2):
        with open(fn1, 'r') as f1:
            content1 = f1.read()
        with open(fn2, 'r') as f2:
            content2 = f2.read()
        return content1 == content2

    def run_ffc_test(self, fcc, name):
        output_fn = os.path.join('test', 'output', f'output_{name}.gml')
        fcc.to_xml_file(output_fn)
        connect_base_url = databaseConfig['connect_base_url']
        connect_version = databaseConfig['connect_version']
        connect_key = databaseConfig['connect_key']
        self.aerius_connection = AeriusConnection(self, base_url=connect_base_url, version=connect_version, api_key=connect_key)
        self.log(self.aerius_connection, user='user')
        # the below is failing with a segment error which is likely why trying to write to non existing file
        # breaks when put the api key in. if this none then works
        # result = self.aerius_connection.post_validate(output_fn)
        # # then still need to check if this result is valid
        # bstr = result.readAll()
        # result_dict = json.loads(bytes(bstr))
        # if 'successful' in result_dict and result_dict['successful']:
        #     print("Success")

    def log(self, message, tab='Imaer', lvl='Info', bar=False, user='user', duration=3):
        # lvl: Info, Warning, Critical
        # user: user, dev
        level = getattr(Qgis, lvl)
        # if bar or (user == 'user') or (user == 'dev' and self.dev):
        #    QgsMessageLog.logMessage(str(message), tab, level=level)
        # if bar:
        #   self.iface.messageBar().pushMessage(lvl, str(message), level, duration=duration)
        print(message)

    def test_ffc_empty(self):
        fcc = ImaerDocument()
        self.run_ffc_test(fcc, 'empty')

    def test_ffc_metadata(self):
        fcc = ImaerDocument()
        fcc.metadata = AeriusCalculatorMetadata(
            project={'year': 2020, 'description': 'SOme description...'},
            situation={'name': 'Situation 1', 'reference': 'ABCDE12345'},
            calculation={},
            version={'aeriusVersion': '2019A_20200610_3aefc4c15b', 'databaseVersion': '2019A_20200610_3aefc4c15b'}
        )
        self.run_ffc_test(fcc, 'metadata')

    def test_ffc_emission_simple(self):
        fcc = ImaerDocument()
        es = EmissionSource(local_id='ES.123', sector_id=9000, label='Bron 123', geom=_GEOM0)
        es.emissions.append(Emission('NH3', 1))
        fcc.feature_members.append(es)
        self.run_ffc_test(fcc, 'em_simple')

    def test_ffc_emission_characteristics01(self):
        hc = SpecifiedHeatContent(value=12.5)
        es = EmissionSource(local_id='ES.123', sector_id=9999, label='Bron 123', geom=_GEOM1)
        es.emission_source_characteristics = EmissionSourceCharacteristics(heat_content=hc, emission_height=2.4, spread=3, diurnal_variation='CONTINUOUS')
        es.emissions.append(Emission('NH3', 1))
        es.emissions.append(Emission('NOX', 3.3))
        fcc = ImaerDocument()
        fcc.feature_members.append(es)
        self.run_ffc_test(fcc, 'characteristics01')


if __name__ == '__main__':
    unittest.main()

