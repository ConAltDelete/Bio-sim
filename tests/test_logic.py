from biosim.logic import *
from biosim.simulation import BioSim

def test_migrasion():
	island, illigal = BioSim(island_map="WWWW\nWllW\nwwww".upper(),seed=1234)
	