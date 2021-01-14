# -*- coding: utf-8 -*-

"""
functioning visualization of the island simulation
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'

#from biosim.simulation import *
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
        self.n_steps = 0
        self.island_map_ax = None
        self.island_map = None
        self.rgb_map = None
        self.leg_ax = None
        self.histogram_age = None
        self.histogram_weight = None
        self.histogram_fitness = None
        self.heatmap_ax = None
        self.img_ax = None
        self.heatmap2_ax = None
        self.img2_ax = None
        self.pop = None
        self.n_carn = None
        self.n_herb = None
        self.count_carn = int()
        self.count_herb = int()
        self.fig = None
        self.year = None
        self.year_current = 0
        self.axt = None
        self.age = 0
        self.weight = 0
        self.fitness = 0

    def setup_graphics(self, nx_step):
        """
        setups a graphics interface with heat maps, line graphs and histograms
        """
        self.n_steps += nx_step
        rgb_value = {'W': (0, 0.5, 1),
                     'D': (1, 1, 0.3),
                     'H': (0, 0.6, 0),
                     'L': (0, 0.3, 0)}

        if self.fig is None:
            self.fig = plt.figure(figsize=(12, 12))
            self.axt = self.fig.add_axes([0.4, 0.8, 0.2, 0.2])

        if self.island_map_ax is None:
            self.island_map_ax = self.fig.add_subplot(3, 3, 1)
            self.island_map = self.island_map_ax.imshow(self.rgb_map)
            self.island_map_ax.set_xticks(range(len(self.rgb_map[0])))
            self.island_map_ax.set_xticklabels([_ + 1 if not (_ + 1) % 5 else '' for _ in range(len(self.rgb_map[0]))])
            self.island_map_ax.set_yticks(range(len(self.rgb_map)))
            self.island_map_ax.set_yticklabels([_ + 1 if not (_ + 1) % 5 else '' for _ in range(len(self.rgb_map))])

        if self.leg_ax is None:
            self.leg_ax = self.fig.add_axes([0.36, 0.7, 0.1, 0.2])
            self.leg_ax.axis('off')
            for ix, name in enumerate(('Water', 'Lowland', 'Highland', 'Desert')):
                self.leg_ax.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1, facecolor=rgb_value[name[0]]))
                self.leg_ax.text(0.35, ix * 0.2, name, transform=self.leg_ax.transAxes)

        if self.heatmap_ax is None:
            self.heatmap_ax = self.fig.add_subplot(4, 2, 5)
            self.img_ax = None

        if self.heatmap2_ax is None:
            self.heatmap2_ax = self.fig.add_subplot(4, 2, 6)
            self.img2_ax = None

        if self.pop is None:
            self.pop = self.fig.add_subplot(3, 3, 3)
            self.pop.set_ylim(0, 1000)

        self.pop.set_xlim(0, self.n_steps + 1)

        if self.n_herb is None:
            herb_plot = self.pop.plot(np.arange(self.n_steps),
                                      np.full(self.n_steps, np.nan), 'b-')
            self.n_herb = herb_plot[0]
        else:
            hx_data, hy_data = self.n_herb.get_data()
            hx_new = np.arange(hx_data[-1] + 1, self.n_steps)
            if len(hx_new) > 0:
                hy_new = np.full(hx_new.shape, np.nan)
                self.n_herb.set_data(np.hstack((hx_data, hx_new)),
                                     np.hstack((hy_data, hy_new)))
        if self.n_carn is None:
            carn_plot = self.pop.plot(np.arange(self.n_steps),
                                      np.full(self.n_steps, np.nan), 'r-')
            self.n_carn = carn_plot[0]
        else:
            cx_data, cy_data = self.n_carn.get_data()
            cx_new = np.arange(cx_data[-1] + 1, self.n_steps)
            if len(cx_new) > 0:
                hy_new = np.full(cx_new.shape, np.nan)
                self.n_carn.set_data(np.hstack((cx_data, cx_new)),
                                     np.hstack((cy_data, hy_new)))

        if self.histogram_age is None:
            self.histogram_age = self.fig.add_subplot(7, 3, 19)
            self.histogram_age.set_xlim(0, 60)
            self.histogram_age.set_ylim(0, 2000)

        if self.histogram_weight is None:
            self.histogram_weight = self.fig.add_subplot(7, 3, 20)
            self.histogram_weight.set_xlim(0, 60)
            self.histogram_weight.set_ylim(0, 1000)

        if self.histogram_fitness is None:
            self.histogram_fitness = self.fig.add_subplot(7, 3, 21)
            self.histogram_fitness.set_xlim(0, 1.0)
            self.histogram_fitness.set_ylim(0, 2000)

        self.histogram_age.hist(self.age, bins=30, histtype='step')

        self.axt.cla()
        self.axt.axis('off')  # turn off coordinate system
        self.year = self.axt.text(0.5, 0.5, 'Year: {:5}'.format(0),
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
        self.histogram_age.set_ylim(0, 500)
        self.histogram_age.hist(self.age, bins=30, histtype='step')

        self.histogram_weight.cla()
        self.histogram_weight.set_xlim(0, 60)
        self.histogram_weight.set_ylim(0, 250)
        self.histogram_weight.hist(self.weight, bins=30, histtype='step')

        self.histogram_fitness.cla()
        self.histogram_fitness.set_xlim(0, 1)
        self.histogram_fitness.set_ylim(0, 500)
        self.histogram_fitness.hist(self.fitness, bins=20, histtype='step')

        if self.img_ax is not None:
            self.img_ax.set_data(cells_map)
        else:
            self.img_ax = self.heatmap_ax.imshow(cells_map, interpolation='nearest', vmin=0, vmax=200)
            plt.colorbar(self.img_ax, ax=self.heatmap_ax, orientation='vertical')

        if self.img2_ax is not None:
            self.img2_ax.set_data(cells_map2)
        else:
            self.img2_ax = self.heatmap2_ax.imshow(cells_map2, interpolation='nearest', vmin=0, vmax=50)
            plt.colorbar(self.img2_ax, ax=self.heatmap2_ax, orientation='vertical')

        self.fig.canvas.flush_events()
        plt.pause(1e-6)

    def update_data(self, n_species: dict, list_of_ages, l_weights, l_fitness):
        self.count_herb = n_species["Herbivore"]
        self.count_carn = n_species["Carnivore"]

        self.age = list_of_ages
        self.weight = l_weights
        self.fitness = l_fitness

    def convert_map(self, map_str: str):
        rgb_value = {'W': (0, 0.5, 1),
                     'D': (1, 1, 0.3),
                     'H': (0, 0.6, 0),
                     'L': (0, 0.3, 0)}

        self.rgb_map = [[rgb_value[column] for column in row]
                        for row in map_str.split()]


if __name__ == "__main__":
    geogr = """\
                   WWWWWWWWWWWWWWWWWWWWW
                   WWWWWWWWHWWWWLLLLLLLW
                   WHHHHHLLLLWWLLLLLLLWW
                   WHHHHHHHHHWWLLLLLLWWW
                   WHHHHHLLLLLLLLLLLLWWW
                   WHHHHHLLLDDLLLHLLLWWW
                   WHHLLLLLDDDLLLHHHHWWW
                   WWHHHHLLLDDLLLHWWWWWW
                   WHHHLLLLLDDLLLLLLLWWW
                   WHHHHLLLLDDLLLLWWWWWW
                   WWHHHHLLLLLLLLWWWWWWW
                   WWWHHHHLLLLLLLWWWWWWW
                   WWWWWWWWWWWWWWWWWWWWW"""
    v = Visualization()
    v.convert_map(geogr)
    v.setup_graphics()
    for k in range(300):
        sim = {'herbivore': random.randint(2000, 8000), 'carnivore': random.randint(1, 6000)}
        z = np.random.randint(200, size=(13, 21))
        z2 = np.random.randint(200, size=(13, 21))
        v.get_data(sim)
        v.update_graphics(k, z, z2)
    plt.ioff()
    plt.show()
