# -*- coding: utf-8 -*-

"""
This file handels visuals.
"""

from island import Cells

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'

def string2map(map_str : str):
    """
    This file converts map to a readable map.
    Assumes class 'Cells' handels strings at __init__.
    :param map_str: a string that represents the map.
    """
    map_list = [list(map_r) for map_r in map_str.split()]
    new_map = []
    for row in enumerate( map_list ):
        for colum in enumerate( row[1] ):
            if colum[1] != "W":
                new_map.append( { ( colum[0] + 1, row[0] + 1) : Cells({"W":0,"L":3,"H":2,"D":1}[colum[1]],[colum[0] + 1, row[0] + 1] ) } )
    return new_map

def set_param(island,_type : str, parm : dict):
    """
    This function adjust the cells of a given type (_type) with paramaters (parm)
    :param _type: a string witch is either 'L', 'H', 'D', 'W'
    :param parm: a Dict with param (f_max)
    """
    Cell_type = {"W":0,"L":3,"H":2,"D":1}
    Cell_type = Cell_type[_type]
    for c in (C for C in island if C.type == Cell_type):
        c.f_max = parm["f_max"]


if __name__ == '__main__':
    map_test = "WWWWW\nWWLLW\nWWWWW"
    new_map = string2map(map_test)
    print(new_map)
    for cells in new_map:
        for c in cells.values():
            print(c.type)
