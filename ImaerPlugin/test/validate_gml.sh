#!/bin/bash

lp='C:/Program Files/QGIS 3.16.13/lib'
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${lp}
#echo ${LD_LIBRARY_PATH}

python3 validate_gml.py $*
