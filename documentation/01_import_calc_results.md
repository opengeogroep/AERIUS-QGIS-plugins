* [Index](00_index.md)
* [Import Calculator Results](01_import_calc_results.md)
* [Export Calculator Results](02_export_calc_results.md)
* [Generate Calculator Input](03_generate_calc_input.md)

# Import AERIUS Calculator results

## Introduction

Import AERIUS Calculator result files.

## Howto

Click the ![alt text](../ImaerPlugin/icon_import_calc_result.png "import buton") button in the IMAER toolbar and browse to the downloaded IMAER GML file from Aerius Calculator. (Make sure you download the "GML with calculation results".)

The data will be converted into a GeoPackage (.gpkg) file at the same location your GML file is placed. Make sure you have write access to that directory.

After conversion, the calculation result hexagons will be opened as a normal polygon vector layer in QGIS. The attribute table contains the deposition values.

You can use all standard QGIS functionality for viewing, analysing and editing the data.
