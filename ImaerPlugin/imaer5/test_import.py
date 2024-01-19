import time

from PyQt5.QtCore import QXmlStreamReader, QFile

from .imaer5 import *

t0 = time.time()

fn = '/home/raymond/terglobo/projecten/aerius/202401_subreceptors/CAPER_demo_roads_including_results_20230116/AERIUS_20240116163736_0_Localroadplanwithbarrier.gml'
fn_short = '/home/raymond/terglobo/projecten/aerius/202401_subreceptors/CAPER_demo_roads_including_results_20230116/AERIUS_20240116163736_0_Localroadplanwithbarrier_short.gml'
fn_old = '/home/raymond/terglobo/projecten/aerius/202007_calc_input_plugin/demodata/AERIUS_gml_20201027090613_v31_result_2sit/AERIUS_20201027090613_0_Situatie1.gml'
fn_old_2mb = '/home/raymond/terglobo/projecten/ogg/aerius/data/AERIUS_Calculator_20150330082713_0_Situation1.gml'

doc = ImaerDocument()
print(doc)


for rp in receptor_points:
    #print(rp)
    for result in rp.results:
        pass#print(' ', result)

print(len(receptor_points))

print(time.time() - t0)