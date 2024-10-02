* [Index](index.md)
* [Generate Calculator Input](01_generate_calc_input.md)
* [Import Calculator Results](04_import_calc_results.md)
* [Relate Calculator results](05_relate_calc_results.md)
* [Connect - Receptor Sets](07_connect_receptor_sets.md)
* [Connect - Jobs](08_connect_jobs.md)
* [Configuration](09_configuration.md)

<img src="img/icons/icon_relate_calc_results.svg" alt="button" width="96"/>

# Relate Calculator results

Relate IMAER layers to one another by calculating the difference, sum or maximum values
of the receptor's deposition values.

## Howto

You will need at least 2 IMAER layers, loaded with the Import IMAER GML tool.

1. Click the Relate calculation results button to open the dialog.
2. Choose the `calculation type` (difference, sum or maximum).
3. By default, the name for the new layer will be the name of the calculation type.
You can choose a more specific name in the `layer name` input widget.
4. Choose the layers to perform the calculation on. (In case of calculating the difference, is will be layer1 minus layer2)

![dialog](img/relate_calc_results_dlg.png)

A new memory layer will be created, holding all receptors from the input layers. In case a receptor only exists in one of the layers, the calculation will use the value 0 for the missing receptor.

![dialog](img/relate_calc_results_map.png)

The generated memory layer will have a predefined, 2 color style showing positive or negative values. This style can of course be changed with standard QGIS functionality.

![dialog](img/relate_calc_results_legend.png)

Output layers will have the same deposition fields as the IMAER layers so they can be used with this relate function as well. For example for summarizing more than 2 layers.

## Processing

The relate functions are also available as algorithms in the processing toolbox. These can be used
in a more generic way, for example combined with other algorithms in a model. And it's possible to
call them from a Python script.

![dialog](img/relate_calc_results_processing.png)

## Remarks

* The `difference` operation works on 2 layers, but the `sum` and `maximum` can work
on up to 5 layers.
