#!/bin/bash

lp='/home/raymond/programs/qgis/qgis-3.22/lib/'
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${lp}
#echo ${LD_LIBRARY_PATH}

python3 validate_gml.py $*
