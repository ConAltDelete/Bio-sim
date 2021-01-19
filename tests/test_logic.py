from biosim.logic import *
from biosim.simulation import *

import pytest

@pytest.mark.parametrize("n",[n for n in range(1,6)])
def test_ageing_animals(n):
    length = 15
    the_map = """
        WWW
        WLW
        WWW
    """
    ini_herb = [{'species': 'Herbivore',
                 'age': 0,
                 'weight': 100} for _ in range(length)]
    ini_carn = [{'species': 'Carnivore',
                 'age': 0,
                 'weight': 100} for _ in range(length)]
    ini_pop = [{"loc":(2,2), "pop":ini_herb+ini_carn}]
    sim = BioSim(island_map=the_map, ini_pop=ini_pop)
    island = sim.island
    for cell in island:
        season_ageing(island[cell])
    for coord in island:
        for spesis in island[coord].default:
            check = [animal.var["a"] == 1 for animal in island[coord].default[spesis]]
            assert all(check)


def test_migrasion_consistensy_one_animal():
    length = 15
    this_fucking_thing = BioSim(island_map="WWWW\nWllW\nwllw\nWWWW".upper(), seed=1234,
                                ini_pop=[{"loc": (2, 2), "pop": [{'species': 'Herbivore', 'age': 5, 'weight': 100} for _ in range(length)]}])
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
    ini_herb = [{'species': 'Herbivore',
                 'age': 5,
                 'weight': 100} for _ in range(length)]
    ini_carn = [{'species': 'Carnivore',
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

def test_migrasion_one_species():
    length = 20
    this_fucking_thing = BioSim(island_map="WWWWW\nWLllW\nwlllw\nwlllw\nWWwWW".upper(), seed=1234,
                                ini_pop=[{"loc": (3, 3), "pop": [{'species': 'Herbivore', 'age': 5, 'weight': 100} for _ in range(length)]}])
    this_fucking_thing.set_animal_parameters("Herbivore",{
        'mu': 1,
        'omega': 0,
        'gamma': 0,
        'a_half': 1000})
    the_map = this_fucking_thing.island
    illigal_moves = this_fucking_thing.illigal_coord
    season_migration(the_map, illigal_moves)
    count_cells = dict()
    for cell in the_map:
        if "Herbivore" in the_map[cell].default:
            count_cells[cell] = len(the_map[cell].default["Herbivore"])
    antall_dyr = sum(count_cells.values())
    antall_celler = len(count_cells.keys())
    total = antall_dyr/antall_celler
    assert total == pytest.approx(5,1.4)

def test_migrasion_two_species():
    length = 20
    ini_herb = [{'species': 'Herbivore',
                 'age': 5,
                 'weight': 100} for _ in range(length)]
    ini_carn = [{'species': 'Carnivore',
                 'age': 5,
                 'weight': 100} for _ in range(length)]
    ini_pop = ini_herb + ini_carn
    fin_pop = [{"loc": (3, 3), "pop": ini_pop}]
    this_fucking_thing = BioSim(island_map="WWWWW\nWLllW\nwlllw\nwlllw\nWWwWW".upper(),
            ini_pop=fin_pop
                )
    this_fucking_thing.set_animal_parameters("Herbivore",{
        'mu': 1,
        'omega': 0,
        'gamma': 0,
        'a_half': 1000})
    this_fucking_thing.set_animal_parameters("Carnivore",{
        'mu': 1,
        'omega': 0,
        'gamma': 0,
        'a_half': 1000})
    the_map = this_fucking_thing.island
    illigal_moves = this_fucking_thing.illigal_coord
    season_migration(the_map, illigal_moves)
    count_cells = dict()
    for cell in the_map:
        if "Herbivore" in the_map[cell].default and len(the_map[cell].default["Herbivore"]) != 0:
            if cell not in count_cells:
                count_cells[cell] = len(the_map[cell].default["Herbivore"])
            else:
                count_cells[cell] += len(the_map[cell].default["Herbivore"])
        if "Carnivore" in the_map[cell].default and len(the_map[cell].default["Carnivore"]) != 0:
            if cell not in count_cells:
                count_cells[cell] = len(the_map[cell].default["Carnivore"])
            else:
                count_cells[cell] += len(the_map[cell].default["Carnivore"])
    antall_dyr = sum(count_cells.values())
    antall_celler = len(count_cells.keys())
    total = antall_dyr/antall_celler
    assert total == pytest.approx(10,rel=0.1)

def test_no_diagonal_movements():
    length = 20
    ini_herb = [{'species': 'Herbivore',
                 'age': 5,
                 'weight': 100} for _ in range(length)]
    ini_carn = [{'species': 'Carnivore',
                 'age': 5,
                 'weight': 100} for _ in range(length)]
    ini_pop = ini_herb + ini_carn
    fin_pop = [{"loc": (3, 3), "pop": ini_pop}]
    this_fucking_thing = BioSim(island_map="WWWWW\nWLllW\nwlllw\nwlllw\nWWwWW".upper(),
            ini_pop=fin_pop
                )
    this_fucking_thing.set_animal_parameters("Herbivore",{
        'mu': 100,
        'omega': 0,
        'gamma': 0,
        'a_half': 1000})
    this_fucking_thing.set_animal_parameters("Carnivore",{
        'mu': 100,
        'omega': 0,
        'gamma': 0,
        'a_half': 1000})
    the_map = this_fucking_thing.island
    illigal_moves = this_fucking_thing.illigal_coord
    season_migration(the_map,illigal_moves)
    count_cells = dict()
    for cell in the_map:
        if "Herbivore" in the_map[cell].default:
            if cell not in count_cells:
                count_cells[cell] = len(the_map[cell].default["Herbivore"])
            else:
                count_cells[cell] += len(the_map[cell].default["Herbivore"])
        if "Carnivore" in the_map[cell].default:
            if cell not in count_cells:
                count_cells[cell] = len(the_map[cell].default["Carnivore"])
            else:
                count_cells[cell] += len(the_map[cell].default["Carnivore"])
    not_expected = [(3,3),(2,2),(2,4),(4,2),(4,4)]
    for coord in not_expected:
        if coord in count_cells:
            count = count_cells[coord] == 0
            assert count

def test_no_diagonal_movements_two_iterations():
    length = 20
    ini_herb = [{'species': 'Herbivore',
                 'age': 5,
                 'weight': 100} for _ in range(length)]
    ini_carn = [{'species': 'Carnivore',
                 'age': 5,
                 'weight': 100} for _ in range(length)]
    ini_pop = ini_herb + ini_carn
    fin_pop = [{"loc": (4, 4), "pop": ini_pop}]
    this_fucking_thing = BioSim(island_map="WWWWWWW\nWLLLllW\nwLLlllw\nwlLLllw\nwlLLllw\nwlLLllw\nwwWWwWW".upper(),
            ini_pop=fin_pop
                )
    this_fucking_thing.set_animal_parameters("Herbivore",{
        'mu': 100,
        'omega': 0,
        'gamma': 0,
        'a_half': 1000})
    this_fucking_thing.set_animal_parameters("Carnivore",{
        'mu': 100,
        'omega': 0,
        'gamma': 0,
        'a_half': 1000})
    the_map = this_fucking_thing.island
    illigal_moves = this_fucking_thing.illigal_coord
    for _ in range(2):
        season_migration(the_map,illigal_moves)
    count_cells = dict()
    for cell in the_map:
        if "Herbivore" in the_map[cell].default:
            if cell not in count_cells:
                count_cells[cell] = len(the_map[cell].default["Herbivore"])
            else:
                count_cells[cell] += len(the_map[cell].default["Herbivore"])
        if "Carnivore" in the_map[cell].default:
            if cell not in count_cells:
                count_cells[cell] = len(the_map[cell].default["Carnivore"])
            else:
                count_cells[cell] += len(the_map[cell].default["Carnivore"])
    not_expected = [(3,4),(4,3),(4,5),(5,4)]
    for coord in not_expected:
        if coord in count_cells:
            count = count_cells[coord] == 0
            assert count

def test_eating_Herbivore():
    class cell:
        def __init__(self):
            self.food = 20

    a_cell = cell()
    herb = Herbivore(a= 5, w = 100)
    herb.eat(a_cell)
    assert a_cell.food == 10

def test_two_Herbivore_eating_in_cell():
    ini_herb = [ {'species': 'Herbivore',
                 'age': 5,
                 'weight': 100} for _ in range(2)]
    ini_pop = [{"loc":(2,2),"pop":ini_herb}]
    island_setup = BioSim(island_map="WWW\nWLW\nWWW", seed=1234, ini_pop=ini_pop)
    the_map = island_setup.island
    season_feeding(the_map[(2,2)])
    cell = the_map[(2,2)]
    assert cell.food == 780

def test_eating_carnevore():
    class herb_test:
        def __init__(self):
            self.default = {"Herbivore":[Herbivore(a=1,w=1)]}
    herd = herb_test()
    pred = Carnivore(a=5,w=100)
    pred.var["phi"] = 20
    pred.eat(herd)
    assert list(herd.default["Herbivore"]) == []

def test_weight_loss():
    sim = BioSim(island_map="""WWW\nWLW\nWWW""", ini_pop=[{
        "loc":(2,2),
        "pop": [
            {
                "species": "Herbivore",
                'age': 5,
                'weight': 20

            } for _ in range(20)
        ]
    }])
    island = sim.island
    for cell in island:
        season_ageing(island[cell])
    for coord in island:
        for spesis in island[coord].default:
            check = [animal.var["w"] == 19 for animal in island[coord].default[spesis]]
            assert all(check)

def test_season_end():
    sim = BioSim(island_map="WWW\nWLW\nWWW",ini_pop=[])
    sim.island[(2,2)].food = 0
    island = sim.island
    season_end(island)
    assert island[(2,2)].food == island[(2,2)].f_max

def test_birth_one_animal():
    ini_herb = [ {'species': 'Herbivore',
                 'age': 5,
                 'weight': 100} for _ in range(1)]
    island_setup = BioSim(island_map="WWW\nWLW\nWWW", seed=1234, ini_pop=[])
    island_setup.set_animal_parameters("Herbivore",{"gamma":100})
    ini_pop = [{"loc":(2,2),"pop":ini_herb}]
    island_setup.add_population(population=ini_pop)
    the_map = island_setup.island
    season_breeding(the_map[(2,2)])
    cell = the_map[(2,2)]
    assert len(cell.default["Herbivore"]) == 1

@pytest.mark.parametrize("n_animals",[n for n in range(2,9)])
def test_birth_two_animals(n_animals):
    ini_herb = [ {'species': 'Herbivore',
                 'age': 5,
                 'weight': 100} for _ in range(n_animals)]
    island_setup = BioSim(island_map="WWW\nWLW\nWWW", seed=1234, ini_pop=[])
    island_setup.set_animal_parameters("Herbivore",{"gamma":1000})
    ini_pop = [{"loc":(2,2),"pop":ini_herb}]
    island_setup.add_population(population=ini_pop)
    the_map = island_setup.island
    season_breeding(the_map[(2,2)])
    cell = the_map[(2,2)]
    assert len(cell.default["Herbivore"]) == 2*n_animals

def test_death_one_animal():
    herb = Herbivore(a=5,w=0)
    herb.death()
    assert not(herb.var["life"])

@pytest.mark.parametrize("n_animals",[n for n in range(2,6)])
def test_death_multi_animal(n_animals):
    ini_pop = [{
        "loc": (2,2),
        "pop": [
            {
                "species": "Herbivore",
                "age": 5,
                "weight": 0
            } for _ in range(n_animals)
        ]
        }
    ]
    sim = BioSim("WWW\nWLW\nWWW",ini_pop=ini_pop)
    the_map = sim.island
    season_ageing(the_map[(2,2)])
    assert len(the_map[(2,2)].default["Herbivore"]) == 0

@pytest.mark.parametrize("n_carn",[n for n in range(2,6)])
@pytest.mark.parametrize("n_herb",[n for n in range(2,6)])
def test_death_multi_specis(n_herb,n_carn):
    ini_herb = [
            {
                "species": "Herbivore",
                "age": 5,
                "weight": 0
            } for _ in range(n_herb)
        ]

    ini_carn = [
        {
                "species": "Carnivore",
                "age": 5,
                "weight": 0
            } for _ in range(n_carn)
    ]

    ini_pop = [
        {
            "loc": (2,2),
            "pop": ini_herb + ini_carn
        }
    ]
    sim = BioSim("WWW\nWLW\nWWW",ini_pop=ini_pop)
    the_map = sim.island
    season_ageing(the_map[(2,2)])
    assert len(the_map[(2,2)].default["Herbivore"]) == 0 and len(the_map[(2,2)].default["Carnivore"]) == 0