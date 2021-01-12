# -*- coding: utf-8 -*-

"""
This file handels visuals.
"""

from .island import Cells

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'

def find_border(x_length,y_length):
    """
    Creates a list of border coordinates based on a rectangle.
    :param x_lenght: lenght of x-axis
    :param x_lenght: lenght of y-axis
    :return: list of all border coordinates
    """
    fix_x_1: list = [(y+1,1) for y in range(y_length)]
    fix_x_end: list = [(y+1,x_length) for y in range(y_length)]
    fix_y_1: list = [(1,x+1) for x in range(x_length)]
    fix_y_end: list = [(y_length,x+1) for x in range(x_length)]

    all_coord: list = fix_x_1 + fix_x_end + fix_y_1 + fix_y_end

    return all_coord

def string2map(map_str: str):
    """
    This file converts map to a readable map.
    Assumes class 'Cells' handels strings at __init__.
    :param map_str: a string that represents the map.
    :return: a new map, and illigal coordinates
    """
    map_list = [list(map_r) for map_r in map_str.split()]

    x_length = len(map_list[0])
    if any( ( len(row) != x_length for row in map_list ) ):
        raise ValueError("Inconsistent row lenght")
    
    standard_values = {"W": 0, "L": 3, "H": 2, "D": 1}
    border_coord = find_border(x_length,len(map_list))
    new_map = {}
    illigal_coord = []
    for row in enumerate(map_list):
        for colum in enumerate(row[1]):
            incomming_coord = (row[0] + 1, colum[0] + 1)
            if colum[1] != "W" and incomming_coord not in border_coord:
                if colum[1] not in standard_values:
                    raise ValueError("'{}' is not a standard value, expected {}".format(colum[1],standard_values))
                new_map.update({incomming_coord: Cells(
                    standard_values[colum[1]], list(incomming_coord))})
            else:
                if colum[1] != "W" and incomming_coord in border_coord:
                    raise ValueError("excpected 'W', got {}".format(colum[1]))
                illigal_coord.append(incomming_coord)
    return [new_map, illigal_coord]


def set_param(island, _type: str, parm: dict):
    """
    This function adjust the cells of a given type (_type) with paramaters (parm)
    :param _type: a string witch is either 'L', 'H', 'D', 'W'
    :param parm: a Dict with param (f_max)
    """
    Cell_types = {"W": 0, "L": 3, "H": 2, "D": 1}
    Cell_type = Cell_types[_type]
    for coord in island:
        if island[coord].type == Cell_type:
            island[coord].f_max = parm["f_max"]


if __name__ == '__main__':
    map_test = "WWWWW\nWWLLW\nWWWWW"
    new_map = string2map(map_test)[0]
    print(new_map)
    for cells in new_map:
        for c in cells.values():
            print(c.type)
