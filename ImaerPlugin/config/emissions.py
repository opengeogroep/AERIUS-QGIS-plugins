from qgis.core import QgsFieldProxyModel

emission_sectors = {
    'ROAD_TRANSPORTATION': {
        'subsectors': {
            'Freeways': {'sector_id': 3111},
            'Non-urban roads': {'sector_id': 3112},
            'Urban roads': {'sector_id': 3113}
        }
    },
    'OTHER': {'sector_id': 9999},
}


ui_settings = {
    'project_years': [
        '2020', '2021', '2022', '2023', '2024',
        '2025', '2026', '2027', '2028', '2029',
        '2030', '2031', '2032', '2033', '2034',
        '2035', '2036', '2037', '2038', '2039',
        '2040'],
    'project_default_year': '2023',
    'situation_name': 'Situation 1',
    'situation_types': ['REFERENCE', 'PROPOSED', 'TEMPORARY'], #'NETTING'],
    'countries': ['NL', 'UK'],
    'imaer_versions': ['4.0', '5.0'],
    'crs': [
        {'name': 'Amersfoort / RD New - Netherlands', 'srid': 28992},
        {'name': 'OSGB 1936 / British National Grid', 'srid': 27700}
    ],
}
