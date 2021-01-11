# -*- coding: utf-8 -*-

"""
"""

from biosim.simulation import *

if __name__ == "__main__":
    sim = BioSim(island_map="WWW\nWLW\nWWW",ini_pop=[{
        "loc":(2,2),
        "pop":[
            {
        "species": "Herbivore",
        "age": 5,
        "weight": 100} for _ in range(2)]
    }])
    sim.simulate(num_years=100,vis_years=1)
    sim.simulate(num_years=100,vis_years=1)
