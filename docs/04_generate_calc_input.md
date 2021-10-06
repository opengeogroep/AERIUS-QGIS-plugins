* [Index](index.md)
* [Import Calculator Results](01_import_calc_results.md)
* [Export Calculator Results](02_export_calc_results.md)
* [Extract GML from AERIUS PDF](03_extract_gml_from_pdf.md)
* [Generate Calculator Input](04_generate_calc_input.md)
* [Relate Calculator results](05_relate_calc_results.md)
* [Add Open data Layer](06_open_data_layers.md)
* [Connect - Receptor Sets](07_connect_receptor_sets.md)
* [Connect - Jobs](08_connect_jobs.md)
* [Configuration](09_configuration.md)

<img src="img/icons/icon_generate_calc_input.svg" alt="button" width="96"/>

# Generate Calculator Input

## Introduction

Convert your emission source data into an IMAER GML file which can be used as AERIUS Calculator input.

## Howto

Open your emission data as a regular vector layer in QGIS. The geometries can be points, linestrings or polygons. Be aware that multi geometries are not (yet) supported.

![dialog](img/generate_aerius_calculator_input_dlg.png)

1. Click the Generate input GML button to open the dialog for generating Calculator input GML.
2. Choose the layer with your input data, the year and coordinate reference system (CRS).
3. Choose the sector (and sub sector) for your data. (Currently only 3 sectors are available, and only `OTHER` should really work.)
4. Choose the fields from your layer for every variable you want to store in the GML file.
5. Choose a file name for your GML file. The dialog will suggest a name including the current date and time (like `calcinput_20200907_193245.gml`)

After pressing `save`, the GML will be generated. A link to the file will be displayed in the message bar on top of your map. If anything goes wrong, an error will be displayed there.

## Using the exported GML file

The generated GML file can be imported using the interface at [Aerius Calculator (NL)](https://calculator.aerius.nl/) for starting the calculation. It is possible to import multiple files before starting the calculation, which you can use when having multiple maplayers with emission data (and different geometry types).

**The current version of the generated GML file is `IMAER 3.1`!!**
