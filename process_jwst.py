# Script to process JWST data
from astropy.time import Time
from fetch_data import fetch_obspointing
from moc_utils import add_moc_column

# Convert time to MJD
times = ['2023-06-01', '2023-07-01']
t = Time(times)
print(t.mjd)

# Get data from TAP
df = fetch_obspointing('JWST',
                 f'AND t_min > {t.mjd[0]} AND t_max < {t.mjd[1]}')
print(df)

df = add_moc_column(df)
print(df)
