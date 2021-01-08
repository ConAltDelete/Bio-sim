# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, matshoemolsen@nmbu.no'

from biosim.animal import *


class Cells:
    """
    The cells class
    """
    defauld_food = {
        0: 0,
        1: 0,
        2: 300,
        3: 800
    }

    def __init__(self, cell_type, coord=None):
        self.coord = coord if coord is not None else [0, 0]
        self.food = 0.0
        self.n_herb = 0
        self.n_carn = 0
        self.type = cell_type
        self.f_max = Cells.defauld_food[self.type]
        self.herb_default = list()
        self.herb_migrate = list()
        self.carn_default = list()
        self.carn_migrate = list()

    def migration(self, illigal_moves):
        for H in self.herb_default:
            H.var["coord"] = list(self.coord)
            H.move(illigal_moves)
        for h in self.herb_default:
            if h.var["coord"] != self.coord:
                self.herb_migrate.append(h)
                self.herb_default.remove(h)

        for P in self.carn_default:
            P.var["coord"] = list(self.coord)
            P.move(illigal_moves)
        for p in self.herb_default:
            if p.var["coord"] != self.coord:
                self.herb_migrate.append(p)
                self.herb_default.remove(p)

    def count_herb(self):
        self.n_herb = len(self.herb_default) + len(self.herb_migrate)

    def count_carn(self):
        self.n_carn = len(self.carn_default) + len(self.carn_migrate)

    def fill_food(self, food):
        self.food = food

    def reduce_food(self, amount_eaten):
        self.food -= amount_eaten

    def combine_migrate(self):
        self.herb_default.extend(self.herb_migrate)
        self.herb_migrate = list()
        self.carn_default.extend(self.carn_migrate)
        self.herb_migrate = list()


if __name__ == '__main__':

    K = Cells(3)
    K.herb_default.extend(
        [herbavor(0, 8.0), herbavor(0, 8.0), herbavor(0, 8.0)])
    print(K.n_herb)
    K.count_herb()
    print(K.n_herb)
    K.herb_newborn.extend([herbavor(0, 8.0), herbavor(0, 8.0)])
    K.count_herb()
    print(K.n_herb)
    print(K.herb_default)
    print(K.herb_newborn)
    K.combine_newborn()
    print(K.herb_default)
    print(K.herb_newborn)
    K.count_herb()
    print(K.n_herb)
