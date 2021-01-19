from biosim.simulation import BioSim


ini_pop = [
	{
		"loc":(2,2),
		"pop": [
			{
				"species": "Herbivore",
				"age": 5,
				"weight": 100
			} for _ in range(10)
		]
	}
]

sim = BioSim(island_map="WWWW\nWLHW\nWLHW\nWWWW",ini_pop=ini_pop)

print(sim.str_map,end="\n\n")

for coord in sim.island:
	print(coord,sim.island[coord].type)
sim.simulate(50)
sim.re_map(new_map="WWWW\nWHLW\nWWWW\nWWWW")
sim.simulate(50)
print(sim.str_map,end="\n\n")

for coord in sim.island:
	print(coord,sim.island[coord].type)