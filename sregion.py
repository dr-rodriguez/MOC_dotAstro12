# Utility functions for working with sregion
import numpy as np
import astropy.units as u
from astropy.visualization.wcsaxes.patches import _rotate_polygon


def convert_to_polygon(center_ra, center_dec, radius, resolution=16):
    """
    Convert a circle to a polygon

    :param center_ra: astropy.units.Quantity
    :param center_dec: astropy.units.Quantity
    :param radius: astropy.units.Quantity
    :param resolution: int
    :return:
    """
    lon = np.linspace(0., 2 * np.pi, resolution + 1)[:-1] * u.radian
    lat = np.repeat(0.5 * np.pi - radius.to_value(u.radian), resolution) * u.radian
    lon, lat = _rotate_polygon(lon, lat, center_ra, center_dec)
    lon = lon.to_value(u.deg).tolist()
    lat = lat.to_value(u.deg).tolist()
    return lon, lat


def parse_s_region(s_region):
    """Parse the s_region into a dictionary of ra/dec values"""
    ra = []
    dec = []
    counter = 0

    if s_region is None or s_region.split()[0].upper() not in ('POLYGON', 'CIRCLE'):
        print(f'Unsupported shape: {s_region}')
        return None

    if s_region.split()[0].upper() == 'POLYGON':
        for elem in s_region.strip().split():
            try:
                value = float(elem)
            except ValueError:
                continue
            if counter % 2 == 0:
                ra.append(value * u.deg)
            else:
                dec.append(value * u.deg)
            counter += 1
    elif s_region.split()[0].upper() == 'CIRCLE':
        center_ra, center_dec, radius = None, None, None
        for elem in s_region.strip().split():
            try:
                value = float(elem)
            except ValueError:
                continue
            if counter % 2 == 1:
                center_dec = value
            if center_ra is None and counter % 2 == 0:
                center_ra = value
            else:
                radius = value
            counter += 1
        ra, dec = convert_to_polygon(center_ra*u.deg, center_dec*u.deg, radius*u.deg)

    return {'ra': ra, 'dec': dec}
