from qgis.core import QgsFieldProxyModel

'''
emission_sectors = {
    'ENERGY': {'sector_id': 2100},
    'AGRICULTURE': {
        'subsectors': {
            'Stalemissies': {'sector_id': 4110},
            'Mestopslag': {'sector_id': 4120},
            'Beweiding': {'sector_id': 4130},
            'Mestaanwending': {'sector_id': 4140},
            'Glastuinbouw': {'sector_id': 4320},
            'Vuurhaarden Overig': {'sector_id': 4600}
        }
    },
    'LIVE_AND_WORK': {
        'subsectors': {
            'Woningen': {'sector_id': 8200},
            'Recreatie': {'sector_id': 8210},
            'Werken en winkels': {'sector_id': 8640}
        }
    },
    'INDUSTRY': {
        'subsectors': {
            'Afvalverwerking': {'sector_id': 1050},
            'Voedings- en genotmiddelen': {'sector_id': 1100},
            'Chemische industrie': {'sector_id': 1300},
            'Bouwmaterialen': {'sector_id': 1400},
            'Basismetaal': {'sector_id': 1500},
            'Metaalbewerkingsindustrie': {'sector_id': 1700},
            'Overig': {'sector_id': 1800}
        }
    },
    'MOBILE_EQUIPMENT': {
        'subsectors': {
            'Landbouw': {'sector_id': 3210},
            'Bouw- en industrie': {'sector_id': 3220},
            'Delfstoffenwinning': {'sector_id': 3230},
            'Consumenten mobiele werktuigen': {'sector_id': 3530}
        }
    },
    'RAIL_TRANSPORTATION': {
        'subsectors': {
            'Emplacement': {'sector_id': 3710},
            'Spoorweg': {'sector_id': 3720}
        }
    },
    'AVIATION': {
        'subsectors': {
            'Stijgen': {'sector_id': 3610},
            'Landen': {'sector_id': 3620},
            'Taxien': {'sector_id': 3630},
            'Bronnen luchthaventerrein': {'sector_id': 3640}
        }
    },
    'ROAD_TRANSPORTATION': {
        'subsectors': {
            'Snelwegen': {'sector_id': 3111},
            'Buitenwegen': {'sector_id': 3112},
            'Binnen bebouwde kom': {'sector_id': 3113}
        }
    },
    'SHIPPING': {
        'subsectors': {
            'Zeescheepvaart Aanlegplaats': {'sector_id': 7510},
            'Zeescheepvaart Binnengaats route': {'sector_id': 7520},
            'Zeescheepvaart Zeeroute': {'sector_id': 7530},
            'Binnenvaart Aanlegplaats': {'sector_id': 7610},
            'Binnenvaart Vaarroute': {'sector_id': 7620}
        }
    },
    'PLAN': {'sector_id': 9000},
    'OTHER': {'sector_id': 9999}
}
'''

emission_sectors = {
    'OTHER': {'sector_id': 9999}
}


flt_str = QgsFieldProxyModel.String
flt_num = QgsFieldProxyModel.Numeric
#flt_int = QgsFieldProxyModel.Int
#flt_longlong = QgsFieldProxyModel.LongLong

emission_elements = {
    'loc_name': {'types': [flt_str], 'label': 'Location Name', 'group': 'general', 'sector_ids': [-1]},
    'emission_nh3': {'types': [flt_num], 'label': 'Emissie NH3', 'group': 'emission', 'sector_ids': [-1]},
    'emission_nox': {'types': [flt_num], 'label': 'Emissie NOx', 'group': 'emission', 'sector_ids': [-1]},
    'esc_height': {'types': [flt_num], 'label': 'Emission height', 'group': 'emission', 'sector_ids': [9000, 9999]},
    'esc_heat_content': {'types': [flt_num], 'label': 'Heat content', 'group': 'esc', 'sector_ids': [9000, 9999]},
    'esc_em_temp': {'types': [flt_num], 'label': 'Emission Temperature', 'group': 'esc', 'sector_ids': [9000, 9999]},
    'esc_of_diam': {'types': [flt_num], 'label': 'Emission Outflow Diameter', 'group': 'esc', 'sector_ids': [9000, 9999]},
    'esc_of_vel': {'types': [flt_num], 'label': 'Emission Outflow Velocity', 'group': 'esc', 'sector_ids': [9000, 9999]},
    'esc_of_dir': {'types': [flt_str], 'label': 'Emission Outflow Direction', 'group': 'esc', 'sector_ids': [9000, 9999]},
    'esc_diurnal_var': {'types': [flt_str], 'label': 'Diurnal variation', 'group': 'esc', 'sector_ids': [9999]},
    'esc_bld_height': {'types': [flt_num], 'label': 'Building Height', 'group': 'esc_bld', 'sector_ids': [9999]},
    'esc_bld_width': {'types': [flt_num], 'label': 'Building Width', 'group': 'esc_bld', 'sector_ids': [9999]},
    'esc_bld_length': {'types': [flt_num], 'label': 'Building Length', 'group': 'esc_bld', 'sector_ids': [9999]},
    'esc_bld_orientation': {'types': [flt_num], 'label': 'Building Orientation', 'group': 'esc_bld', 'sector_ids': [9999]},
}

ui_settings = {
    'years': ['2019', '2020', '2021'],
    'situation_name': 'Situation 1',
    'crs': [
        {'name': 'Amersfoort / RD New - Netherlands', 'srid': 28992},
        {'name': 'OSGB 1936 / British National Grid', 'srid': 27700},
        ],
}
