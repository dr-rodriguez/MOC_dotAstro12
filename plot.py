# Scripts for handling plotting
import matplotlib.pyplot as plt


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
