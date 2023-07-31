pep8 --ignore E402,E501,E722 \
--exclude ImaerPlugin/config/validation_variables.py \
ImaerPlugin/*.py \
ImaerPlugin/algs/*.py \
ImaerPlugin/config/*.py \
ImaerPlugin/connect/*.py \
ImaerPlugin/imaer*/*.py \
ImaerPlugin/tasks/*.py \
ImaerPlugin/test/*.py

# E402 module level import not at top of file
# E501 line too long (80 > 79 characters)
# E722 do not use bare 'except'
