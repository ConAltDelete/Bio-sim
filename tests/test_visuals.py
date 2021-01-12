from biosim.visuals import *
from biosim.simulation import BioSim

import pytest

@pytest.mark.parametrize("valid_cells",['L','D','W','H'])
def test_single_cell(valid_cells):
	string2map("WWW\nW{}W\nWWW".format(valid_cells))

@pytest.mark.parametrize("invalid_cells",[ascii(n) for n in range(65,91) if n not in [76,72,68,87]])
def test_single_invalid_cell(invalid_cells):
	with pytest.raises(ValueError):
		string2map("WWW\nW{}W\nWWW".format(invalid_cells))

def test_set_param_on_single_animal():
	island_setup = BioSim(island_map="WWW\nWLW\nWWW", seed=1234, ini_pop=[])
	island_setup.set_animal_parameters("Herbivore",{
		"beta":20,
		"gamma":100
		})
	island_setup.add_population([ {"loc":(2,2),"pop": [{'species': 'Herbivore',
				 'age': 5,
				 'weight': 100} for _ in range(1)] } ] )
	animal = island_setup.island[(2,2)].default["Herbivore"][0]
	assert animal.var["beta"] == 20 and animal.var["gamma"] == 100

def test_set_param_more_animals():
	island_setup = BioSim(island_map="WWW\nWLW\nWWW", seed=1234, ini_pop=[])
	island_setup.set_animal_parameters("Herbivore",{
		"beta":20,
		"gamma":100
		})
	island_setup.set_animal_parameters("Carnivore",{
		"eta":20,
		"a_half":100
	})
	island_setup.add_population([ {"loc":(2,2),"pop": [{'species': 'Herbivore',
				 'age': 5,
				 'weight': 100},{
					 'species': 'Carnivore',
				 'age': 5,
				 'weight': 100
				 } ] } ] )
	herb = island_setup.island[(2,2)].default["Herbivore"][0]
	carn = island_setup.island[(2,2)].default["Carnivore"][0]
	assert herb.var["beta"] == 20 and herb.var["gamma"] == 100
	assert carn.var["eta"] == 20 and carn.var["a_half"] == 100

def test_illigal_border():
	coords = find_border(2,2)
	expected = [(1,1),(1,2),(2,1),(2,2)]
	for coord in coords:
		assert coord in expected

def test_border_not_center():
	coords = find_border(3,3)
	expected = [(2,2)]
	for coord in coords:
		assert coord not in expected