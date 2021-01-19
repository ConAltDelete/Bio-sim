# -*- coding: utf-8 -*-

"""
visuals.py handles the given map string into a functional map for simulation purposes
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, matshoemolsen@nmbu.no'

from .island import Cells


def find_border(x_length, y_length):
    """
    Creates a list of border coordinates based on a rectangle.

    Starting index is 1.


    :param x_length: length of x-axis
    :param y_length: length of y-axis
    :return: list of all border coordinates
    """
    fix_x_1: list = [(y + 1, 1) for y in range(y_length)]
    fix_x_end: list = [(y + 1, x_length) for y in range(y_length)]
    fix_y_1: list = [(1, x + 1) for x in range(x_length)]
    fix_y_end: list = [(y_length, x + 1) for x in range(x_length)]

    all_coord: list = fix_x_1 + fix_x_end + fix_y_1 + fix_y_end

    return all_coord


def string2map(map_str: str, names: list):
    """
    This file converts map to a readable map. This function considers the following tiles:
     - 'W': Water tile, it has the curious property of being inaccessible to all being.
     - 'D': Dessert: it contains no food for the ``Herbivore``.
     - 'H': Highland: its maximum food supply is less than ``Lowland``.
     - 'L': Lowland: its maximum food supply is greater than ``HighLand``.


    :param map_str: a string that represents the map.
    :param list names: a list of species names.
    :return: a new map, and illegal coordinates
    """
    map_list = [list(map_r) for map_r in map_str.split()]

    x_length = len(map_list[0])
    if any((len(row) != x_length for row in map_list)):
        raise ValueError("Inconsistent row length")

    standard_values = {"W": 0, "L": 3, "H": 2, "D": 1}
    border_coord = find_border(x_length, len(map_list))
    newer_map = {}
    illegal_coord = []
    for row in enumerate(map_list):
        for column in enumerate(row[1]):
            incoming_coord = (row[0] + 1, column[0] + 1)
            if column[1] != "W" and incoming_coord not in border_coord:
                if column[1] not in standard_values:
                    raise ValueError("'{}' is not a standard value, expected {}".format(column[1], standard_values))
                newer_map.update({incoming_coord: Cells(
                    standard_values[column[1]], list(incoming_coord), names)})
            else:
                if column[1] != "W" and incoming_coord in border_coord:
                    raise ValueError("expected 'W' on border, got {}".format(column[1]))
                newer_map.update({incoming_coord: Cells(
                    standard_values[column[1]], list(incoming_coord), names)})
                illegal_coord.append(incoming_coord)
    return [newer_map, illegal_coord]


def set_param(island, _type: str, parm: dict):
    """
    This function adjust the cells of a given type (_type) with parameters (parm)


    :param island: a list of cells
    :param str _type: a string witch is either 'L', 'H', 'D', 'W'
    :param parm: a Dict with param (f_max)
    """
    cell_types = {"W": 0, "L": 3, "H": 2, "D": 1}
    cell_type = cell_types[_type]
    for coord in island:
        if island[coord].type == cell_type:
            island[coord].f_max = float(parm["f_max"])
