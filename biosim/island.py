# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, matshoemolsen@nmbu.no'


class Cells:
    """
    The cells class
    """
    def __init__(self, food, coord=None):
        self.coord = coord if coord is not None else [0, 0]
        self.food = food
        self.n_herb = self.count_herb()
        self.n_carn = self.count_carn()

    def count_herb(self):
        pass

    def count_carn(self):
        pass


if __name__ == '__main__':
    pass
