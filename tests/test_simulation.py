from biosim.simulation import BioSim
import pytest as pt

def test_consistensy_simulation_one_cell_one_species():
	sim = BioSim(island_map="WWW\nWLW\nWWW",ini_pop=[{
		"loc":(2,2),
		"pop":[
			{
		"species": "Herbivore",
		"age": 5,
		"weight": 20} for _ in range(100)]
	}])
	sim.simulate(num_years=200,vis_years=500)
	n_animals = len(sim.island[(2,2)].default["Herbivore"])
	assert n_animals == pt.approx(200,abs=25)

def test_consistensy_simulation_one_cell_two_species():
	ini_herb = [
			{
		"species": "Herbivore",
		"age": 5,
		"weight": 20} for _ in range(100)]
	ini_carn = [{"species": "Carnivore",
		"age": 5,
		"weight": 20} for _ in range(20)]
	ini_pop = [{"loc":(2,2),"pop":ini_carn + ini_herb}]
	sim = BioSim(island_map="WWW\nWLW\nWWW",ini_pop=ini_pop)
	sim.simulate(num_years=300,vis_years=500)
	n_herb = len(sim.island[(2,2)].default["Herbivore"])
	n_carn = len(sim.island[(2,2)].default["Carnivore"])
	assert n_herb == pt.approx(85,abs=17)
	assert n_carn == pt.approx(41, abs=1)