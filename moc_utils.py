# Utility functions for handling MOCs
import astropy.units as u
from mocpy import MOC
import matplotlib.pyplot as plt
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


def plot_moc(moc):
    """ Plot a MOC object """
    # Plot the MOC using matplotlib
    fig = plt.figure(figsize=(10, 10))
    wcs = moc.wcs(fig)
    ax = fig.add_subplot(projection=wcs)
    moc.border(ax, wcs, color='blue')


def create_union_moc(df):
    """ Create a MOC union from a list of MOCs"""
    moc = df['moc'].iloc[0]
    for i in df['moc']:
        moc = moc.union(i)
    return moc



