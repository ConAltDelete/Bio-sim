# -*- coding: utf-8 -*-

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, matshoemolsen@nmbu.no'

from .animal import *


class Cells:
    """
    The ``Cells`` class keeps track of informasion of the cells on the island.
    """
    default_food = {
        0:0,
        1:0,
        2:300,
        3:800
    }
    def __init__(self, cell_type: int, coord=None, names: list = None):
        """
        :param int cell_type: Describes the cell type as an integer.
        :param list/None coord: Tells the cell where it is on the map. The default value is ``[0,0]``.
        """
        self.coord           = coord if coord is not None else [0, 0]
        self.count_species   = dict() if not(names) else {species:0 for species in names}
        self.count_age = dict()
        self.count_weight = dict()
        self.count_fitness = dict()
        self.type            = cell_type
        self.f_max           = float(Cells.default_food[self.type])
        self.food            = self.f_max
        self.default         = dict()
        self.migrate         = dict()

    def migration(self, illigal_moves):
        """
        Animals in the cell get the opertunity to move to
        another cell.


        :param list[tuple[int,int]] illigal_moves: a list of tuples with illigal cells
        """
        # We tell the animal to move to a resenable spot#
        for specis in self.default:
            for animal in self.default[specis]:
                animal.var["coord"] = list(self.coord)
                animal.move(illigal_moves)
        # Now we check if it moves, if it does we move it, else ignore it.#
        for specis in self.default:
            len_animal = len(self.default[specis])
            for _ in range(len_animal):
                animal = self.default[specis].pop(0)
                if tuple(animal.var["coord"]) != tuple(self.coord):
                    if specis in self.migrate:
                        self.migrate[specis].append(animal)
                    else:
                        self.migrate[specis] = [animal]
                else:
                    self.default[specis].insert(0,animal)

    def count(self):
        """
        Counts the number of animals in the cell.
        """
        self.count_age = {'Herbivore': [], 'Carnivore': []}
        self.count_weight = {'Herbivore': [], 'Carnivore': []}
        self.count_fitness = {'Herbivore': [], 'Carnivore': []}
        for spesis in self.default:
            self.count_species[spesis] = len(self.default[spesis])
            if len(self.default[spesis]) != 0:
                for animals in self.default[spesis]:
                    self.count_age[spesis].append(animals.var["a"])
                    self.count_weight[spesis].append(animals.var["w"])
                    self.count_fitness[spesis].append(animals.var["sigma"])


if __name__ == '__main__':
    pass
