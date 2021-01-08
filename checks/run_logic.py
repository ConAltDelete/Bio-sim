from biosim.simulation import BioSim
from biosim.logic import season_migration

if __name__ == '__main__':
	this_fucking_thing = BioSim(island_map = "WWWW\nWLLW\nWWWW", ini_pop = [{'loc':(2,2) , 'pop':[ {"species":"herbivore","age":5,"weight":20} for _ in range(10)] } ] , seed = 1234)
	the_map = this_fucking_thing.island
	illigal_moves = this_fucking_thing.illigal_coord
	for _ in range(30):
		season_migration(the_map,illigal_moves)
	for cell in the_map:
		print("coord:",the_map[cell].coord,"animals:",the_map[cell].herb_default)
		for C in the_map[cell].herb_default:
			print(C.var["coord"], C.var["a"])