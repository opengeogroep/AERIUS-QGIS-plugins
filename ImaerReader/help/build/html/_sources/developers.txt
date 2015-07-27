Developers
**********

General setup
=============
This plug in for QGIS is meant to be a demonstrator. It is designed to be easily extensible and adaptable. Therefore the plug-in is split in two main parts:

- the ``imaerread`` module which handles the import of IMAER gml
- the ``imaer_reader`` module which provides the QGIS user interface and receives data from the imaerread module


imaerread module
================
The imaerread module reads IMAER gml and passes its features. The module can be imported and used stand alone. Therefore it provides a basis for extending GIS (or other) software with the capability to read AERIUS IMAER output. 

The module has no dependencies outside of the Python core libraries.

Basic usage
-----------
Reading IMAER gml from python by using the imaerread module is simple:

Start by importing the module::

    import imaerread

Create a reader object by providing a filename::

    ir = ImaerRead(gmlFile = 'filename.gml')

The gml file contains an unknown number of ReceptorPoint features. The nextFeature() function finds the next, parses it and returns a imaer feature object::

    ft = ir.nextFeature()
    
It uses the pulldom parser from the standard xml library, because the gml files can be too large to fit in memory.    
    
    
The features that are returned are python dictionaries with this structure::
    
    {
      u'id': u'3204036',
      u'DEP_NH3': 0.0502,
      u'DEP_NOX': 0.0123,
      u'DEP_NO2': 0.0456,
      u'DEP_PM10': 0.6783,
      u'DEP_PM25': 0.354,
      u'CON_NH3': 0.0789,
      u'CON_NOX': 0.0234,
      u'CON_NO2': 0.0567,
      u'CON_PM10': 0.0678,
      u'CON_PM25': 0.0345,
      u'point': u'POINT(148871.0 409361.0)',
      u'hexagon': u'POLYGON((148902.0 409415.0,148933.0 409361.0,148902.0 409307.0,148840.0 409307.0,148809.0 409361.0,148840.0 409415.0,148902.0 409415.0))'
    }

For efficiency, you can parse the parameters doPoints=False or doHexagons=False to prevent processing geometry you do not need. The returning object lacks the point or hexagon information.

Both point and and hexagon are returned in well known text (WKT) format to be parsed in most GIS libraries. 

imaer_reader module
===================

The ImaerWriter module has a standard QGIS plug-in setup. The basics were generated using the QGIS plugin builder plugin.

- It provides a user interface (GUI) for the imaerread module.
- It creates memory layers based on the imaer gml data.

The GUI was created with Qt4 Designer.

Source code van be found on `github <https://github.com/opengeogroep/AERIUS-QGIS-plugins/>`_. Any issues can also be reported there. There are also some demo files available there.




