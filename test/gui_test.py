import os

demo_data_dir = '/home/raymond/git/AERIUS-QGIS-plugins/demodata/'
old_work_dir = '/home/raymond/imaer_plugin'

work_dir = os.path.join(QDir.tempPath(), 'imaer_plugin_gui_test')
if not os.path.exists(work_dir):
        os.makedirs(work_dir)

plugin = qgis.utils.plugins['ImaerPlugin']

# Settings
def set_configuration(country=None, crs=None, work_dir=None):
    if country is not None:
        plugin.configuration_dlg.combo_country.setCurrentText(country)
    if crs is not None:
        crs_dict = {28992: 1, 27700: 2}
        plugin.configuration_dlg.combo_crs.setCurrentIndex(crs_dict[crs])
    if work_dir is not None:
        plugin.configuration_dlg.edit_work_dir.setText(work_dir)
    
    plugin.configuration_dlg.save_ui_to_settings()
    plugin.aerius_connection.check_connection()
    plugin.update_connect_widgets()
    plugin.update_crs_widgets()

set_configuration(country='NL', crs=28992, work_dir=work_dir)
#plugin.configuration_dlg.show()
set_configuration(country='UK', crs=27700)

# Generate GML

# uk roads
fn = os.path.join(demo_data_dir, 'test_input_uk.gpkg')
ln = 'Traffic_shapefile_UK_27700'
layer = QgsVectorLayer(f'{fn}|layername={ln}', 'test_input_traffic')
QgsProject.instance().addMapLayer(layer)
plugin.generate_calc_input_dlg.combo_layer_rd.setLayer(layer)

cfg_fn = os.path.join(demo_data_dir, 'generate_gml_config_uk_roads.json')
plugin.generate_calc_input_dlg.load_settings(cfg_fn)

gml_fn = os.path.join(work_dir, 'test_uk_roads.gml')
plugin.generate_calc_input_dlg.edit_outfile.setText(gml_fn)
plugin.generate_calc_input_dlg.generate_imaer_gml()



set_configuration(work_dir=old_work_dir)
