# Utility functions for handling MOCs
import astropy.units as u
from mocpy import MOC
from sregion import parse_s_region

MAX_DEPTH = 9


def get_polygon_moc(row):
    # print('{} ({} {}) {}'.format(row['obs_id'], row['s_ra'], row['s_dec'], row['s_region']))
    lon = u.Quantity(row['coords']['ra'])
    lat = u.Quantity(row['coords']['dec'])
    temp_moc = MOC.from_polygon(lon, lat, max_depth=MAX_DEPTH)
    return temp_moc


def add_moc_column(df):
    """Add a coords and moc column to the dataframe"""

    df['coords'] = df.apply(lambda x: parse_s_region(x['s_region']), axis=1)
    df['moc'] = df.apply(get_polygon_moc, axis=1)

    return df
