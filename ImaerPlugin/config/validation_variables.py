# This file contains description of tooltips and allowed values/types for
# Aerius make gml (roads)

# this dictionary contains field description:
#       [tooltip, datatype, allowed_options]
# the name of the field from qgis ui to be updated when ui is complete

tooltip_validation_label_dict = {
                'road_width_uk':
                    ['Width of the road (m)',
                     ['int', 'float'],
                     [range(2, 1000)]],
                'road_elev_uk':
                    ['Height of the road (m)',
                     ['int', 'float'],
                     [range(0, 15000)]],
                'gradient_uk':
                    ['Gradient of the road (%)',
                     ['int', 'float'],
                     [range(-50,50)]],
                'barrier_l_type_uk':
                    ['Type of barrier on left-hand-side of road',
                     ['str'],
                     ['None',
                      'NOISE_BARRIER',
                      'BRICK_WALL',
                      'STREET_CANYON_TERRACED_HOUSES',
                      'STREET_CANYON_SEMIDETACHED_HOUSES',
                      'STREET_CANYON_DETACHED_HOUSES',
                      'TREE_BARRIER_OPEN',
                      'TREE_BARRIER_DENSE',
                      'OTHER']],
                'barrier_l_width_uk':
                    ['Width of barrier on left-hand-side of road (m)',
                     ['int', 'float'],
                     ['>0', '>road_width_uk/2']],
                'barrier_l_maxheight_uk':
                    ['Maximum height of barrier on left-hand-side of road (m)',
                     ['int', 'float'],
                     ['>=0',
                      '>barrier_l_avheight_uk',
                      '>barrier_l_minheight_uk']],
                'barrier_l_avheight_uk':
                    ['Average height of barrier on left-hand-side of road (m)',
                     ['int', 'float'],
                     ['>=0',
                      '<barrier_l_maxheight_uk',
                      '>barrier_l_minheight_uk']],
                'barrier_l_minheight_uk':
                    ['Minimum height of barrier on left-hand-side of road (m)',
                     ['int', 'float'],
                     ['>=0',
                      '<barrier_l_avheight_uk',
                      '<barrier_l_maxheight_uk']],
                'barrier_l_por_uk':
                    ['Porosity of barrier on left-hand-side of road (%)',
                     ['int', 'float'],
                     [range(0, 100)]],
                'barrier_r_type_uk':
                    ['Type of barrier on right-hand-side of road',
                     ['str'],
                     ['None',
                      'NOISE_BARRIER',
                      'BRICK_WALL',
                      'STREET_CANYON_TERRACED_HOUSES',
                      'STREET_CANYON_SEMIDETACHED_HOUSES',
                      'STREET_CANYON_DETACHED_HOUSES',
                      'TREE_BARRIER_OPEN',
                      'TREE_BARRIER_DENSE',
                      'OTHER']],
                'barrier_r_width_uk':
                    ['Width of barrier on right-hand-side of road (m)'
                     ['int', 'float'],
                     ['>0', '>road_width_uk/2']],
                'barrier_r_maxheight_uk':
                    ['Maximum height of barrier on right-hand-side of road (m)'
                     ['int', 'float'],
                     ['>=0',
                      '>barrier_r_minheight_uk',
                      '>barrier_r_avheight_uk']],
                'barrier_r_avheight_uk':
                    ['Average height of barrier on right-hand-side of road (m)',
                     ['int', 'float'],
                     ['>=0',
                      '>barrier_r_minheight_uk',
                      '<barrier_r_maxheight_uk']],
                'barrier_r_minheight_uk':
                    ['Minimum height of barrier on right-hand-side of road (m)',
                     ['int', 'float'],
                     ['>=0',
                      '<barrier_r_avheight_uk',
                      '<barrier_r_maxheight_uk']],
                'barrier_r_por_uk':
                    ['Porosity of barrier on left-right-side of road (%)',
                     ['int', 'float'],
                     [range(0, 100)]],
                'barrier_coverage_uk':
                    ['Coverage of barrer (%)',
                     ['int', 'float'],
                     [range(0, 100)]],
                'diurnal_uk':
                    ['Diurnal profile to be used for road',
                     ['str'],
                     ['CONTINUOUS',
                      'DEFAULT',
                      '72 comma-separated values (24 weekday, 24 Sat, 24 Sun)']],
                'area_uk':
                    ['Area of UK being modelled',
                     ['str'],
                     ['Sco', 'Eng', 'Nor', 'Wal']],
                'road_type_uk':
                    ['Type of road being modelled',
                     ['str'],
                     ['Urb', 'Rur', 'Mot', 'Lon1', 'Lon2', 'Lon3', 'Lon4']],
                'direction_uk':
                    ['Is the road one or two directions',
                     ['str'],
                     ['BOTH', 'A_TO_B', 'B_TO_A']],
                'eft_spd_uk':
                    ['Average speed on road link (kph)',
                     ['int', 'float'],
                     ['>0']],
                'eft_veh_movements_uk':
                    ['Averaging time of vehicle count provided',
                     ['str'],
                     ['DAY', 'HOUR', 'MONTH', 'YEAR']],
                'eft_car_uk':
                    ['Number of cars',
                     ['int', 'float'],
                     ['>=0']],
                'eft_taxi_uk':
                    ['Number of taxis',
                     ['int', 'float'],
                     ['>=0']],
                'eft_mc_uk':
                    ['Number of motorcycles',
                     ['int', 'float'],
                     ['>=0']],
                'eft_lgv_uk':
                    ['Number of Light Goods Vehicles (LGV)',
                     ['int', 'float'],
                     ['>=0']],
                'eft_hgv_uk':
                    ['Number of Heavy Goods Vehicles (HGV)',
                     ['int', 'float'],
                     ['>=0']],
                'eft_bus_uk':
                    ['Number of buses',
                     ['int', 'float'],
                     ['>=0']],
                'custom_desc_uk':
                    ['Description of custom calculation',
                     ['str'],
                     []],
                'custom_veh_movements_uk':
                    ['Number of vehicles on road',
                     ['int', 'float'],
                     ['>0']],
                'custom_veh_movements_time_uk':
                    ['Averaging time of vehicle count provided',
                     ['str'],
                     ['DAY', 'HOUR', 'MONTH', 'YEAR']],
                'custom_nox_ems_uk':
                    ['NOx emissions on road (g/km/s)',
                     ['int', 'float'],
                     ['>=0']],
                'custom_nh3_ems_uk':
                    ['NH3 emissions on road (g/km/s)',
                     ['int', 'float'],
                     ['>=0']],
                'tunnel_factor_nl':
                    ['Apply tunnel factor',
                     ['int', 'float'],
                     ['>0']],
                'elevation_type_nl':
                    ['Type of elevation to model',
                     ['str'],
                     ['NORMAL',
                      'NORMAL_DYKE',
                      'STEEP_DYKE',
                      'VIADUCT',
                      'TUNNEL']],
                'elevation_nl':
                    ['Height of road (m)',
                     ['int', 'float'],
                     [range(-6, 12)]],
                'barrier_l_type_nl':
                    ['Barrier type on left-hand-side of road',
                     ['str'],
                     ['None', 'SCREEN', 'WALL']],
                'barrier_l_height_nl':
                    ['Height of barrer on left-hand-side (m)',
                     ['int', 'float'],
                     ['>0']],
                'barrier_l_width_nl':
                    ['Width of barrier on left-hand-side (m)',
                     ['int', 'float'],
                     ['>0']],
                'barrier_r_type_nl':
                    ['Barrier type on right-hand-side of road',
                     ['str'],
                     ['None', 'SCREEN', 'WALL']],
                'barrier_r_height_nl':
                    ['Height of barrer on right-hand-side (m)',
                     ['int', 'float'],
                     ['>0']],
                'barrier_r_width_nl':
                    ['Width of barrier on right-hand-side (m)',
                     ['int', 'float'],
                     ['>0']],
                'road_type_nl':
                    ['Type of road being modelled',
                     ['str'],
                     ['FREEWAY',
                      'NON_URBAN_ROAD_NATIONAL',
                      'URBAN_ROAD_FREE_FLOW']],
                'direction_nl':
                    ['Direction of traffic on the link',
                     ['str'],
                     ['BOTH', 'A_TO_B', 'B_TO_A']],
                'eft_speed_nl':
                    ['Speed to be modelled kph',
                     ['str'],
                     ['80',
                      '80_enforced',
                      '100',
                      '100_enforced',
                      '120',
                      '130']],
                'eft_veh_movements_nl':
                    ['Averaging period for vehicle movements',
                     ['str'],
                     ['HOUR', 'DAY', 'MONTH', 'YEAR']],
                'eft_light_traffic_nl':
                    ['Number of light traffic vehicles',
                     ['int', 'float'],
                     ['>=0']],
                'eft_light_traffic_congestion_nl':
                    ['Percentage in congestion',
                     ['int', 'float'],
                     range(0, 100)],
                'eft_med_freight_traffic_nl':
                    ['Number of medium freight traffic vehicles',
                     ['int', 'float'],
                     ['>=0']],
                'eft_med_freight_traffic_congestion_nl':
                    ['Percentage in congestion',
                     ['int', 'float'],
                     range(0, 100)],
                'eft_heavy_freight_traffic_nl':
                    ['Number of heavy freight traffic vehicles',
                     ['int', 'float'],
                     ['>=0']],
                'eft_heavy_freight_traffic_congestion_nl':
                    ['Percentage in congestion',
                     ['int', 'float'],
                     range(0, 100)],
                'eft_bus_traffic_nl':
                    ['Number of buses',
                     ['int', 'float'],
                     ['>=0']],
                'eft_bus_traffic_congestion_nl':
                    ['Percentage in congestion',
                     ['int', 'float'],
                     range(0, 100)],
                'custom_desc_nl':
                    ['Unique identifier for custom specification',
                     ['str'],
                     []],
                'custom_euro_nl':
                    ['Euro class for custom specification',
                     ['str'],
                     ['Refer to IMAER guidance document for options']],
                'custom_veh_movements_av_nl':
                    ['Averaging time period for custom vehicles',
                     ['str'],
                     ['HOUR', 'DAY', 'MONTH', 'YEAR']],
                'custom_veh_movements_nl':
                    ['Number of vehicle movements',
                     ['int', 'float'],
                     ['>0']],
                'custom_nox_ems_nl':
                    ['NOx emission per vehicle (g/km)',
                     ['int', 'float'],
                     ['>=0']],
                'custom_no2_ems_nl':
                    ['NO2 emission per vehicle (g/km)',
                     ['int', 'float'],
                     ['>=0']],
                'custom_nh3_ems_nl':
                    ['NH3 emission per vehicle (g/km)',
                     ['int', 'float'],
                     ['>=0']]
                }
