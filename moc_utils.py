# Utility functions for handling MOCs
import pandas as pd
import astropy.units as u
from astropy.time import Time
from mocpy import MOC, STMOC
from sqlalchemy import create_engine
from sregion import parse_s_region

MAX_DEPTH = 9
TIME_DEPTH = 40  # 61 is 1microsecond, 23 is 3 days
# Not clear what DEPTH (mocpy) is in relation to ORDER (ivoa docs)


def get_polygon_moc(row):
    """Construct a MOC"""
    lon = u.Quantity(row['coords']['ra'])
    lat = u.Quantity(row['coords']['dec'])
    temp_moc = MOC.from_polygon(lon, lat, max_depth=MAX_DEPTH)
    return temp_moc.to_string(format='json')


def make_stmoc(row):
    """Construct STMOC"""
    moc = MOC.from_string(row['moc'], format='json')
    times_start = Time([row['t_min']], format='mjd')
    times_end = Time([row['t_max']], format='mjd')
    stmoc = STMOC.from_spatial_coverages(times_start=times_start,
                                         times_end=times_end,
                                         spatial_coverages=[moc],
                                         time_depth=TIME_DEPTH)
    return stmoc.to_string(format='json')


def add_moc_column(df):
    """Add a coords and moc column to the dataframe"""

    df['coords'] = df.apply(lambda x: parse_s_region(x['s_region']), axis=1)
    df['moc'] = df.apply(get_polygon_moc, axis=1)
    df['stmoc'] = df.apply(make_stmoc, axis=1)

    return df


def create_union_moc(df, format='json', col='moc'):
    """ Create a MOC union from a list of MOCs"""

    mobj = STMOC if col == 'stmoc' else MOC

    if format == 'json':
        moc_list = [mobj.from_string(i, format='json') for i in df[col].tolist()]
    else:
        moc_list = df[col].tolist()

    moc = moc_list[0]
    for i in moc_list[1:]:
        moc = moc.union(i)
    return moc


def get_db():
    """ get the sqlite obspointing db """
    connection_string = 'sqlite:///mast_moc.db'
    engine = create_engine(connection_string)
    return pd.read_sql('select * from obspointing', engine)


def get_obs_id(moc):
    """ get the obsservation ids that intersect with the input moc """
    db = get_db()
    moclist = [MOC.from_string(i, format='json') for i in db['moc']]
    sub = [e for e, i in enumerate(moclist) if not moc.intersection(i).empty()]
    return db.iloc[sub][['obs_id', 's_ra', 's_dec']]
