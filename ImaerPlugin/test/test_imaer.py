import os.path
import sys
import unittest

sys.path.append('/home/raymond/programs/qgis-master/share/qgis/python')
from qgis.core import QgsGeometry

from imaer import *

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
        verify_fn = os.path.join('test', 'output', f'verify_{name}.gml')
        fcc.write_to_file(output_fn)
        self.assertTrue(self.compare_files(output_fn, verify_fn))


    def test_ffc_empty(self):
        fcc = FeatureCollectionCalculator()
        self.run_ffc_test(fcc, 'empty')


    def test_ffc_metadata(self):
        fcc = FeatureCollectionCalculator()
        fcc.metadata = AeriusCalculatorMetadata(
            project = {'year': 2020, 'description': 'SOme description...'},
            situation = {'name': 'Situation 1', 'reference': 'ABCDE12345'},
            calculation = {},
            version = {'aeriusVersion': '2019A_20200610_3aefc4c15b', 'databaseVersion': '2019A_20200610_3aefc4c15b'}
        )
        self.run_ffc_test(fcc, 'metadata')


    def test_ffc_emission_simple(self):
        fcc = FeatureCollectionCalculator()
        es = EmissionSource('ES.123', 9000, 'Bron 123', _GEOM0, 28992)
        es.add_emission('NH3', 1)
        fcc.add_feature_member(es)
        self.run_ffc_test(fcc, 'em_simple')


    def test_ffc_emission_characteristics01(self):
        hc = SpecifiedHeatContent(12.5)
        esc = EmissionSourceCharacteristics(hc, 2.4, spread=3, diurnal_variation='CONTINUOUS')
        es = EmissionSource('ES.123', 9999, 'Bron 123', _GEOM1, 28992, es_characteristics=esc)
        es.add_emission('NH3', 1)
        es.add_emission('NOX', 3.3)
        fcc = FeatureCollectionCalculator()
        fcc.add_feature_member(es)
        self.run_ffc_test(fcc, 'characteristics01')


    def test_ffc_emission_characteristics02(self):
        hc = CalculatedHeatContent(11.85, 0.1, 0.0, 'VERTICAL')
        esc = EmissionSourceCharacteristics(hc, 2.4, spread=3, diurnal_variation='CONTINUOUS')
        es = EmissionSource('ES.123', 9999, 'Bron 123', _GEOM1, 28992, es_characteristics=esc)
        es.add_emission('NH3', 1)
        es.add_emission('NOX', 3.3)
        fcc = FeatureCollectionCalculator()
        fcc.add_feature_member(es)
        self.run_ffc_test(fcc, 'characteristics02')


    def test_ffc_emission_building(self):
        hc = SpecifiedHeatContent(2.5)
        bld = Building(3.0, 1.5, 10, 0)
        esc = EmissionSourceCharacteristics(hc, 2.4, spread=3, diurnal_variation='CONTINUOUS', building=bld)
        es = EmissionSource('ES.123', 9999, 'Bron 123', _GEOM2, 28992, es_characteristics=esc)
        es.add_emission('NH3', 5.5)
        es.add_emission('NOX', 0.0)
        fcc = FeatureCollectionCalculator()
        fcc.add_feature_member(es)
        self.run_ffc_test(fcc, 'building')




if __name__ == '__main__':
    unittest.main()
