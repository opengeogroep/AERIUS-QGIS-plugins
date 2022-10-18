#!/bin/bash

#lp=$(grep -A3 'test:' dev.yml | tail -n1); db=${db//*database: /}; echo "$db"

lp='/home/raymond/programs/qgis/qgis-3.22/lib/'
# echo ${PATH}
#PATH=${PATH}\:${lp}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${lp}
# export PATH
echo ${LD_LIBRARY_PATH}

#python connect/test.py
python3 -m unittest test.test_imaer
