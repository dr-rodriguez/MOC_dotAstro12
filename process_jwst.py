# Script to process JWST data
from astropy.time import Time
from fetch_data import fetch_obspointing
from moc_utils import add_moc_column, create_union_moc
from plot import plot_moc
from sqlalchemy import create_engine 


# Convert time to MJD
times = ['2023-06-01', '2023-07-01']
t = Time(times)
print(t.mjd)

# Get data from TAP
df = fetch_obspointing('JWST',
                 f'AND t_min >= {t.mjd[0]} AND t_max < {t.mjd[1]}')
print(df)

# Generate MOCs
df = add_moc_column(df)
print(df)

# Store in database
connection_string = 'sqlite:///mast_moc.db'
engine = create_engine(connection_string)
# can use if_exists='append' to add to table
no_coords = [x for x in df.columns if x!='coords']  # need to eliminate coords since it has Quantity objects
df[no_coords].to_sql(name='obspointing', con=engine, if_exists='replace', index=False)

# Union the mocs
moc = create_union_moc(df, format='json')

# Plot the MOC using matplotlib
plot_moc(moc)
