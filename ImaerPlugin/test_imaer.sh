#!/bin/bash
lp='C:/Program Files/QGIS 3.16.13/apps/Python39'
echo ${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${lp}
echo ${LD_LIBRARY_PATH}

'C:/Program Files/QGIS 3.16.13/apps/Python39/python3' -m unittest test/test_imaer.py
