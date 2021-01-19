# -*- coding: utf-8 -*-

"""
Visualization of the BioSim project
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'

import matplotlib.pyplot as plt
import numpy as np
import os


class Visualization:
    """
        Visualization is the graphics interface of the BioSim project that displays a island map, population graph,
        population heatmap and histogram distributions based on age, weight and fitness.


        :param names: names of species
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'`
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers

        Visualization does as follows:
        - grab information from the island simulation every cycle (mostly handled by simulation.py)
        - set up a plot graphics window
        - update the graphics window every cycle
        - the graphics windows contains:
            Geography; the map is visualized with colors
            Total number of animals by species; shown as a line graph
            Population map; each species is shown with a heat map
            Histograms; shall show histograms of each species ages, weights and fitness
            Year; the current year shall be shown
    """
    def __init__(self, names, img_base, img_fmt, ymax_animals):
        colours = [ (1,0,0), (0,0,1), (0,1,0), (0,1,1), (1,1,0), (1,0,1) ]
        while len(names) > len(colours):
            colours = set(colours)
            colours.update(inner_points(colours))
            colours = list(colours)
        
        self.meta_data = {
            d[0]:{"colour":d[1]} for d in zip(names,colours)
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
        self.y_set_lim = ymax_animals
        self.y_def_lim = 0
        self.n = {species:None for species in names}
        self.count = dict()
        self.fig = None
        self.year = None
        self.year_current = 0
        self.axt = None
        self.def_cmax = {'Herbivore': 200, 'Carnivore': 50}
        self.def_specs = {'weight': {'max': 60, 'delta': 2},
                          'fitness': {'max': 1.0, 'delta': 0.05},
                          'age': {'max': 60, 'delta': 2}}
        self.age = dict()
        self.weight = dict()
        self.fitness = dict()

        self._img_base = img_base
        self._img_ctr = 0
        self._img_fmt = img_fmt

    def setup_graphics(self, nx_step, cmax_animals, hist_specs):
        """
        sets up a graphics interface with island map, heat maps, population graph and histograms


        :param nx_step: integer that adds to the current year to give the total amount of years to simulate
        :param cmax_animals: dictionary parameter that specifies the limits of heatmap values
        :param hist_specs: dictionary parameter that specifies the limits of histogram values
        """
        self.n_steps += nx_step
        rgb_value = {'W': (0, 0.5, 1),
                     'D': (1, 1, 0.3),
                     'H': (0, 0.6, 0),
                     'L': (0, 0.3, 0)}

        if self.fig is None:
            self.fig = plt.figure(figsize=(10, 10))

        if self.island_map_ax is None:
            self.island_map_ax = self.fig.add_axes([0.1, 0.55, 0.3, 0.45])
            self.island_map_ax.title.set_text("Island Map")
            self.island_map = self.island_map_ax.imshow(self.rgb_map)
            self.island_map_ax.set_xticks(range(len(self.rgb_map[0])))
            self.island_map_ax.set_xticklabels([_ + 1 if not (_ + 1) % 5 else '' for _ in range(len(self.rgb_map[0]))])
            self.island_map_ax.set_yticks(range(len(self.rgb_map)))
            self.island_map_ax.set_yticklabels([_ + 1 if not (_ + 1) % 5 else '' for _ in range(len(self.rgb_map))])

        if self.leg_ax is None:
            self.leg_ax = self.fig.add_axes([0.45, 0.7, 0.1, 0.2])
            self.leg_ax.axis('off')
            for ix, name in enumerate(('Water', 'Lowland', 'Highland', 'Desert')):
                self.leg_ax.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1, facecolor=rgb_value[name[0]]))
                self.leg_ax.text(0.35, ix * 0.2, name, transform=self.leg_ax.transAxes)

        if self.heatmap_ax is None:
            self.heatmap_ax = self.fig.add_axes([0.6, 0.75, 0.3, 0.15])
            self.heatmap_ax.title.set_text("Herbivore Heatmap")
            self.img_ax = None

        if self.heatmap2_ax is None:
            self.heatmap2_ax = self.fig.add_axes([0.6, 0.55, 0.3, 0.15])
            self.heatmap2_ax.title.set_text("Carnivore Heatmap")
            self.img2_ax = None

        if self.pop is None:
            self.pop = self.fig.add_axes([0.1, 0.1, 0.4, 0.4])
            self.pop.title.set_text("Population Graph")

        self.pop.set_xlim(0, self.n_steps + 1)

        for species in self.n:
            if self.n[species] is None:
                self.n[species], = self.pop.plot(np.arange(self.n_steps),
                                                 np.full(self.n_steps, np.nan),
                                                 color=self.meta_data[species]["colour"],
                                                 label=species)
            else:
                hx_data, hy_data = self.n[species].get_data()
                hx_new = np.arange(hx_data[-1] + 1, self.n_steps)
                if len(hx_new) > 0:
                    hy_new = np.full(hx_new.shape, np.nan)
                    self.n[species].set_data(np.hstack((hx_data, hx_new)),
                                             np.hstack((hy_data, hy_new)))
        self.pop.legend()

        if cmax_animals:
            for keys in ['Herbivore', 'Carnivore']:
                if cmax_animals.get(keys):
                    self.def_cmax[keys] = cmax_animals[keys]

        if hist_specs:
            for keys in ['age', 'weight', 'fitness']:
                if hist_specs.get(keys):
                    self.def_specs[keys] = hist_specs[keys]

        if self.histogram_age is None:
            self.histogram_age = self.fig.add_axes([0.55, 0.40, 0.35, 0.1])

        if self.histogram_weight is None:
            self.histogram_weight = self.fig.add_axes([0.55, 0.25, 0.35, 0.1])

        if self.histogram_fitness is None:
            self.histogram_fitness = self.fig.add_axes([0.55, 0.1, 0.35, 0.1])
        if self.axt is None:
            self.axt = self.fig.add_axes([0.4, 0.8, 0.2, 0.2])
            self.axt.cla()
            self.axt.axis('off')  # turn off coordinate system
            self.year = self.axt.text(0.5, 0.5, 'Year: {:5}'.format(0),
                                horizontalalignment='center',
                                verticalalignment='center',
                                transform=self.axt.transAxes)  # relative coordinates

        plt.pause(1e-6)  # pause required to make figure visible

        plt.ion()

    def pop_handler(self, current_year, n_species):
        """
        Method for specifically handling the population graph and updating the year counter


        :param current_year: integer that updates the current year
        :param n_species: dictionary containing population count for each species
        """
        for species in n_species:
            self.count[species] = n_species[species]

        self.year_current = current_year
        for species in self.n:
            data = self.n[species].get_ydata()
            data[self.year_current] = self.count[species]
            self.n[species].set_ydata(data)

    def update_histograms(self):
        """
        Updates the histograms on the graphics interface
        """
        self.histogram_age.cla()
        self.histogram_age.set_xlim(0, self.def_specs['age']['max'])
        # self.histogram_age.set_ylim(0, 2000)
        for species in self.weight:
            self.histogram_age.hist(self.age[species],
                                    bins=int((self.def_specs['age']['max']) / (self.def_specs['age']['delta'])),
                                    histtype='step',
                                    range=(0, self.def_specs['age']['max']),
                                    color=self.meta_data[species]["colour"])
        self.histogram_age.title.set_text("Age Distribution")

        self.histogram_weight.cla()
        self.histogram_weight.set_xlim(0, self.def_specs['weight']['max'])
        # self.histogram_weight.set_ylim(0, 3000 )
        for species in self.weight:
            self.histogram_weight.hist(self.weight[species],
                                       bins=int(
                                           (self.def_specs['weight']['max']) / (self.def_specs['weight']['delta'])),
                                       range=(0, self.def_specs['weight']['max']),
                                       histtype='step',
                                       color=self.meta_data[species]["colour"])
        self.histogram_weight.title.set_text("Weight Distribution")

        self.histogram_fitness.cla()
        self.histogram_fitness.set_xlim(0, self.def_specs['fitness']['max'])
        # self.histogram_fitness.set_ylim(0, 2000 )
        for species in self.weight:
            self.histogram_fitness.hist(self.fitness[species],
                                        bins=int(
                                            (self.def_specs['fitness']['max']) / (self.def_specs['fitness']['delta'])),
                                        histtype='step',
                                        range=(0, self.def_specs['fitness']['max']),
                                        color=self.meta_data[species]["colour"])
        self.histogram_fitness.title.set_text("Fitness Distribution")

    def update_heatmaps(self, cells_map):
        """
        Updates the heatmaps on the graphics interface


        :param cells_map: dictionary containing for each species
                          containing 2d arrays for the population count in each cell
        """
        if self.img_ax is not None:
            self.img_ax.set_data(cells_map["Herbivore"])
        else:
            self.img_ax = self.heatmap_ax.imshow(cells_map["Herbivore"], interpolation='nearest',
                                                 vmin=0, vmax=self.def_cmax['Herbivore'])
            plt.colorbar(self.img_ax, ax=self.heatmap_ax, orientation='vertical')

        if self.img2_ax is not None:
            self.img2_ax.set_data(cells_map["Carnivore"])
        else:
            self.img2_ax = self.heatmap2_ax.imshow(cells_map["Carnivore"], interpolation='nearest',
                                                   vmin=0, vmax=self.def_cmax['Carnivore'])
            plt.colorbar(self.img2_ax, ax=self.heatmap2_ax, orientation='vertical')

    def update_graphics(self, cells_map):
        """
        Updates the graphics interface with new data and shows it live


        :param cells_map: dictionary containing for each species
                          containing 2d arrays for the population count in each cell
        """
        self.year.set_text('Year:{:5}'.format(self.year_current))

        if not self.y_set_lim:
            if self.y_def_lim <= max(self.count['Herbivore'], self.count['Carnivore']):
                self.y_def_lim = max(self.count['Herbivore'], self.count['Carnivore'])
        else:
            self.y_def_lim = self.y_set_lim - 1000

        self.pop.set_ylim(0, self.y_def_lim + 1000)

        self.update_histograms()

        self.update_heatmaps(cells_map)

        self.fig.canvas.flush_events()
        plt.pause(1e-6)

    def update_data(self, n_species: dict, l_ages, l_weights, l_fitness):
        """
        Updates the histogram data and limits the data outside the ranges to display as maximum


        :param n_species: dictionary containing the types of species
        :param l_ages: dictionary containing data for ages for each species
        :param l_weights: dictionary containing data for weights for each species
        :param l_fitness: dictionary containing data for fitness for each species
        """
        for species in n_species:
            self.age[species] = [a if a < self.def_specs['age']['max'] else
                                 self.def_specs['age']['max'] for a in l_ages[species]]
            self.weight[species] = [w if w < self.def_specs['weight']['max'] else
                                    self.def_specs['weight']['max'] for w in l_weights[species]]
            self.fitness[species] = [f if f < self.def_specs['fitness']['max'] else
                                     self.def_specs['fitness']['max'] for f in l_fitness[species]]

    def convert_map(self, map_str: str):
        """
        Converts a given map string into a usable display


        :param map_str: String with W, D, H, L letters to specify cell type display
        """
        rgb_value = {'W': (0, 0.5, 1),
                     'D': (1, 1, 0.3),
                     'H': (0, 0.6, 0),
                     'L': (0, 0.3, 0)}

        self.rgb_map = [[rgb_value[column] for column in row]
                        for row in map_str.split()]

    def create_images(self):
        """
        saves images to file and creates directory if one doesn't exist
        """
        if self._img_base is None:
            return

        if not os.path.exists('../data'):
            os.makedirs('../data')

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1


def inner_points(p: iter):
    """
    finds a small sample of inner point limited by the volum made from points p.

    :param iter[tuple[float,float,float]] p: point that containes a volume.
    :return: a set of inner points.
    """
    r = []
    for a in p:
        for b in (q for q in p if q != a):
            r.append( ( (a[0]+b[0])/2 , (a[1]+b[1])/2 , (a[2]+b[2])/2 ) )
    return set(r)
