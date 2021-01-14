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
        "loc":(3,3),
        "pop":[
            {
        "species": "Herbivore",
        "age": 5,
        "weight": 20} for _ in range(200)]
    }])
    sim.set_animal_parameters("Herbivore",{
        'mu': 100,
        'omega': 0,
        'gamma': 0,
        'a_half': 1000})
    sim.set_animal_parameters("Carnivore",{
        'mu': 100,
        'omega': 0,
        'gamma': 0,
        'a_half': 1000})
    sim.simulate(num_years=50,vis_years=1)
    sim.add_population(population=[
        {
            "loc":(3,3),
            "pop":[
                {
                    "species": "Carnivore",
                    "age": 5,
                    "weight": 20
                } for _ in range(100)
            ]
        }
    ])
    sim.simulate(num_years=250,vis_years=1)
