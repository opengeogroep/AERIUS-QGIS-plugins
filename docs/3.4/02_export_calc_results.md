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

<img src="img/icons/icon_export_calc_result.svg" alt="button" width="96"/>

# Export edited AERIUS Calculator results

After editing the imported AERIUS Calculator results, the plugin can export the data back to IMAER GML format.

## Howto

Select the layer with the (edited) Calculator results to enable the export button in the IMAER toolbar. Clicking the button will save a new GML file in the same directory as the source GML file used for the import. The filename will be `<old_file_name>_modified.gml`.

Currently there is no support for changing the file name. A second export operation will
overwrite the existing file.
