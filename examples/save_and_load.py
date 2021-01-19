from biosim.simulation import BioSim, load

the_map = "WWW\nWLW\nWWW"

ini_pop = [
	{
		"loc": (2,2),
		"pop": [
			{
				"species": "Herbivore",
				"age": 5,
				"weight": 100
			},
			{
				"species": "Herbivore",
				"age": 5,
				"weight": 100
			}
		]
	}
]

sim = BioSim(island_map = the_map, ini_pop=ini_pop)

sim.set_animal_parameters("Herbivore", {"gamma":100})

sim.simulate(num_years=50, vis_years=3)

sim.save(path="./data/",name="my_love")

sim.simulate(num_years=50, vis_years= 5)

sim2 = load("./data/my_love.biosim")

sim2.set_animal_parameters("Herbivore", {"gamma":0})

sim2.simulate(num_years = 50, vis_years = 3)