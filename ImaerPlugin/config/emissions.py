from qgis.core import QgsFieldProxyModel

emission_sectors = {
    'ENERGY': {'code': 2100},
    'AGRICULTURE': {
        'subsectors': {
            'Stalemissies': {'code': 4110},
            'Mestopslag': {'code': 4120},
            'Beweiding': {'code': 4130},
            'Mestaanwending': {'code': 4140},
            'Glastuinbouw': {'code': 4320},
            'Vuurhaarden Overig': {'code': 4600}
        }
    },
    'LIVE_AND_WORK': {
        'subsectors': {
            'Woningen': {'code': 8200},
            'Recreatie': {'code': 8210},
            'Werken en winkels': {'code': 8640}
        }
    },
    'INDUSTRY': {
        'subsectors': {
            'Afvalverwerking': {'code': 1050},
            'Voedings- en genotmiddelen': {'code': 1100},
            'Chemische industrie': {'code': 1300},
            'Bouwmaterialen': {'code': 1400},
            'Basismetaal': {'code': 1500},
            'Metaalbewerkingsindustrie': {'code': 1700},
            'Overig': {'code': 1800}
        }
    },
    'MOBILE_EQUIPMENT': {
        'subsectors': {
            'Landbouw': {'code': 3210},
            'Bouw- en industrie': {'code': 3220},
            'Delfstoffenwinning': {'code': 3230},
            'Consumenten mobiele werktuigen': {'code': 3530}
        }
    },
    'RAIL_TRANSPORTATION': {
        'subsectors': {
            'Emplacement': {'code': 3710},
            'Spoorweg': {'code': 3720}
        }
    },
    'AVIATION': {
        'subsectors': {
            'Stijgen': {'code': 3610},
            'Landen': {'code': 3620},
            'Taxien': {'code': 3630},
            'Bronnen luchthaventerrein': {'code': 3640}
        }
    },
    'ROAD_TRANSPORTATION': {
        'subsectors': {
            'Snelwegen': {'code': 3111},
            'Buitenwegen': {'code': 3112},
            'Binnen bebouwde kom': {'code': 3113}
        }
    },
    'SHIPPING': {
        'subsectors': {
            'Zeescheepvaart Aanlegplaats': {'code': 7510},
            'Zeescheepvaart Binnengaats route': {'code': 7520},
            'Zeescheepvaart Zeeroute': {'code': 7530},
            'Binnenvaart Aanlegplaats': {'code': 7610},
            'Binnenvaart Vaarroute': {'code': 7620}
        }
    },
    'PLAN': {'code': 9000},
    'OTHER': {'code': 9999}
}

flt_str = QgsFieldProxyModel.String
flt_num = QgsFieldProxyModel.Numeric
#flt_int = QgsFieldProxyModel.Int
#flt_longlong = QgsFieldProxyModel.LongLong

emission_elements = {
    'loc_name': {'types': [flt_str], 'label': 'Location Name', 'group': 'general'},
    'emission_nh3': {'types': [flt_num], 'label': 'Emissie NH3', 'group': 'emission'},
    'emission_nox': {'types': [flt_num], 'label': 'Emissie NOx', 'group': 'emission'},
}
