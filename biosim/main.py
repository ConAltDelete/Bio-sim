# -*- coding: utf-8 -*-

"""
"""

from biosim.simulation import *

if __name__ == "__main__":
    sim = BioSim(island_map=""" WWWWW
                                WLLLW
                                WLLLW
                                WLLLW
                                WWWWW""",ini_pop=[{
        "loc":(2,2),
        "pop":[
            {
        "species": "Herbivore",
        "age": 5,
        "weight": 20} for _ in range(10)]
    }])
    sim.simulate(num_years=50,vis_years=500)
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
    sim.simulate(num_years=250,vis_years=500)
