# -*- coding: utf-8 -*-

"""
"""

from biosim.simulation import *
import textwrap

if __name__ == "__main__":
    geogr = """\
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
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)
    sim = BioSim(island_map=geogr,ini_pop=[{
        "loc":(10,9),
        "pop":[
            {
        "species": "Herbivore",
        "age": 5,
        "weight": 20} for _ in range(200)]
    }])
    sim.simulate(num_years=50,vis_years=1)
    
    sim.add_population(population=[
        {
            "loc":(10,9),
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
