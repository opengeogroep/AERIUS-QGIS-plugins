from qgis.core import QgsFieldProxyModel

emission_sectors = {
    'Energie': {},
    'Landbouw': {
        'subsectors': {
            'Stalemissies': {},
            'Mestopslag': {},
            'Beweiding': {},
            'Mestaanwending': {},
            'Glastuinbouw': {},
            'Vuurhaarden Overig': {}
        }
    },
    'Wonen en Werken': {
        'subsectors': {
            'Woningen': {},
            'Recreatie': {},
            'Werken en winkels': {}
        }
    },
    'Industrie': {},
    'Mobiele Werktuigen': {},
    'Railverkeer': {},
    'Luchtverkeer': {},
    'Wegverkeer': {},
    'Scheepvaart': {},
    'Plan': {},
    'Anders': {}
}

flt_str = QgsFieldProxyModel.String
flt_num = QgsFieldProxyModel.Numeric
flt_int = QgsFieldProxyModel.Int

emission_elements = {
    'emission_nh3': {'types': [flt_num], 'name': 'Emissie NH3', 'group': 'emission'},
    'emission_nox': {'types': [flt_num], 'name': 'Emissie NOx', 'group': 'emission'},
    'loc_name': {'types': [flt_str], 'name': 'Location Name', 'group': 'general'}
}
