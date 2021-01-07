

from animal import herbavor, preditor
import random as ran
import visuals as bv

class BioSim:
	def __init__(self, island_map : str, ini_pop : list, seed : int,ymax_animals=None, cmax_animals=None, hist_specs=None,
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
		ran.seed(seed)
		self.island, self.illigal_coord = bv.string2map(island_map)
		
		temp_population = { pop['loc']: pop['pop'] for pop in ini_pop }
		
		self.population = self.add_population(temp_population)
	
	def set_animal_parameters(self, species: str, params: dict):
		"""
		Set parameters for animal species.
		:param species: String, name of animal species
		:param params: Dict with valid parameter specification for species
		"""
		species = species.lower()
		for dict_key in params:
			if species == "herbavore":
				herbavor.var[dict_key] = params[dict_key]
			elif species == "preditor":
				preditor.var[dict_key] = params[dict_key]
				if dict_key == "F":
					preditor.var["F_max"] = params[dict_key]

	
	def set_landscape_parameters(self, landscape, params):
		"""
		Set parameters for landscape type.
		:param landscape: String, code letter for landscape
		:param params: Dict with valid parameter specification for landscape
		"""
		bv.set_param(self.island,landscape,params)
	
	def simulate(self, num_years, vis_years=1, img_years=None):
		"""
		Run simulation while visualizing the result.
		:param num_years: number of years to simulate
		:param vis_years: years between visualization updates
		:param img_years: years between visualizations saved to files (default: vis_years)
		Image files will be numbered consecutively.
		"""
		pass
	
	def add_population(self, population:dict):
		"""
		Add a population to the island
		:param population: List of dictionaries specifying population (x,y):[{
			'age': int,
			'weight': float,
			'species': str
		}]
		"""
		for coord in population:
			cell = self.island[coord]
			for animal in population[coord]:
				if animal["species"].lower() == "herbivore":
					cell.herb_default.append(herbavor(a = animal["age"], w = animal["weight"]))
				elif animal["species"].lower() == "carnivore":
					cell.carn_default.append(preditor(a = animal["age"], w = animal["weight"]))
				else:
					raise ValueError("Got '{}'; needs 'herbivore' or 'carnivore'")
	
	@property
	def year(self):
		"""Last year simulated."""
		pass
	
	@property
	def num_animals(self):
		"""Total number of animals on island."""
		pass
	
	@property
	def num_animals_per_species(self):
		"""Number of animals per species in island, as dictionary."""
		pass
	
	def make_movie(self):
		"""Create MPEG4 movie from visualization images saved."""
		pass