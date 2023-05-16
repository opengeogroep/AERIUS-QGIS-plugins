import os.path
import sys
import unittest
import json
from pkg_resources import IMetadataProvider
import yaml
import time

import faulthandler
faulthandler.enable()

# Get settings for local dev
with open('test/dev.yml') as file:
    try:
        dev_config = yaml.safe_load(file)
        # print(dev_config)
    except yaml.YAMLError as exc:
        print(exc)

sys.path.append(dev_config['path_qgis_python_folder'])

from qgis.core import QgsGeometry, Qgis

from qgis.core import *

from imaer5 import *
from connect import *
from tasks.import_calc_result import ImportImaerCalculatorResultTask

_GEOM0 = QgsGeometry.fromWkt('POINT(148458.0 411641.0)')
_GEOM1 = QgsGeometry.fromWkt('LINESTRING((1 0, 2 1, 3 0))')
_GEOM2 = QgsGeometry.fromWkt('MULTIPOLYGON(((1 0, 2 1, 3 0, 2 -1, 1 0)))')
_GEOM3 = QgsGeometry.fromWkt('LINESTRING((311279.0 723504.3, 311262.5 723349.6))')

class TestImaer(unittest.TestCase):

    def __init__(self, whatever):
        unittest.TestCase.__init__(self, whatever)
        # connect_base_url = dev_config['connect_base_url']
        # connect_version = dev_config['connect_version']
        # connect_key = dev_config['connect_key']
        # self.aerius_connection = AeriusConnection(None, base_url=connect_base_url, version=connect_version, api_key=connect_key)
        # print(self.aerius_connection)

    def compare_files(self, fn1, fn2):
        with open(fn1, 'r') as f1:
            content1 = f1.read()
        with open(fn2, 'r') as f2:
            content2 = f2.read()
        return content1 == content2

    # This test always fails because the Qt XML exporter puts data in random
    # order and therefore the text files are (almost) never exactly the same.
    def run_file_test(self, fcc, name):
        output_fn = os.path.join('test', 'output', f'output_{name}.gml')
        verify_fn = os.path.join('test', 'output', f'verify_{name}.gml')
        fcc.to_xml_file(output_fn)
        self.assertTrue(self.compare_files(output_fn, verify_fn))

    # This function does NOT work yet!!
    def run_validation_test(self, fcc, name):
        output_fn = os.path.join('test', 'output', f'output_{name}.gml')
        fcc.to_xml_file(output_fn)

        #self.log(self.aerius_connection, user='user')
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
        #self.run_file_test(fcc, 'empty')
        self.run_validation_test(fcc, 'empty')

    def test_ffc_metadata(self):
        fcc = ImaerDocument()
        fcc.metadata = AeriusCalculatorMetadata(
            project={'year': 2020, 'description': 'Some description...'},
            situation={'name': 'Situation 1', 'reference': 'ABCDE12345'},
            calculation={},
            version={'aeriusVersion': '2019A_20200610_3aefc4c15b', 'databaseVersion': '2019A_20200610_3aefc4c15b'}
        )
        #self.run_ffc_test(fcc, 'metadata')

    def test_ffc_emission_simple(self):
        fcc = ImaerDocument()
        es = EmissionSource(local_id='ES.123', sector_id=9000, label='Bron 123', geom=_GEOM0, epsg_id=28992)
        es.emissions.append(Emission('NH3', 1))
        fcc.feature_members.append(es)
        self.run_validation_test(fcc, 'em_simple')

    def test_ffc_emission_characteristics01(self):
        hc = SpecifiedHeatContent(value=12.5)
        es = EmissionSource(local_id='ES.123', sector_id=9999, label='Bron 123', geom=_GEOM1, epsg_id=28992)
        es.emission_source_characteristics = EmissionSourceCharacteristics(heat_content=hc, emission_height=2.4, spread=3, diurnal_variation='CONTINUOUS')
        es.emissions.append(Emission('NH3', 1))
        es.emissions.append(Emission('NOX', 3.3))
        fcc = ImaerDocument()
        fcc.feature_members.append(es)
        #self.run_ffc_test(fcc, 'characteristics01')

    def test_create_srm2road(self):
        es = SRM2Road(
            local_id='ES.33',
            sector_id='3100',
            label='testlabel',
            geom=_GEOM1,
            epsg_id=28992,
            road_area_type='NL',
            road_type='FREEWAY')
        fcc = ImaerDocument()
        fcc.feature_members.append(es)
        self.run_validation_test(fcc, 'srm2road')

    def test_create_adms_road(self):
        # setup the barrier (left)
        b1 = AdmsRoadSideBarrier(type='BRICK_WALL',
                                 distance=5,
                                 Avheight=7,
                                 Maxheight=10,
                                 Minheight=3,
                                 porosity=5)

        # this is creating the Emissions Source Type (including left barrier)
        es = ADMSRoad(
            local_id='ES.33',
            sector_id='3100',
            label='testlabel',
            geom=_GEOM3,
            epsg_id=27700,
            road_area_type='Sco',
            road_type='Urb',
            tunnel_factor=None,
            elevation=2,
            elevation_height=None,
            gradient=0.5,
            width=8,
            coverage=0,
            barrier_left=b1)

        # want to create ADMS road vehicle info (standard vehicle)
        v1 = StandardVehicle(vehicles_per_time_unit=1000,
                             time_unit='DAY',
                             vehicle_type='Bus',
                             maximum_speed=50,
                             strict_enforcement='false',
                             stagnation_factor=0.0)
        # add the vehicle created above to the emission source
        es.vehicles.append(v1)

        fcc = ImaerDocument()
        fcc.feature_members.append(es)

        self.run_validation_test(fcc, 'admsroad')

if __name__ == '__main__':
    QgsApplication.setPrefixPath("/home/raymond/programs/qgis/qgis-3.22/share/qgis/python/", True)
    qgs = QgsApplication([], True)
    qgs.initQgis()

    unittest.main()

    qgs.exitQgis()
