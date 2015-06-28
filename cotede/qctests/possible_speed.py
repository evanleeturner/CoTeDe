# -*- coding: utf-8 -*-

from numpy import ma


def haversine(lat_a, lon_a, lat_b, lon_b):
    """

        Copied from MAUD.
    """

    lat_a, lon_a, lat_b, lon_b = map(radians, [lat_a, lon_a, lat_b, lon_b])

    dlat = lat_a - lat_b
    dlon = lon_a - lon_b
    d = np.sin(dlat / 2) ** 2 + \
            np.cos(lat_a) * np.cos(lat_b) * np.sin(dlon / 2) ** 2
    h = 2 * AVG_EARTH_RADIUS * np.arcsin(np.sqrt(d))

    return h


def speed(data):
    """
    """
    #assert hasattr(data, 'attributes'), "Missing attributes"
    assert ('timeS' in data.keys()), \
            "Missing timeS in input data"
    assert ('latitude' in data.keys()), \
            "Missing latitude in input data"
    assert ('longitude' in data.keys()), \
            "Missing longitude in input data"
    

    dL = haversine(data['longitude'][:-1], data['latitude'][:-1],
            data['longitude'][1:], data['latitude'][1:])
    dt = ma.diff(data['timeS'])

    speed = ma.append(ma.masked_array([0], [True]),
            dL/dt)

    return speed


def possible_speed(data, cfg):
    """

        Consider 4 if smooth is higher, 3 if smooth smaller, 1 if raw smaller
    """
    s = speed(data)

    flag = np.zeros(s.shape, dtype='i1')

    #flag[np.nonzero(ds >= cfg['threshold'])] = cfg['flag_good']
    #flag[np.nonzero(ds < cfg['threshold'])] = cfg['flag_bad']
    flag[s <= 60] = 1
    flag[s > 60] = 3

    # Flag as 9 any masked input value
    for v in ['latitude', 'longitude']:
        flag[ma.getmaskarray(data[v])] = 9

    return flag, s