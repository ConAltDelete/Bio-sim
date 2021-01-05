# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, matshoemolsen@nmbu.no'

from animal import *


class Cells:
    """
    The cells class
    """
    def __init__(self, food, coord=None):
        self.coord = coord if coord is not None else [0, 0]
        self.food = food
        self.n_herb = 0
        self.n_carn = 0

    def count_herb(self, list_herb):
        self.n_herb = len([h for h in list_herb if self.coord == h.coor])

    def count_carn(self, list_carn):
        self.n_carn = len([c for c in list_carn if self.coord == c.coor])


if __name__ == '__main__':
    list_herb = [herbavor(0, 8.0), herbavor(0, 8.0), herbavor(0, 8.0, [1, 0])]
    K = Cells(46346345)
    K.count_herb(list_herb)
    print(K.n_herb)