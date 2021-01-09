# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, matshoemolsen@nmbu.no'

from .animal import *


class Cells:
    """
    The cells class
    """
    default_food = {
        0:0,
        1:0,
        2:300,
        3:800
    }
    def __init__(self, cell_type, coord=None):
        self.coord   = coord if coord is not None else [0, 0]
        self.food    = 0.0
        self.count   = dict()
        self.type    = cell_type
        self.f_max   = Cells.default_food[self.type]
        self.default = dict()
        self.migrate = dict()
        self.newborn = dict()
        self.eaten   = dict()

    def migration(self, illigal_moves):
        """
        Animals in the cell get the opertunity to move to
        another cell.
        :param illigal_moves: a list of tuples with illigal cells
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
        We count the number of animals in cell.
        """
        self.count = 0
        for spesis in self.default:
            self.count += len(self.default[spesis])
        for spesis in self.newborn:
            self.count += len(self.newborn[spesis])
        for spesis in self.migrate:
            self.count += len(self.migrate[spesis])

    def fill_food(self, food):
        self.food = food

    def reduce_food(self, amount_eaten):
        self.food -= amount_eaten

    def combine_newborn(self):
        for spesis in self.newborn:
            self.default[spesis].extend(self.newborn[spesis])
            self.newborn[spesis] = list()

    def combine_migrate(self):
        for spesis in self.migrate:
            self.default[spesis].extend(self.migrate[spesis])
            self.migrate[spesis] = list()

    def combine_eaten(self):
        for spesis in self.eaten:
            self.default[spesis].extend(self.eaten[spesis])
            self.eaten[spesis] = list()


if __name__ == '__main__':
    pass