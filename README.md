# AERIUS IMAER plugin for QGIS

QGIS 3 plugin for working with IMAER files

## Documentation

The user documentation can be found here:
[Github Pages](http://opengeogroep.github.io/AERIUS-QGIS-plugins/)

## Running tests

* In the folder ```ImaerPlugin/test``` create a dev.yml file with your local settings (use dev_example.yml as a template)
* To run tests in Linux: Run ```./test_imaer.sh``` from the ImaerPlugin folder
* To run tests in Windows: Open the command line from the ImaerPlugin folder and run ```python -m unittest test.test_imaer```

## Releasing

* Make sure the plugin runs fine!
  * Runn tests
  * Test different QGIS versions
* Update the metadata.txt (version, changelog)
* Update the self.version in the ImaerPlugin class
* Run the release script: ```python3 Make_zip_release.py 3.0.0```
* Move the zip file to the ```releases``` directory
* For a new major or minor relese, create (and update) a copy of the documentation
* Upload to plugins.qgis.org

## Dependencies in AERIUS project

Changes in IMAER and CONNECT can affect the working of the plugin. 

## IMAER
* Version number
* Metadata
* Calculation results (depositions, concentrations)
* Emission sources:
  * generic ("other")
  * roads (adms & srmt)
  * buildings
  * diurnal variation / time varying profiles
  * calculation points
  * Connect API

## CONNECT
* Version number
* URL
* Services:
  * actuator/health
  * user/generateApiKey
  * jobs
  * wnb/calculate
  * receptorSets
  * utility/validate
