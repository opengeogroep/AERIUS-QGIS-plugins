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

Convert your emission source data into an IMAER GML file which can be used as AERIUS Calculator input.

## Howto

Open your emission data as a regular vector layer in QGIS. The geometries can be points,
lines or polygons.

![dialog](img/generate_aerius_calculator_input_dlg_2.png)

1. Click the Generate input GML button to open the dialog for generating Calculator input GML.
2. Choose the layer with your input data and coordinate reference system (CRS).
3. Choose the sector for your data. Currently only 2 sectors are available, `ROAD_TRANSPORTATION` and `OTHER` (for generic emission sources).
4. In both the Metadata and Sector tabs, choose the fields from your layer for every variable you want to store in the GML file.
5. Choose a file name for your GML file. The dialog will suggest a name including the current date and time (like `calcinput_20200907_193245.gml`)

After pressing Save, the GML file will be generated. A link to the file will be displayed in the message bar on top of your map. If anything goes wrong, an error will be displayed there.

## Saving and loading settings

Because picking all the fields is a lot of work, there's a way to store the current
field settings in a file. This is done with the `Save settings` and `Load settings` buttons
at the bottom of the dialog.
Loading the settings will set the field names.
* In case the current input layer does not contain that field name, the entry will be cleared.
* Empty values are stored as well.
* The settings are stored in the work directory in a file called `generate_gml_config.json`
which will be overwritten on every save operation.

![roads tab](img/generate_aerius_calculator_input_dlg_3.png)

## Using the exported GML file

There are several ways of using the generated GML.

1. Use the **plugin's Connect** functionality. This can validate the GML content, start a calculation and retreive the results.
2. The generated GML file can be imported using the interface at [Aerius Calculator (NL)](https://calculator.aerius.nl/) for starting the calculation. It is possible
to import multiple files before starting the calculation, which you can use when having
multiple maplayers with emission data (and different geometry types).
3. Use the **AERIUS Connect API** using the [Swagger](https://connect.aerius.nl/) interface or
create your own software to connect to it.

## Remarks

* The current version of the generated GML file is `IMAER 5.1`
* IMAER does not support multi geometry types (like MultiLineString) and will try to
convert your data in case it has a multi type, as single geometry data is often stored as multi geometry in GIS.
* Your attribute data must contain the exact values that should end up in the GML file. The plugin
does not attempt to convert values in some smart way.
