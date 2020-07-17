from qgis.core import QgsFieldProxyModel

emission_sectors = {
    'ENERGY': {},
    'AGRICULTURE': {
        'subsectors': {
            'Stalemissies': {},
            'Mestopslag': {},
            'Beweiding': {},
            'Mestaanwending': {},
            'Glastuinbouw': {},
            'Vuurhaarden Overig': {}
        }
    },
    'LIVE_AND_WORK': {
        'subsectors': {
            'Woningen': {},
            'Recreatie': {},
            'Werken en winkels': {}
        }
    },
    'INDUSTRY': {
        'subsectors': {
            'Afvalverwerking': {},
            'Voedings- en genotmiddelen': {},
            'Chemische industrie': {},
            'Bouwmaterialen': {},
            'Basismetaal': {},
            'Metaalbewerkingsindustrie': {},
            'Overig': {}
        }
    },
    'MOBILE_EQUIPMENT': {
        'subsectors': {
            'Landbouw': {},
            'Bouw- en industrie': {},
            'Delfstoffenwinning': {},
            'Consumenten mobiele werktuigen': {}
        }
    },
    'RAIL_TRANSPORTATION': {
        'subsectors': {
            'Emplacement': {},
            'Spoorweg': {}
        }
    },
    'AVIATION': {
        'subsectors': {
            'Stijgen': {},
            'Landen': {},
            'Taxien': {},
            'Bronnen luchthaventerrein': {}
        }
    },
    'ROAD_TRANSPORTATION': {
        'subsectors': {
            'Snelwegen': {},
            'Buitenwegen': {},
            'Binnen bebouwde kom': {}
        }
    },
    'SHIPPING': {
        'subsectors': {
            'Zeescheepvaart Aanlegplaats': {},
            'Zeescheepvaart Binnengaats route': {},
            'Zeescheepvaart Zeeroute': {},
            'Binnenvaart Aanlegplaats': {},
            'Binnenvaart Vaarroute': {}
        }
    },
    'PLAN': {},
    'OTHER': {}
}

flt_str = QgsFieldProxyModel.String
flt_num = QgsFieldProxyModel.Numeric
#flt_int = QgsFieldProxyModel.Int
#flt_longlong = QgsFieldProxyModel.LongLong

emission_elements = {
    'emission_nh3': {'types': [flt_num], 'label': 'Emissie NH3', 'group': 'emission'},
    'emission_nox': {'types': [flt_num], 'label': 'Emissie NOx', 'group': 'emission'},
    'loc_name': {'types': [flt_str], 'label': 'Location Name', 'group': 'general'},
}
