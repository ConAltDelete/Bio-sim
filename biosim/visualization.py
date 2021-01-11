# -*- coding: utf-8 -*-

"""
functioning visualization of the island simulation
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'

from biosim.simulation import *
import matplotlib.pyplot as plt
import random
import numpy as np

"""
1. grab information from the island simulation every cycle
2. set up a plot graphics window
3. update the graphics window every cycle
4. the graphics windows contains:
    Geography; the map is visualized with colors
    Total number of animals by species; shown as a line graph
    Population map; each species is shown with a heat map
    Histograms; shall show histograms of each species ages, weights and fitness
    Year; the current year shall be shown
"""


def random_numbers():
    return random.random()


class Visualization:
    """
    Visualization
    """
    def __init__(self): ...

    @staticmethod
    def setup_graphics():
        """
        setups a graphics interface with heat maps, line graphs and histograms
        """
        fig = plt.figure()

        # normal subplots
        ax1 = fig.add_subplot(2, 3, 1)
        ax2 = fig.add_subplot(2, 3, 3)
        ax3 = fig.add_subplot(2, 3, 4)
        ax4 = fig.add_subplot(2, 3, 5)
        ax5 = fig.add_subplot(2, 3, 6)

        # axes for text
        axt = fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
        axt.axis('off')  # turn off coordinate system

        template = 'Count: {:5}'
        txt = axt.text(0.5, 0.5, template.format(0),
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=axt.transAxes)  # relative coordinates

        plt.pause(1e-6)  # pause required to make figure visible

        input('Press ENTER to begin counting')

        for k in range(40):
            txt.set_text(template.format(k))
            plt.pause(0.1)

        plt.show()

    def update_graphics(self, n_steps):
        """
        updates the graphics interface with new data and shows it live
        """
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim(0, n_steps)
        ax.set_ylim(0, 1)

        line = ax.plot(np.arange(n_steps),
                       np.full(n_steps, np.nan), 'b-')[0]

        for n in range(n_steps):
            ydata = line.get_ydata()
            ydata[n] = np.random.random()
            line.set_ydata(ydata)
            fig.canvas.flush_events()
            plt.pause(1e-6)


if __name__ == "__main__":
    Visualization.setup_graphics()
