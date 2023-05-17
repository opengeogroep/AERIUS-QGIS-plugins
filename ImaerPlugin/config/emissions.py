from qgis.core import QgsFieldProxyModel

emission_sectors = {
    'roads': {
        'emission_tab': 'tab_roads',
        'tab_name': 'Roads',
        'ui_settings': {
            'default': {
                'disable_widgets': [],
                'vehicle_page': None
            },
            'NL': {
                'disable_widgets': [
                    'label_rd_width', 'fcb_rd_width',
                    'label_rd_gradient', 'fcb_rd_gradient',
                    'label_rd_coverage', 'fcb_rd_coverage',
                    'label_rd_b_left_height_av', 'fcb_rd_b_left_height_av',
                    'label_rd_b_left_height_max', 'fcb_rd_b_left_height_max',
                    'label_rd_b_left_height_min', 'fcb_rd_b_left_height_min',
                    'label_rd_b_left_porosity', 'fcb_rd_b_left_porosity',
                    'label_rd_b_right_height_av', 'fcb_rd_b_right_height_av',
                    'label_rd_b_right_height_max', 'fcb_rd_b_right_height_max',
                    'label_rd_b_right_height_min', 'fcb_rd_b_right_height_min',
                    'label_rd_b_right_porosity', 'fcb_rd_b_right_porosity',
                ],
                'vehicle_page': 'page_veh_srm2'
            },
            'UK': {
                'disable_widgets': [
                    'label_rd_b_left_height', 'fcb_rd_b_left_height',
                ],
                'vehicle_page': 'page_veh_adms'
            }
        }
    },
    'other': {
        'emission_tab': 'tab_emission_sources',
        'tab_name': 'Other',
        'sector_id': 9999
    },
}

ui_settings = {
    'project_years': [
        2020, 2021, 2022, 2023, 2024,
        2025, 2026, 2027, 2028, 2029,
        2030, 2031, 2032, 2033, 2034,
        2035, 2036, 2037, 2038, 2039,
        2040],
    'project_default_year': 2023,
    'situation_name': 'Situation 1',
    'situation_types_connect': ['DEFINED_BY_FILE', 'REFERENCE', 'PROPOSED', 'TEMPORARY'],
    'situation_types_gml': ['REFERENCE', 'PROPOSED', 'TEMPORARY', 'NETTING'],
    'countries': ['NL', 'UK'],
    'imaer_versions': ['5.1'],
    'crs': [
        {'name': 'Amersfoort / RD New - Netherlands', 'srid': 28992},
        {'name': 'OSGB 1936 / British National Grid', 'srid': 27700}
    ],
}
