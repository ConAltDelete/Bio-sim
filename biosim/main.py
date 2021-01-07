# -*- coding: utf-8 -*-

"""
"""

from island import Cells

import simulation 


if __name__ == "__main__":
    this_fucking_thing = simulation.BioSim(island_map = "WWWW\nWLLW\nWWWW", ini_pop = [{'loc':(2,2) , 'pop':[ {"species":"herbivore","age":5,"weight":20} for _ in range(5)] } ] , seed = 1234)
    the_map = this_fucking_thing.island
    illigal_moves = this_fucking_thing.illigal_coord
    for _ in range(3):
        season_migration(the_map,illigal_moves)
    for cell in the_map:
        print("coord:",the_map[cell].coord,"animals:",the_map[cell].herb_default)
