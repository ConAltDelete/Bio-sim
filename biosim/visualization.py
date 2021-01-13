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
        self.island_map_ax = None
        self.island_map = None
        self.histogram_age = None
        self.histogram_weight = None
        self.histogram_fitness = None
        self.heatmap_ax = None
        self.img_ax = None
        self.heatmap2_ax = None
        self.img2_ax = None
        self.pop = None
        self.n_carn = list()
        self.n_herb = list()
        self.count_carn = int()
        self.count_herb = int()
        self.fig = None
        self.year = None
        self.year_current = 0
        self.axt = None
        self.age = 0
        self.weight = 0
        self.fitness = 0

    def setup_graphics(self, island_map, n_steps=300):
        """
        setups a graphics interface with heat maps, line graphs and histograms
        """
        if self.fig is None:
            self.fig = plt.figure(figsize=(12, 12))
            self.axt = self.fig.add_axes([0.4, 0.8, 0.2, 0.2])

        if self.island_map_ax is None:
            self.island_map_ax = self.fig.add_subplot(2, 2, 1)
            self.island_map = self.island_map_ax.imshow(island_map)

        if self.heatmap_ax is None:
            self.heatmap_ax = self.fig.add_subplot(4, 2, 6)
            self.img_ax = None

        if self.heatmap2_ax is None:
            self.heatmap2_ax = self.fig.add_subplot(4, 2, 5)
            self.img2_ax = None

        if self.pop is None:
            self.pop = self.fig.add_subplot(2, 2, 2)
            self.pop.set_ylim(0, 8000)

        self.pop.set_xlim(0, n_steps + 1)

        self.n_herb = self.pop.plot(np.arange(n_steps),
                                    np.full(n_steps, np.nan), 'b-')[0]
        self.n_carn = self.pop.plot(np.arange(n_steps),
                                    np.full(n_steps, np.nan), 'r-')[0]

        if self.histogram_age is None:
            self.histogram_age = self.fig.add_subplot(5, 3, 13)
            self.histogram_age.set_xlim(0, 60)
            self.histogram_age.set_ylim(0, 2000)

        if self.histogram_weight is None:
            self.histogram_weight = self.fig.add_subplot(5, 3, 14)
            self.histogram_weight.set_xlim(0, 60)
            self.histogram_weight.set_ylim(0, 1000)

        if self.histogram_fitness is None:
            self.histogram_fitness = self.fig.add_subplot(5, 3, 15)
            self.histogram_fitness.set_xlim(0, 1.0)
            self.histogram_fitness.set_ylim(0, 2000)

        self.histogram_age.hist(self.age, bins=30, histtype='step')

        self.axt.axis('off')  # turn off coordinate system

        template = 'Year: {:5}'
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

    def update_graphics(self, current_year, cells_map, cells_map2):
        """
        updates the graphics interface with new data and shows it live
        TODO: cells_map and cells_map2 make into 1 as a dict
        """

        self.year.set_text('Year:{:5}'.format(self.year_current))
        self.year_current = current_year

        herbdata = self.n_herb.get_ydata()
        carndata = self.n_carn.get_ydata()
        herbdata[current_year] = self.count_herb
        carndata[current_year] = self.count_carn
        self.n_herb.set_ydata(herbdata)
        self.n_carn.set_ydata(carndata)

        self.histogram_age.cla()
        self.histogram_age.set_xlim(0, 60)
        self.histogram_age.set_ylim(0, 2000)
        self.histogram_age.hist(self.age, bins=30, histtype='step')

        self.histogram_weight.cla()
        self.histogram_weight.set_xlim(0, 60)
        self.histogram_weight.set_ylim(0, 1000)
        self.histogram_weight.hist(self.weight, bins=30, histtype='step')

        self.histogram_fitness.cla()
        self.histogram_fitness.set_xlim(0, 1)
        self.histogram_fitness.set_ylim(0, 2000)
        self.histogram_fitness.hist(self.fitness, bins=20, histtype='step')

        if self.img_ax is not None:
            self.img_ax.set_data(cells_map)
        else:
            self.img_ax = self.heatmap_ax.imshow(cells_map, interpolation='nearest', vmin=0, vmax=200)
            plt.colorbar(self.img_ax, ax=self.heatmap_ax, orientation='vertical')

        if self.img2_ax is not None:
            self.img2_ax.set_data(cells_map2)
        else:
            self.img2_ax = self.heatmap2_ax.imshow(cells_map2, interpolation='nearest', vmin=0, vmax=200)
            plt.colorbar(self.img2_ax, ax=self.heatmap2_ax, orientation='vertical')

        self.fig.canvas.flush_events()
        plt.pause(1e-6)

    def get_data(self, n_species: dict, cells=None):
        self.count_herb = n_species["herbivore"]
        self.count_carn = n_species["carnivore"]

        self.age = np.random.randint(120, size=8000)
        self.weight = np.random.randint(120, size=8000)
        self.fitness = np.random.random(8000)


if __name__ == "__main__":
    v = Visualization()
    v.setup_graphics()
    for k in range(300):
        sim = {'herbivore': random.randint(2000, 8000), 'carnivore': random.randint(1, 6000)}
        z = np.random.randint(200, size=(21, 21))
        z2 = np.random.randint(200, size=(21, 21))
        v.get_data(sim)
        v.update_graphics(k, z, z2)
    plt.ioff()
    plt.show()
