# Script to handle MOC intersections
import pandas as pd 
from sqlalchemy import create_engine
from mocpy import MOC
from plot import plot_moc, plot_moc_with_targets

# Read in the MOCs
jwst = MOC.from_fits('jwst_mission_moc.fits')
tess = MOC.from_fits('tess_mission_moc.fits')

# Intersect them
moc = tess.intersection(jwst)

# Plot intersection
# plot_moc(moc)

# Find obervations
conn = create_engine('sqlite:///mast_moc.db').connect()
df = pd.read_sql_table('obspointing', conn)
print(df)

# Crude intersection, but fast for ~4k rows
moc_list = [MOC.from_string(i, format='json') for i in df['moc'].tolist()]
moc_ind = []
for i, t in enumerate(moc_list):
    temp = moc.intersection(t)
    if not temp.empty():
        print(i, temp)
        moc_ind.append(i)

# Observations in the intersection
result = df.iloc[moc_ind][['obs_id', 's_ra', 's_dec']]
print(result)

# Plot alongside MOC intersection
plot_moc_with_targets(tess, result, save='june2023.png')
