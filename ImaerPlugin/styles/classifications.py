
classifications = {}

classifications['nl_contribution'] = {
    'render_type': 'graduated',
    'classes': [
        ['0.00 - 1.07', 0, 1.07, 'fffdb3'],
        ['1.07 - 2.86', 1.07, 2.86, 'fde76a'],
        ['2.86 - 5.00', 2.86, 5, 'feb66e'],
        ['5.00 - 7.14', 5, 7.14, 'a5cc46'],
        ['7.14 - 10.00', 7.14, 10, '23a870'],
        ['10.00 - 15.00', 10, 15, '5a7a32'],
        ['15.00 - 20.00', 15, 20, '0093bd'],
        ['20.00 - 25.00', 20, 25, '0d75b5'],
        ['25.00 - 35.71', 25, 35.71, '6a70b1'],
        ['35.71 - 71.43', 35.71, 71.43, '304594'],
        ['71.43 - 107.14', 71.43, 107.14, '5e2c8f'],
        ['107.14 - 142.86', 107.14, 142.86, '3f2a84'],
        ['> 142.86', 142.86, 100000000, '2a1612']
    ]
}

classifications['uk_contribution'] = {
    'render_type': 'graduated',
    'classes': [
        ['0.00 - 0.25', 0, 0.25, 'fffdb3'],
        ['0.25 - 0.50', 0.25, 0.50, 'fde76a'],
        ['0.50 - 1.00', 0.50, 1, 'feb66e'],
        ['1.00 - 1.50', 1, 1.5, 'a5cc46'],
        ['1.50 - 2.00', 1.5, 2, '23a870'],
        ['2.00 - 3.00', 2, 3, '5a7a32'],
        ['3.00 - 4.00', 3, 4, '0093bd'],
        ['4.00 - 5.00', 4, 5, '0d75b5'],
        ['5.00 - 10.00', 5, 10, '6a70b1'],
        ['10.00 - 15.00', 10, 15, '304594'],
        ['15.00 - 20.00', 15, 20, '5e2c8f'],
        ['20.00 - 25.00', 20, 25, '3f2a84'],
        ['> 25.00', 25, 100000000, '2a1612']
    ]
}

classifications['nl_difference'] = {
    'render_type': 'graduated',
    'classes': [
        ['< -20.00', -100000000, -20, '507122'],
        ['-20.00 - -10.00', -20, -10, '507122'],
        ['-10.00 - -5.00', -10, -5, '738d4e'],
        ['-5.00 - -2.86', -5, -2.86, '96aa7a'],
        ['-2.86 - -1.07', -2.86, -1.07, 'b9c6a7'],
        ['-1.07 - 0.00', -1.07, 0, 'dce3d3'],
        ['0.00 - 1.07', 0, 1.07, 'd8d3e5'],
        ['1.07 - 2.86', 1.07, 2.86, 'b1a9cb'],
        ['2.86 - 5.00', 2.86, 5, '8b7db0'],
        ['5.00 - 10.00', 5, 10, '645296'],
        ['10.00 - 20.00', 10, 20, '3d277c'],
        ['> 20.00', 20, 100000000, '3d277c']
    ]
}

classifications['uk_difference'] = {
    'render_type': 'graduated',
    'classes': [
        ['< -25.00', -100000000, -25, '507122'],
        ['-25.00 - -16.00', -25, -16, '507122'],
        ['-16.00 - -8.00', -16, -8, '738d4e'],
        ['-8.00 - -4.00', -8, -4, '96aa7a'],
        ['-4.00 - -2.00', -4, -2, 'b9c6a7'],
        ['-2.00 - 0.00', -2, 0, 'dce3d3'],
        ['0.00 - 2.00', 0, 2, 'd8d3e5'],
        ['2.00 - 4.00', 2, 4, 'b1a9cb'],
        ['4.00 - 8.00', 4, 8, '8b7db0'],
        ['8.00 - 16.00', 8, 16, '645296'],
        ['16.00 - 25.00', 16, 25, '3d277c'],
        ['> 25.00', 25, 100000000, '3d277c']
    ]
}