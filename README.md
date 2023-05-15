# AERIUS IMAER plugin for QGIS

QGIS 3 plugin for working with IMAER files

## Documentation

The user documentation can be found here:
[Github Pages](http://opengeogroep.github.io/AERIUS-QGIS-plugins/)

## Releasing

* Make sure the plugin runs fine!
* Update the metadata.txt (version, changelog)
* Delete all ```__pycache__``` directories
* zip the ```Imaer_Plugin``` directory
* Rename zip file with version info
* Move the zip file to the ```releases``` directory
* Upload to plugins.qgis.org

## Running tests

* To run test in Linux: dev.yml must be created (use dev_example.yml as a template). Then run the test_imaer.sh from the plugin directory
* To run the test in Windows: dev.yml must be created (use dev_example.yml as a template). Then open the command line from the Imaer plugin folder and run python -m unittest test.test_imaer 