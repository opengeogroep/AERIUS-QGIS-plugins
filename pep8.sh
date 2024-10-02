pep8 --ignore E124,E128,E402,E501,E722 \
--exclude ImaerPlugin/config/validation_variables.py \
--count \
ImaerPlugin/*.py \
ImaerPlugin/algs/*.py \
ImaerPlugin/config/*.py \
ImaerPlugin/connect/*.py \
ImaerPlugin/gpkg/*.py \
ImaerPlugin/imaer*/*.py \
ImaerPlugin/styles/*.py \
ImaerPlugin/tasks/*.py \
ImaerPlugin/test/*.py

# E124 continuation line under-indented for visual indent
# E128 closing bracket does not match visual indentation
# E402 module level import not at top of file
# E501 line too long (80 > 79 characters)
# E722 do not use bare 'except'
