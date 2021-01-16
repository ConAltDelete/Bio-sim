# -*- coding: utf-8 -*-

"""
functioning visualization of the island simulation
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'

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
    def __init__(self, img_base, img_fmt):
        self.meta_data = {
            "Herbivore": {
                "colour": (1,0,0)
            },
            "Carnivore": {
                "colour": (0,0,1)
            }
        }
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
        self.n = dict()
        self.count = dict()
        self.fig = None
        self.year = None
        self.year_current = 0
        self.axt = None
        self.age = dict()
        self.weight = dict()
        self.fitness = dict()

        self._img_base = img_base
        self._img_ctr = 0
        self._img_fmt = img_fmt

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
            self.pop.set_ylim(0, 300)

        self.pop.set_xlim(0, self.n_steps + 1)

        for species in self.n:
            if self.n[species] is None:
                self.n[species] = (self.pop.plot(np.arange(self.n_steps),
                                      np.full(self.n_steps, np.nan), 'b-'))[0]
            else:
                hx_data, hy_data = self.n[species].get_data()
                hx_new = np.arange(hx_data[-1] + 1, self.n_steps)
                if len(hx_new) > 0:
                    hy_new = np.full(hx_new.shape, np.nan)
                    self.n[species].set_data(np.hstack((hx_data, hx_new)),
                                         np.hstack((hy_data, hy_new)))

        if self.histogram_age is None:
            self.histogram_age = self.fig.add_subplot(7, 3, 19)

        if self.histogram_weight is None:
            self.histogram_weight = self.fig.add_subplot(7, 3, 20)

        if self.histogram_fitness is None:
            self.histogram_fitness = self.fig.add_subplot(7, 3, 21)

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
        self.year_current = current_year
        self.year.set_text('Year:{:5}'.format(self.year_current))

        for species in self.n:
            data = self.n[species].get_ydata()
            data[current_year] = self.count[species]
            self.n[species].set_ydata(data)

        self.histogram_age.cla()
        self.histogram_age.set_xlim(0, 60)
        self.histogram_age.set_ylim(0, 2000)
        for species in self.weight:
            self.histogram_age.hist(self.age[species], bins=30, histtype='step', color=self.meta_data[species]["colour"])

        self.histogram_weight.cla()
        self.histogram_weight.set_xlim(0, 60)
        self.histogram_weight.set_ylim(0, 1000)
        for species in self.weight:
            self.histogram_weight.hist(self.weight[species], bins=30, histtype='step', color=self.meta_data[species]["colour"])

        self.histogram_fitness.cla()
        self.histogram_fitness.set_xlim(0, 1)
        self.histogram_fitness.set_ylim(0, 2000)
        for species in self.weight:
            self.histogram_fitness.hist(self.fitness[species], bins=20, histtype='step', color=self.meta_data[species]["colour"])

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

    def update_data(self, n_species: dict, l_ages, l_weights, l_fitness):
        for species in n_species:
            self.count[species] = n_species[species]
        
        for species in n_species:
            self.age[species] = l_ages[species]
            self.weight[species] = l_weights[species]
            self.fitness[species] = l_fitness[species]

    def convert_map(self, map_str: str):
        rgb_value = {'W': (0, 0.5, 1),
                     'D': (1, 1, 0.3),
                     'H': (0, 0.6, 0),
                     'L': (0, 0.3, 0)}

        self.rgb_map = [[rgb_value[column] for column in row]
                        for row in map_str.split()]

    def create_images(self):
        """saves images to file"""
        if self._img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1


if __name__ == "__main__":
    from biosim.simulation import *
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
    v = Visualization(".",".")
    v.convert_map(geogr)
    v.setup_graphics(1)
    for k in range(300):
        sim = {'herbivore': random.randint(2000, 8000), 'carnivore': random.randint(1, 6000)}
        z = np.random.randint(200, size=(13, 21))
        z2 = np.random.randint(200, size=(13, 21))
        v.get_data(sim)
        v.update_graphics(k, z, z2)
    plt.ioff()
    plt.show()
