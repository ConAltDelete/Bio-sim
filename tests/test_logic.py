from biosim.logic import *
from biosim.simulation import BioSim


def test_migrasion_consistensy_one_animal():
    length = 15
    this_fucking_thing = BioSim(island_map="WWWW\nWllW\nwllw\nWWWW".upper(), seed=1234,
                                ini_pop=[{"loc": (2, 2), "pop": [{'species': 'herbivore', 'age': 5, 'weight': 100} for _ in range(length)]}])
    the_map = this_fucking_thing.island
    illigal_moves = this_fucking_thing.illigal_coord
    for _ in range(30):
        season_migration(the_map, illigal_moves)
    total_in_map = 0
    for cell in the_map:
        for specis in the_map[cell].default:
            total_in_map += len(the_map[cell].default[specis])
    assert total_in_map == length


def test_migrasion_consistensy_two_animals():
    length = 15
    ini_herb = [{'species': 'herbivore',
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
    total_in_map = 0
    for cell in the_map:
        for specis in the_map[cell].default:
            total_in_map += len(the_map[cell].default[specis])
    assert total_in_map == 2*length

def test_eating_herbivore():
    herb = herbivore(a= 5, w = 100)
    eaten = herb.eat(100,return_food=True)
    assert eaten == 10

def test_two_herbivore_eating_in_cell():
    ini_herb = [ {'species': 'herbivore',
                 'age': 5,
                 'weight': 100} for _ in range(2)]
    ini_pop = [{"loc":(2,2),"pop":ini_herb}]
    island_setup = BioSim(island_map="WWW\nWLW\nWWW", seed=1234, ini_pop=ini_pop)
    the_map = island_setup.island
    season_feeding(the_map[(2,2)])
    cell = the_map[(2,2)]
    assert cell.food == 780

def test_eating_carnevore():
    herd = [herbivore(a=1,w=1)]
    pred = carnivore(a=5,w=100)
    pred.var["sigma"] = 20
    herd = pred.eat(herd)
    assert herd == []

def test_birth_one_animal():
    ini_herb = [ {'species': 'herbivore',
                 'age': 5,
                 'weight': 100} for _ in range(1)]
    island_setup = BioSim(island_map="WWW\nWLW\nWWW", seed=1234, ini_pop=[])
    island_setup.set_animal_parameters("herbivore",{"gamma":100})
    ini_pop = [{"loc":(2,2),"pop":ini_herb}]
    island_setup.add_population(population=ini_pop)
    the_map = island_setup.island
    season_breeding(the_map[(2,2)])
    cell = the_map[(2,2)]
    assert len(cell.default["herbivore"]) == 1

def test_birth_two_animals():
    ini_herb = [ {'species': 'herbivore',
                 'age': 5,
                 'weight': 100} for _ in range(2)]
    island_setup = BioSim(island_map="WWW\nWLW\nWWW", seed=1234, ini_pop=[])
    island_setup.set_animal_parameters("herbivore",{"gamma":100})
    ini_pop = [{"loc":(2,2),"pop":ini_herb}]
    island_setup.add_population(population=ini_pop)
    the_map = island_setup.island
    season_breeding(the_map[(2,2)])
    cell = the_map[(2,2)]
    assert len(cell.default["herbivore"]) == 4