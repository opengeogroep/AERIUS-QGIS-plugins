import os.path
import sys
import unittest
import yaml
import logging

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

from qgis.core import *

from imaer6 import *

_fn = '/home/raymond/terglobo/projecten/aerius/202401_subreceptors/CAPER_demo_roads_including_results_20230116/AERIUS_20240116163736_0_Localroadplanwithbarrier.gml'
_fn_short = '/home/raymond/terglobo/projecten/aerius/202401_subreceptors/CAPER_demo_roads_including_results_20230116/AERIUS_20240116163736_0_Localroadplanwithbarrier_short.gml'
_fn_old = '/home/raymond/terglobo/projecten/aerius/202007_calc_input_plugin/demodata/AERIUS_gml_20201027090613_v31_result_2sit/AERIUS_20201027090613_0_Situatie1.gml'

logging.basicConfig(filename='/tmp/test_imaer_parse.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG)
logging.warning('initializing script')

class TestImaerParse(unittest.TestCase):

    def __init__(self, whatever):
        logging.debug('init class')
        unittest.TestCase.__init__(self, whatever)
    
    def parse_calculation_results(self):
        file = QFile(_fn_short)

        logging.debug('kaas')

        file.open(QFile.ReadOnly | QFile.Text)
        print(file)

        receptor_points = []

        xml_reader = QXmlStreamReader(file)
        print(xml_reader)

        xml_reader.readNext()

        while not xml_reader.atEnd():
            if xml_reader.isStartElement():
                tag_name = xml_reader.name()
                #print(tag_name)
                if tag_name == 'featureMember':
                    xml_reader.readNextStartElement()
                    tag_name = xml_reader.name()
                    if tag_name == 'ReceptorPoint':
                        #print(f'  Processing {tag_name}')
                        rp = ReceptorPoint()
                        rp.from_xml_reader(xml_reader)
                        if rp.is_valid():
                            receptor_points.append(rp)
                    else:
                        print(f'  Skipping {tag_name}')
                        xml_reader.skipCurrentElement()
            xml_reader.readNext()
        if xml_reader.hasError():
            pass

        for rp in receptor_points:
            #print(rp)
            for result in rp.results:
                pass#print(' ', result)

        print(len(receptor_points))

