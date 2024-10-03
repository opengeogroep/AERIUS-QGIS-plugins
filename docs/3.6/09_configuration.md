* [Index](index.md)
* [Generate Calculator Input](01_generate_calc_input.md)
* [Import Calculator Results](04_import_calc_results.md)
* [Relate Calculator results](05_relate_calc_results.md)
* [Connect - Receptor Sets](07_connect_receptor_sets.md)
* [Connect - Jobs](08_connect_jobs.md)
* [Configuration](09_configuration.md)

<img src="img/icons/icon_configuration.svg" alt="button" width="96"/>

# Configuration

Some plugin configurations can be set in the Configuration dialog. Most of them are related to Connect.

![dialog](img/configuration_dlg.png)

## General

### Country:
The country where you are using AERIUS. Different countries use different versions
and sub sets of IMAER which will reflect in the user interface.

### CRS:
Coordinate reference system your IMAER data should use.

### Work directory:
This is the default local directory on your system where the plugin will download
and save files to. Make sure you have write access to this directory.

## Connect

These settings are only needed if you want to use the plugin for AERIUS Connect
functionality (currently only available in NL). When the country is set to UK, the
Connect settings are disabled.

### Server base URL:
Location of the Connect API URL.
(Since version 3.6 of the plugin, this value is hardcoded
and not editable anymore. It is only shown in the configuration dialog for convenience.)

### Version:

Connect server version.
(Since version 3.6 of the plugin, this value is hardcoded
and not editable anymore. It is only shown in the configuration dialog for convenience.)

### Email:

The email address you want to use for Connect. This is also your account name, and
the address that will receive notifications when your calculations are completed.

### API Key:

Connect API key that you will receive by e-mail after requesting it. You can click
the `Request new API key` button to get (a new) one.

After receiving the new API key in your mailbox, simply copy the 32 character key
to the configuration screen.

## Save

Save the settings. When the country is set to NL, the plugin will attempt to make a connection by firing a few rquests. That will also update the content of the Connect buttons and dialogs.

## Hint

In case you are running into connection problems, open the Debug/Developer panel in QGIS
(F12) to inspect the internet traffic between QGIS and Connect.
