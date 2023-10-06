# Script to process JWST data
from astropy.time import Time
from fetch_data import fetch_obspointing
from moc_utils import add_moc_column, create_union_moc
from plot import plot_moc

from moc_utils import add_moc_column, create_union_moc

mission = 'JWST'

# Convert time to MJD
times = ['2023-06-01', '2023-07-01']
t = Time(times)
print(t.mjd)

# Get data from TAP
df = fetch_obspointing(mission,
                 f'AND t_min >= {t.mjd[0]} AND t_max < {t.mjd[1]}')
print(df)

# Generate MOCs
df = add_moc_column(df)
print(df)

# Store in database
from sqlalchemy import create_engine
connection_string = 'sqlite:///caom.db'
engine = create_engine(connection_string)
df.to_sql('caom', engine)

# Plot the MOCs
from mocpy import MOC
import matplotlib.pyplot as plt
moc_list = [MOC.from_string(i, format='json') for i in df['moc'].tolist()]

# Union the mocs
moc = create_union_moc(df, format='json')

# Plot the MOC using matplotlib
plot_moc(moc)
