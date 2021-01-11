from biosim.simulation import BioSim
import pytest as pt

def test_consistensy_simulation_one_cell_one_species():
	sim = BioSim(island_map="WWW\nWLW\nWWW",ini_pop=[{
		"loc":(2,2),
		"pop":[
			{
		"species": "Herbivore",
		"age": 5,
		"weight": 20} for _ in range(2)]
	}])
	sim.simulate(num_years=200,vis_years=1)
	n_animals = len(sim.island[(2,2)].default["Herbivore"])
	assert n_animals == pt.approx(200,abs=25)
