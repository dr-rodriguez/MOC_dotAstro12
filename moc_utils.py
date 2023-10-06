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
    return temp_moc.to_string(format='json')


def add_moc_column(df):
    """Add a coords and moc column to the dataframe"""

    df['coords'] = df.apply(lambda x: parse_s_region(x['s_region']), axis=1)
    df['moc'] = df.apply(get_polygon_moc, axis=1)

    return df


def create_union_moc(df, format='json'):
    """ Create a MOC union from a list of MOCs"""

    if format=='json':
        moc_list = [MOC.from_string(i, format='json') for i in df['moc'].tolist()]
    else:
        moc_list = df['moc'].tolist()

    moc = moc_list[0]
    for i in moc_list[1:]:
        moc = moc.union(i)
    return moc
