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
                    'label_rd_area_type', 'fcb_rd_area_type',
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
                    'groupBox_rd_tvp_adms',
                ],
                'vehicle_page': 'page_veh_srm2'
            },
            'UK': {
                'disable_widgets': [
                    'label_rd_tunnel_factor', 'fcb_rd_tunnel_factor',
                    'label_rd_elevation_height', 'fcb_rd_elevation_height',
                    'label_rd_b_left_height', 'fcb_rd_b_left_height',
                    'label_rd_b_right_height', 'fcb_rd_b_right_height',
                    'groupBox_rd_tvp',
                ],
                'vehicle_page': 'page_veh_adms'
            }
        }
    },
    'other': {
        'emission_tab': 'tab_emission_sources',
        'tab_name': 'Generic Sources',
        'sector_id': 9999,
        'ui_settings': {
            'default': {
                'disable_widgets': [],
            },
            'NL': {
                'disable_widgets': [
                    'label_es_adms_height', 'fcb_es_adms_height',
                    'label_es_adms_heat_capacity', 'fcb_es_adms_heat_capacity',
                    'label_es_adms_source_type', 'fcb_es_adms_source_type',
                    'label_es_adms_diameter', 'fcb_es_adms_diameter',
                    'label_es_adms_elevation_angle', 'fcb_es_adms_elevation_angle',
                    'label_es_adms_horizontal_angle', 'fcb_es_adms_horizontal_angle',
                    'label_es_adms_width', 'fcb_es_adms_width',
                    'label_es_adms_vertical_dimension', 'fcb_es_adms_vertical_dimension',
                    'label_es_adms_buoyancy_type', 'fcb_es_adms_buoyancy_type',
                    'label_es_adms_density', 'fcb_es_adms_density',
                    'label_es_adms_temperature', 'fcb_es_adms_temperature',
                    'label_es_adms_efflux_type', 'fcb_es_adms_efflux_type',
                    'label_es_adms_vertical_velocity', 'fcb_es_adms_vertical_velocity',
                    'label_es_adms_volumetric_flow_rate', 'fcb_es_adms_volumetric_flow_rate',
                    'groupBox_es_tvp_adms',
                ]
            },
            'UK': {
                'disable_widgets': [
                    'label_es_emission_height', 'fcb_es_emission_height',
                    'label_es_spread', 'fcb_es_spread',
                    'groupBox_heatContent',
                    'groupBox_es_tvp',
                ],
            }
        }
    },
    'buildings': {
        'emission_tab': 'tab_buildings',
        'tab_name': 'Buildings',
        'sector_id': 9998
    },
    'calc_points': {
        'emission_tab': 'tab_calc_points',
        'tab_name': 'Calculation Points',
        'sector_id': 9997
    },
    'time_varying_profiles': {
        'emission_tab': 'tab_time_varying_profiles',
        'tab_name': 'Time Varying Profiles',
        'sector_id': 9996
    }
}

ui_settings = {
    'project_years': [
        2018, 2019,
        2020, 2021, 2022, 2023, 2024,
        2025, 2026, 2027, 2028, 2029,
        2030, 2031, 2032, 2033, 2034,
        2035, 2036, 2037, 2038, 2039,
        2040],
    'project_default_year': 2024,
    'situation_name': {'NL': 'Situation 1', 'UK': 'Scenario 1'},
    'situation_types_gml': {
        'NL': ['OFF_SITE_REDUCTION', 'PROPOSED', 'REFERENCE', 'TEMPORARY'],
        'UK': ['COMBINATION_PROPOSED', 'COMBINATION_REFERENCE', 'OFF_SITE_REDUCTION', 'PROPOSED', 'REFERENCE', 'TEMPORARY'],
    },
    'situation_types_connect': ['DEFINED_BY_FILE', 'REFERENCE', 'PROPOSED', 'TEMPORARY'],
    'countries': ['NL', 'UK'],
    'connect_countries': ['NL'],
    'supported_imaer_versions': ['6.0'],
    'crs': [
        {'name': 'Amersfoort / RD New - Netherlands', 'srid': 28992},
        {'name': 'OSGB 1936 / British National Grid', 'srid': 27700}
    ],
    'units_veh_movements': ['p/hour', 'p/24 hour', 'p/month', 'p/year'],
    'time_varying_profile_types': ['THREE_DAY', 'MONTHLY']
}
