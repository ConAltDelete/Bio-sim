

from .animal import Carnivore,Herbivore
import random as ran
from .visuals import string2map, set_param
from .logic import year_cycle
import sys
import re

class BioSim:
	def __init__(self, island_map : str, ini_pop : list, seed : int = None,ymax_animals=None, cmax_animals=None, hist_specs=None,
img_base=None, img_fmt='png'):
		"""
		:param island_map: Multi-line string specifying island geography
		:param ini_pop: List of dictionaries specifying initial population
		:param seed: Integer used as random number seed
		:param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
		:param cmax_animals: Dict specifying color-code limits for animal densities
		:param hist_specs: Specifications for histograms, see below
		:param img_base: String with beginning of file name for figures, including path
		:param img_fmt: String with file type for figures, e.g. 'png'
		If ymax_animals is None, the y-axis limit should be adjusted automatically.
		If cmax_animals is None, sensible, fixed default values should be used.
		cmax_animals is a dict mapping species names to numbers, e.g.,
		{'Herbivore': 50, 'Carnivore': 20}
		hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
		For each property, a dictionary providing the maximum value and the bin width must be
		given, e.g.,
		{'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
		Permitted properties are 'weight', 'age', 'fitness'.
		If img_base is None, no figures are written to file.
		Filenames are formed as
		'{}_{:05d}.{}'.format(img_base, img_no, img_fmt)
		where img_no are consecutive image numbers starting from 0.
		img_base should contain a path and beginning of a file name.
		"""
		# we set the random seed for future random number generation. In other words,
		# we make a random simulation consistent.#
		if seed != None: ran.seed(seed)

		self.island, self.illigal_coord = string2map(island_map)
		# We look for posible animals in animals.py, meaning we don't need to add maually
		# new animals. This is assuming no global function except in animal superclass. #
		self.names=[n for n in dir(sys.modules["biosim.animal"]) if not re.match("(__)|(np)|(ran)|(animal)",n)]
		self.population = self.add_population(ini_pop)

	
	def set_animal_parameters(self, species: str, params: dict):
		"""
		Set parameters for animal species.
		:param species: String, name of animal species
		:param params: Dict with valid parameter specification for species
		"""
		# Python abuse at its best.#
		check_keys = eval("{}.default_var.keys()".format(species))
		for key in params.keys():
			if key not in check_keys:
				raise ValueError("{} not in {}".format(key,species))
		eval("{}.default_var.update({})".format(species,params))

	
	def set_landscape_parameters(self, landscape : str, params: dict):
		"""
		Set parameters for landscape type.
		:param landscape: String, code letter for landscape
		:param params: Dict with valid parameter specification for landscape
		"""
		set_param(self.island,landscape,params)
	
	def simulate(self, num_years, vis_years=1, img_years=None):
		"""
		Run simulation while visualizing the result.
		:param num_years: number of years to simulate
		:param vis_years: years between visualization updates
		:param img_years: years between visualizations saved to files (default: vis_years)
		Image files will be numbered consecutively.
		"""
		for year in range(num_years):
			year_cycle(self.island,self.illigal_coord,year=year,visual_year=vis_years)
	
	def add_population(self, population:list):
		"""
		Add a population to the island
		:param population: List of dictionaries specifying population (y,x):[{
			'age': int,
			'weight': float,
			'species': str
		}]
		:param names: list of names one can use
		"""
		population = {popul["loc"]:popul["pop"] for popul in population}
		for coord in population:
			cell = self.island[coord]
			for animal in population[coord]:
				animal_name = animal["species"]
				if animal_name in self.names:
					if animal_name in cell.default:
						create_animal = eval("{}(a = animal['age'], w = animal['weight'])".format(animal_name))
						cell.default[animal_name].append(create_animal)
					else:
						create_animal = eval("{}(a = animal['age'], w = animal['weight'])".format(animal_name))
						cell.default[animal_name] = [create_animal]
				else:
					raise ValueError("Got '{}'; needs {}".format(animal["species"],self.names))
	
	@property
	def year(self):
		"""Last year simulated."""
		pass
	
	@property
	def num_animals(self):
		"""Total number of animals on island."""
		self.num_animals_per_species()
		self.total_animals = sum(self.dict_count.values())
	
	@property
	def num_animals_per_species(self):
		"""Number of animals per species in island, as dictionary."""
		self.dict_count = dict()
		for coord in self.island:
			for spesis in self.island[coord].default:
				if spesis in self.dict_count:
					self.dict_count[spesis] += len(self.island[coord].default[spesis])
				else:
					self.dict_count[spesis] = len(self.island[coord].default[spesis])
	
	def make_movie(self):
		"""Create MPEG4 movie from visualization images saved."""
		pass