from biosim.simulation import BioSim
map = "WWW\nWHW\nWWW\n"
ini_pop = [{
	"loc": (2,2),
	"pop": [{
		"species": "Herbivore",
		"age": 5,
		"weight": 100 # kg
	}]
}]
sim = BioSim(map,ini_pop)