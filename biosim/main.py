# -*- coding: utf-8 -*-

"""
"""

from biosim.simulation import *

cmax = {'Herbivore': 200, 'Carnivore': 50}
hist = {'weight': {'max': 30, 'delta': 2},
        'fitness': {'max': 1.0, 'delta': 0.05},
        'age': {'max': 60, 'delta': 2}}

if __name__ == "__main__":
    sim = BioSim(island_map="""\
               WWWWWWWWWWWWWWWWWWWWW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHLLLLLLLLLLLLWWW
               WHHHHHLLLDDLLLHLLLWWW
               WHHLLLLLDDDLLLHHHHWWW
               WWHHHHLLLDDLLLHWWWWWW
               WHHHLLLLLDDLLLLLLLWWW
               WHHHHLLLLDDLLLLWWWWWW
               WWHHHHLLLLLLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW""",ini_pop=[{
        "loc":(10, 9),
        "pop":[
            {
        "species": "Herbivore",
        "age": 5,
        "weight": 20} for _ in range(50)]
    }], img_base=None, ymax_animals=None, cmax_animals=None, hist_specs=None)
    sim.simulate(num_years=50,vis_years=1)
    sim.add_population(population=[
        {
            "loc":(10,9),
            "pop":[
                {
                    "species": "Carnivore",
                    "age": 5,
                    "weight": 20
                } for _ in range(20)
            ]
        }
    ])
    sim.print_random_name()
    sim.simulate(num_years=150, vis_years=1)
    sim.make_movie('mp4')
