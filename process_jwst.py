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
                 f'AND t_min >= {t.mjd[0]} AND t_max < {t.mjd[1]}')
print(df)

df = add_moc_column(df)
print(df)

from mocpy import MOC
import matplotlib.pyplot as plt
moc_list = [MOC.from_string(i, format='json') for i in df['moc'].tolist()]
moc = MOC.union(*moc_list[:2])

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
plt.title("Coverage of JWST, June 2023")
plt.grid(color="black", linestyle="dotted")
plt.show()
