from random import seed
from biosim.simulation import BioSim
import pytest as pt

def test_consistensy_simulation_one_cell_one_species():
	n_animals = 0
	for _ in range(50):
		sim = BioSim(island_map="WWW\nWLW\nWWW",ini_pop=[{
		"loc":(2,2),
		"pop":[
			{
		"species": "Herbivore",
		"age": 5,
		"weight": 20} for _ in range(100)]
	}],tmean=True)
		sim.simulate(num_years=200,vis_years=None)
		n_animals += sim.mean["Herbivore"]
	assert n_animals/50 == pt.approx(200,abs=25)

def test_consistensy_simulation_one_cell_two_species():
	ini_herb = [
			{
		"species": "Herbivore",
		"age": 5,
		"weight": 20} for _ in range(100)]
	ini_carn = [{"species": "Carnivore",
		"age": 5,
		"weight": 20} for _ in range(20)]
	ini_pop = [{"loc":(2,2),"pop":ini_herb}]
	n_herb = 0
	n_carn = 0
	for _ in range(1,51):
		sim = BioSim(island_map="WWW\nWLW\nWWW",ini_pop=ini_pop,tmean=True)
		sim.simulate(num_years=50,vis_years=1)
		sim.add_population([{"loc":(2,2),"pop":ini_carn}])
		sim.simulate(num_years=150,vis_years=1)
		n_herb += sim.mean["Herbivore"]
		n_carn += sim.mean["Carnivore"]
	n_herb /= 50
	n_carn /= 50
	assert n_herb == pt.approx(85, abs=17)
	assert n_carn == pt.approx(41, abs=10)

def test_wrong_placement():
	with pt.raises(ValueError):
		BioSim(island_map="WWW\nWWW\nWWW",ini_pop=[{
		"loc": (2,2),
		"pop":[
			{
				"species":"Herbivore",
				"age": 4,
				"weight": 100
			}
		]
	}])