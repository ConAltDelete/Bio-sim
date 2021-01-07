# -*- coding: utf-8 -*-

"""
"""

from island import Cells

import simulation 

def season_migration(cells: dict, illigal_moves: list):
    """
    Animals moves to desired location if possible.
    :param cells: dictonary with coordinats as key, and Cells objects as value
    :return:
    """
    moving_animals = {"herb":{},"pred":{}}
    for cell in cells.values():
        cell.migration(illigal_moves)
        for mov_herb in cell.herb_migrate:
            moving_animals["herb"][mov_herb.var["coord"]] = mov_herb
        for mov_carn in cell.carn_migrate:
            moving_animals["pred"][mov_carn.var["coord"]] = mov_carn

    # moving animals
    for mov_herb in moving_animals["herb"]:
        cells[mov_herb].herb_default.extend(moving_animals["herb"][mov_herb])
    for mov_pred in moving_animals["pred"]:
        cells[mov_pred].carn_default.extend(moving_animals["pred"][mov_pred])

if __name__ == "__main__":
    cells_dict, illigal_moves = simulation.BioSim(island_map = "WWWW\nWLLW\nWWWW", ini_pop = [{'loc':(2,2) , 'pop':[ {"species":"herbivore","age":5,"weight":20} ] } ] , seed = 1234)

