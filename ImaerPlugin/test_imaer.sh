#!/bin/bash

lp=$(grep 'lp_paths' test/dev.yml | awk '{print $2}' | tr -d '"')
echo ${lp}

# echo ${PATH}
#PATH=${PATH}\:${lp}
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${lp}
# export PATH
echo ${LD_LIBRARY_PATH}

#python connect/test.py
python3 -m unittest test.test_imaer
