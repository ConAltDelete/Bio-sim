# -*- coding: utf-8 -*-

"""
"""

from biosim.simulation import *

if __name__ == "__main__":
    sim = BioSim(island_map="WWWW\nWLLW\nWLLW\nWWWW",ini_pop=[{
        "loc":(2,2),
        "pop":[
            {
        "species": "Herbivore",
        "age": 5,
        "weight": 20} for _ in range(2)]
    }])
    sim.simulate(num_years=100,vis_years=1)
    sim.add_population(population=[
        {
            "loc":(2,2),
            "pop":[
                {
                    "species": "Carnivore",
                    "age": 5,
                    "weight": 20
                } for _ in range(5)
            ]
        }
    ])
    sim.simulate(num_years=100,vis_years=1)
