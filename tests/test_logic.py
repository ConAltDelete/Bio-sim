from biosim.logic import *
from biosim.simulation import BioSim


def test_migrasion_consistensy_one_animal():
    length = 30
    this_fucking_thing = BioSim(island_map="WWWW\nWllW\nwwww".upper(), seed=1234,
                                ini_pop=[{"loc": (2, 2), "pop": [{'species': 'herbevore', 'age': 5, 'weight': 100} for _ in range(length)]}])
    the_map = this_fucking_thing.island
    illigal_moves = this_fucking_thing.illigal_coord
    for _ in range(30):
        season_migration(the_map, illigal_moves)
    total_in_map = 0
    for cell in the_map:
        total_in_map += len(the_map[cell].herb_default)
    assert total_in_map == length


def test_migrasion_consistensy_two_animals():
    length = 5
    ini_herb = [{'species': 'herbevore',
                 'age': 5,
                 'weight': 100} for _ in range(length)]
    ini_carn = [{'species': 'carnivore',
                 'age': 5,
                 'weight': 100} for _ in range(length)]
    ini_pop = ini_herb + ini_carn
    fin_pop = [{"loc": (2, 2), "pop": ini_pop}]
    this_fucking_thing = BioSim(
        island_map="WWWW\nWLLW\nWWWW", seed=1234, ini_pop=fin_pop)
    the_map = this_fucking_thing.island
    illigal_moves = this_fucking_thing.illigal_coord
    for _ in range(30):
        season_migration(the_map, illigal_moves)
    total_in_map_herb = 0
    total_in_map_carn = 0
    for cell in the_map:
        total_in_map_herb += len(the_map[cell].herb_default)
        total_in_map_carn += len(the_map[cell].carn_default)
    assert total_in_map_herb == length
    assert total_in_map_carn == length

def test_eating_one_animal():
    pass