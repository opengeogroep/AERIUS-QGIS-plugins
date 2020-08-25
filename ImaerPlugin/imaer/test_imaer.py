import os
import time
import xml.etree.ElementTree as ET

import site
site.addsitedir('/home/raymond/programs/qgis-3.10/share/qgis/python')

# not working, so run manually:
# export LD_LIBRARY_PATH='/home/raymond/programs/qgis-3.10/lib'
import os
os.environ['LD_LIBRARY_PATH'] = '/home/raymond/programs/qgis-3.10/lib'

from qgis.core import QgsGeometry

from main import FeatureCollectionCalculator, AeriusCalculatorMetadata, EmissionSource



fcc = FeatureCollectionCalculator()
print(fcc)

md = AeriusCalculatorMetadata()
fcc.metadata = AeriusCalculatorMetadata(
    project = {'year': 2020, 'description': 'DD'},
    situation = {'name': 'Situatie 2', 'reference': ''},
    calculation = {},#{'type': 'PERMIT', 'substances': ['NOX', 'NO2', 'NH3'], 'resultType': 'DEPOSITION'},
    version = {'aeriusVersion': '2019A_20200610_3aefc4c15b', 'databaseVersion': '2019A_20200610_3aefc4c15b'}
)

geom0 = QgsGeometry.fromWkt('POINT(148458.0 411641.0)')
geom1 = QgsGeometry.fromWkt('LINESTRING((1 0, 2 1, 3 0))')
geom2 = QgsGeometry.fromWkt('POLYGON((1 0, 2 1, 3 0, 2 -1, 1 0))')

es1 = EmissionSource('ES.123', 'Bron 123', geom0, 28992)
es1.add_emission('NH3', 1)
es1.add_emission('NOX', 3.3)
fcc.add_feature_member(es1)

es2 = EmissionSource('ES.456', 'Bron 456 line', geom2, 28992)
es2.add_emission('NH3', 11)
es2.add_emission('NOX', 12)
#fcc.add_feature_member(es2)


dom = fcc.generate_dom()
#print(dom)

#uglyXml = dom.toprettyxml(indent='  ', newl='\n', encoding="UTF-8")

print()
print(fcc.get_pretty_xml())

out_path = '/home/raymond/terglobo/projecten/aerius/202007_calc_input_plugin/demodata/gen_calc_input'
out_fn = time.strftime("calcinput_%Y%m%d_%H%M%S.gml")
filename = os.path.join(out_path, out_fn)
fcc.write_to_file(filename)
