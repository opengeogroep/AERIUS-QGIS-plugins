Developers
**********

General setup
=============
This plug in for QGIS is meant to be a demonstrator. It is designed to be easily extensible and adaptable. Therefore the plug-in is split in two main parts:

- the ``imaerwrite`` module which handles the creation of valid IMAER gml
- the ``ImaerWriter`` module which provides the QGIS user interface and sends data to the imaerwrite module


imaerwrite module
=================
The imaerwrite module writes valid IMAER gml on the basis of passed in data. The module can be imported and used stand alone. Therefore it provides a basis for extending GIS (or other) software with the capability to write valid IMAER gml. 

The module has no dependencies outside of the Python core libraries. Only generic Emission Sources are supported.

Basic usage
-----------
Writing IMAER gml from python by using the imaerwrite module is simple:

Start by importing the module::

    import imaerwrite as imaer

Create an Emission source by providing an id and a geometry::

    e = imaer.EmissionSource(wktGeometry = 'POINT(25000 300000)', gmlId = 'ES.1')

.. note::
   Geometry should be valid WKT-geometry in the EPSG:28992 coordinate system.


Add an emission to the emission source::

    e.addEmission(imaer.EmissionSource.Emission('NH3',36152))

Create the writer object and pass in a list of Emission sources (a list of one in this case)::

    i = imaer.ImaerWrite(features = [e])

And save::

    i.save('test.gml')

Of course Emission Source Characteristics and a label can be added to an Emission Source::

    sc = imaer.EmissionSource.EmissionSourceCharacteristics(heatContent = 4, emissionHeight = 31)
    e = imaer.EmissionSource(wktGeometry = 'POINT(25000 300000)', 
                             emissionSourceCharacteristics = sc, label = 'test source', gmlId = 'ES.3')

And multiple Emissions can be added to an Emission source::

    e.addEmission(imaer.EmissionSource.Emission('NOX',3.3))
    e.addEmission(imaer.EmissionSource.Emission('NO2',4.12))

To demonstrate the use of the imaerwrite module a demo script ``basictest.py`` is included.


Extending the module with EmissionSourceTypes
---------------------------------------------
Up till now the imaerwrite module supports generic Emission source types only. Adding an Emission source type for a specific sector (eg farmLodging) requires the following steps:

- create a class FarmLodgingEmissionSource using the EmissionSource class as an example

  - create an ``__init__`` method exposing the needed attributes
  - add a ``dom`` property which constructs valid gml from the attributes

- add the new class name to the EmissionSourceTypes property of the ``ImaerWrite`` class.
- expose the attributes via the ``getUiFields`` method of the ``ImaerWrite`` class in a list of two lists: first list mandatory attributes, second list optional attributes
- test by extending the ``basictest.py`` script.
- don't forget to update this documentation!

Be sure the gml your code generates is valid xml according to the IMAER datamodel. Refer to the schema which location is available in the module constant ``_imaerSchemaLocation``. The UML is available at https://www.aerius.nl/nl/file/imaerumlv10pdf .


ImaerWriter module
==================
The ImaerWriter module has a standard QGIS plug-in setup. The basics were generated using the QGIS plugin builder plugin. 

- It provides an user interface (GUI) for the imaerwrite module. 
- It sends geometry and attributes from QGIS data sources to the imaerwrite module

The GUI was created with Qt4 Designer.

Extending the module with EmissionSourceTypes
---------------------------------------------
Up till now the ImaerWriter module supports generic Emission source types only. Adding an Emission source type for a specific sector (eg farmLodging) requires the following steps:

- Extend the ``imaerwrite`` module as described above
- Extend the GUI with the appropriate layout and/ or widgets

    - Edit ``ImaerWriter_dialog_base_ui`` with Qt4 Designer
    - don't forget to run make if you add resources like images

- Generate widgets in the GUI in the ``__init__`` method based on the ``getUiFields`` method from the ``ImaerWrite`` class in the ``imaerwrite`` module
- Extend the signal-slot communication in the ``__init__`` method
- Extend the ``run`` method to send the attributes and geometry to the new EmissionSourceType ``__init__`` method rom the ``ImaerWrite`` class in the ``imaerwrite`` module
- don't forget to update this documentation!
