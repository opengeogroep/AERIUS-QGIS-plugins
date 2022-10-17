#!/bin/bash

lp='C:/Program Files/QGIS 3.16.13/bin':'C:/Program Files/QGIS 3.16.13/apps/qgis-ltr/bin'
# echo ${PATH}
PATH=${PATH}\:${lp} 
export PATH
# echo ${PATH}

python connect/test.py
# python -m unittest test.test_imaer.py