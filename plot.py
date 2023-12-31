# Scripts for handling plotting
import matplotlib.pyplot as plt
import astropy.units as u
import matplotlib.pyplot as plt
from astropy.coordinates import Angle, SkyCoord
from mocpy import WCS


def plot_moc(moc):
    """ Plot a MOC object """
    # Plot the MOC using matplotlib
    fig = plt.figure(figsize=(10, 10))
    wcs = moc.wcs(fig, coordsys="icrs", projection="AIT")
    ax = fig.add_subplot(1, 1, 1, projection=wcs)

    moc.fill(ax=ax, wcs=wcs, alpha=0.5, fill=True, color="green")
    moc.border(ax=ax, wcs=wcs, alpha=0.5, color="black")
    
    plt.xlabel("ra")
    plt.ylabel("dec")
    plt.grid(color="black", linestyle="dotted")
    plt.show()


def plot_unions(mocs: list, missions: list = []):
    """ Plot the unions / intersections between a set of MOCs """

    # Compute their union and intersection
    inter = mocs[0]
    union = mocs[0]
    for i in mocs[1:]:
        inter &= i
        union += i

    # Plot the MOC using matplotlib
    fig = plt.figure(111, figsize=(10, 10))
    # Define a astropy WCS easily
    with WCS(
        fig,
        fov=160 * u.deg,
        center=SkyCoord(0, 0, unit="deg", frame="icrs"),
        coordsys="icrs",
        rotation=Angle(0, u.degree),
        projection="AIT",
    ) as wcs:
        ax = fig.add_subplot(1, 1, 1, projection=wcs)
        # Call fill with a matplotlib axe and the `~astropy.wcs.WCS` wcs object.
        union.fill(
            ax=ax,
            wcs=wcs,
            alpha=0.5,
            fill=True,
            color="red",
            linewidth=0,
            label="Union",
        )
        union.border(ax=ax, wcs=wcs, alpha=1, color="red")

        inter.fill(
            ax=ax,
            wcs=wcs,
            alpha=0.5,
            fill=True,
            color="green",
            linewidth=0,
            label="Intersection",
        )
        inter.border(ax=ax, wcs=wcs, alpha=1, color="green")
        ax.legend()

    plt.xlabel("ra")
    plt.ylabel("dec")
    plt.title(f"Logical operations between {', '.join(missions)}")
    plt.grid(color="black", linestyle="dotted")
    plt.show()


def plot_moc_with_targets(moc, df, intersect_moc=None, save=None):
    """ Plot a MOC object adding targets from a dataframe """

    fig = plt.figure(figsize=(10, 10))
    with WCS(
        fig,
        fov=360 * u.deg,
        center=SkyCoord(0, 0, unit="deg", frame="icrs"),
        coordsys="icrs",
        rotation=Angle(0, u.degree),
        projection="AIT",
    ) as wcs:
        # wcs = moc.wcs(fig, coordsys="icrs", projection="AIT",
        #               rotation=Angle(0, u.degree),)
        ax = fig.add_subplot(1, 1, 1, projection=wcs)

        # The MOC itself
        moc.fill(ax=ax, wcs=wcs, alpha=0.5, fill=True, color="green")
        moc.border(ax=ax, wcs=wcs, alpha=0.5, color="black")

        # Intersection moc
        if intersect_moc is not None:
            intersect_moc.fill(ax=ax, wcs=wcs, alpha=0.5, fill=True, color="red")
            intersect_moc.border(ax=ax, wcs=wcs, alpha=1, color="red")

        # The dataframe rows
        for _, row in df.iterrows():
            x, y = wcs.world_to_pixel(SkyCoord(ra=row['s_ra'] * u.deg, dec=row['s_dec'] * u.deg))
            ax.text(x, y, row['obs_id'])

    plt.xlabel("ra")
    plt.ylabel("dec")
    plt.grid(color="black", linestyle="dotted")
    
    if save:
        plt.savefig(save)
    else:
        plt.show()

