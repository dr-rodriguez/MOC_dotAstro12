# Script to process TESS data
from astropy.time import Time
from sqlalchemy import create_engine 
from fetch_data import fetch_obspointing
from moc_utils import add_moc_column, create_union_moc
from plot import plot_moc

mission = 'TESS'

# Convert time to MJD
times = ['2023-06-01', '2023-07-01']
t = Time(times)
print(t.mjd)

# Get data from TAP
df = fetch_obspointing(mission,
                 f"AND t_min >= {t.mjd[0]} AND t_max < {t.mjd[1]} AND dataproduct_type = 'image'")
print(df)

df = add_moc_column(df)
print(df)

# Store in database
connection_string = 'sqlite:///mast_moc.db'
engine = create_engine(connection_string)
# can use if_exists='append' to add to table
no_coords = [x for x in df.columns if x!='coords']  # need to eliminate coords since it has Quantity objects
df[no_coords].to_sql(name='obspointing', con=engine, if_exists='append', index=False)


# Union the mocs
moc = create_union_moc(df)

# Save the union MOC
moc.save(f'{mission.lower()}_mission_moc.fits', overwrite=True)

# Plot the MOC using matplotlib
plot_moc(moc)
