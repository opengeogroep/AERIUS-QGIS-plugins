#!/bin/bash
lp=~/programs/qgis-master/lib/
echo ${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${lp}
echo ${LD_LIBRARY_PATH}
python3 -m unittest test/test_imaer.py
