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


class Visualization:
    """
    Visualization
    """
    def __init__(self):
        self.histogram_age = None
        self.histogram_weight = None
        self.histogram_fitness = None
        self.heatmap = dict()
        self.pop = None
        self.n_carn = list()
        self.n_herb = list()
        self.count_carn = int()
        self.count_herb = int()
        self.fig = plt.figure()
        self.year = None
        self.year_current = 0
        self.axt = self.fig.add_axes([0.4, 0.8, 0.2, 0.2])

    def setup_graphics(self, n_steps=300):
        """
        setups a graphics interface with heat maps, line graphs and histograms
        """
        # normal subplots
        if self.pop is None:
            self.pop = self.fig.add_subplot(2, 3, 1)
            self.pop.set_xlim(0, 300)
            self.pop.set_ylim(0, 8000)

        self.n_herb = self.pop.plot(np.arange(n_steps),
                                    np.full(n_steps, np.nan), 'b-')[0]
        self.n_carn = self.pop.plot(np.arange(n_steps),
                                    np.full(n_steps, np.nan), 'r-')[0]
        if self.histogram_age is None:
            self.histogram_age = self.fig.add_subplot(2, 3, 3)
            self.histogram_age.set_xlim(0, 60)
            self.histogram_age.set_ylim(0, 2000)
        if self.histogram_weight is None:
            self.histogram_weight = self.fig.add_subplot(2, 3, 4)
            self.histogram_weight.set_xlim(0, 60)
            self.histogram_weight.set_ylim(0, 1000)
        if self.histogram_fitness is None:
            self.histogram_fitness = self.fig.add_subplot(2, 3, 5)
            self.histogram_fitness.set_xlim(0, 1.0)
            self.histogram_fitness.set_ylim(0, 2000)

        ax5 = self.fig.add_subplot(2, 3, 6)

        self.histogram_age.hist([1,1,1,2,3,4,4,5])

        # axes for text
        # llx, lly, w, h
        self.axt.axis('off')  # turn off coordinate system

        template = 'Count: {:5}'
        self.year = self.axt.text(0.5, 0.5, template.format(0),
                            horizontalalignment='center',
                            verticalalignment='center',
                            transform=self.axt.transAxes)  # relative coordinates

        plt.pause(1e-6)  # pause required to make figure visible

        """input('Press ENTER to begin counting')

        for k in range(40):
            txt.set_text(template.format(k))
            plt.pause(0.1)"""

        plt.ion()

    def update_graphics(self, current_year):
        """
        updates the graphics interface with new data and shows it live
        """

        self.year.set_text('Count:{:5}'.format(self.year_current))
        self.year_current = current_year

        herbdata = self.n_herb.get_ydata()
        carndata = self.n_carn.get_ydata()
        herbdata[current_year] = self.count_herb
        carndata[current_year] = self.count_carn
        self.n_herb.set_ydata(herbdata)
        self.n_carn.set_ydata(carndata)
        self.fig.canvas.flush_events()

        plt.pause(1e-6)

    def get_data(self, n_species: dict, cells=None):
        self.count_herb = n_species["herbivore"]
        self.count_carn = n_species["carnivore"]


if __name__ == "__main__":
    v = Visualization()
    v.setup_graphics()
    for k in range(50):
        sim = {'herbivore': random.randint(2000, 8000), 'carnivore': random.randint(1, 6000)}
        v.get_data(sim)
        v.update_graphics(k)
    plt.show()
