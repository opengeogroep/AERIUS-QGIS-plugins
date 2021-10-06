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

<img src="img/icons/icon_import_calc_result.svg" alt="button" width="96"/>

# Import AERIUS Calculator results

Import AERIUS Calculator result files and add them as QGIS vector layers.

## Howto

Click the import button in the IMAER toolbar and browse to the downloaded IMAER GML file from Aerius Calculator. (Make sure you downloaded the "GML with calculation results".)

![dialog](img/import_result_file_dlg.png)

The data will be converted into a GeoPackage (.gpkg) file at the same location your GML file is placed. Make sure you have write access to that directory.

After conversion, the calculation result hexagons will be opened as a normal polygon vector layer in QGIS. The attribute table contains the deposition values.

![deposition map and attribute table](img/import_result_map_and_table.png)

You can use all standard QGIS functionality for viewing, analysing and editing the data.
