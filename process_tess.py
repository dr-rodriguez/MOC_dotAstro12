# Script to process JWST data
from astropy.time import Time
from fetch_data import fetch_obspointing
from mocpy import MOC
import matplotlib.pyplot as plt

from moc_utils import add_moc_column, create_union_moc

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

moc = create_union_moc(df)

# Plot the MOC using matplotlib
fig = plt.figure(111, figsize=(15, 10))
# Define a astropy WCS easily
wcs = moc.wcs(fig, coordsys="icrs", projection="AIT")
ax = fig.add_subplot(1, 1, 1, projection=wcs)
# Call fill with a matplotlib axe and the `~astropy.wcs.WCS` wcs object.
moc.fill(ax=ax, wcs=wcs, alpha=0.5, fill=True, color="green")
moc.border(ax=ax, wcs=wcs, alpha=0.5, color="black")
plt.xlabel("ra")
plt.ylabel("dec")
plt.title(f"Coverage of {mission}, June 2023")
plt.grid(color="black", linestyle="dotted")
plt.show()

moc.save(f'{mission.lower()}_mission_moc.fits', overwrite=True)


