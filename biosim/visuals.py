# -*- coding: utf-8 -*-

"""
This file handels visuals.
"""

from .island import Cells

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'


def string2map(map_str: str):
    """
    This file converts map to a readable map.
    Assumes class 'Cells' handels strings at __init__.
    :param map_str: a string that represents the map.
    :return: a new map, and illigal coordinates
    """
    map_list = [list(map_r) for map_r in map_str.split()]

    x_length = len(map_list[0])
    for row in map_list:
        if len(row) != x_length:
            raise ValueError("Inconsistent row lenght")

    standard_values = {"W": 0, "L": 3, "H": 2, "D": 1}
    new_map = {}
    illigal_coord = []
    for row in enumerate(map_list):
        for colum in enumerate(row[1]):
            if colum[1] != "W":
                if colum[1] not in standard_values:
                    raise ValueError("'{}' is not a standard value, expected {}".format(colum[1],standard_values))
                new_map.update({(colum[0] + 1, row[0] + 1): Cells(
                    standard_values[colum[1]], [colum[0] + 1, row[0] + 1])})
            else:
                illigal_coord.append((colum[0] + 1, row[0] + 1))
    return [new_map, illigal_coord]


def set_param(island, _type: str, parm: dict):
    """
    This function adjust the cells of a given type (_type) with paramaters (parm)
    :param _type: a string witch is either 'L', 'H', 'D', 'W'
    :param parm: a Dict with param (f_max)
    """
    Cell_type = {"W": 0, "L": 3, "H": 2, "D": 1}
    Cell_type = Cell_type[_type]
    for c in (C for C in island if C.type == Cell_type):
        c.f_max = parm["f_max"]


if __name__ == '__main__':
    map_test = "WWWWW\nWWLLW\nWWWWW"
    new_map = string2map(map_test)[0]
    print(new_map)
    for cells in new_map:
        for c in cells.values():
            print(c.type)
