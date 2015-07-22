Usage
*****

Introduction
============
The plug-in writes valid IMAER-gml from any QGIS data source containing the proper IMAER information. For this you have to create a mapping from the attribute columns in your data source to the required and optional IMAER attributes.

Detailed instructions
=====================

Preparing your data
-------------------
First add data sources (eg. ESRI shape files) to your QGIS project. These data sources should contain the data of the Emission sources you want to export to an IMAER gml. Point, line and polygon Emission sources are supported.

Each Emission source should be one record (one row) in the attribute table. Each row should contain the properties for the Emission source as attributes (columns). As only generic Emission Sources are supported the following properties are *mandatory*:

- gmlId: an unique id for the Emission source

- One or more of the Emissions:

  - NH3
  - NO2
  - NOx
  - PM10
  - PM25

The following properties are *optional*:

- label: a human readable label to identify the Emission Source
- Emission Source Characteristics
  
  This is an element containing multiple attributes of which are *mandatory*:

  - heatContent
  - emissionHeight

  and *optionally* you can provide:

  - buildingHeight
  - spread
  - diurnalVariation

For a full understanding of the data required by AERIUS and modeled in IMAER gml please refer to the documentation at: https://www.aerius.nl/nl/factsheets/release/aerius-connect

Exporting your data
-------------------
As soon as your data is prepared you can launch the plug-in via it's icon or the plug-in menu. 

As an IMAER gml file can contain points, lines and polygons all at the same time you'll see three tabs where you can select an appropriate data source.

When you select a data source a section with  pick lists appear with which you can map your data source's attribute columns to IMAER attributes. 

E.g. when your data source has an attribute (column) named 'NH3_emis' containing NH3 emission values you select the column 'NH3_emis' in the pick list NH3 in the Emission section. 

When you are done mapping the attributes you can select a file to save to and click 'Save'. The plug-in will try and construct as many valid IMAER Emission Sources from your data as it can. If it finds any invalid entries which prevents the plug-in from creating a valid IMAER Emission source you will be warned with a warning message stating which record is skipped for what reason.

Using your gml
--------------
The IMAER gml you created can be imported by the IMAER Calculator (https://calculator.aerius.nl/calculator/) when containing less then 100 Emission Sources. 

If your gml contains more than 100 Emission sources you'll have to use the IMAER Connect calculation service. This service is accessible via an API documented at https://www.aerius.nl/nl/factsheets/api-voor-aerius-calculator/ .
