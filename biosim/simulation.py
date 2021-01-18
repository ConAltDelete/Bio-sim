# -*- coding: utf-8 -*-

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, matshoemolsen@nmbu.no'

from .animal import *
import random as ran
from .visuals import string2map, set_param
from .logic import year_cycle
from .visualization import Visualization
import sys
import re
import subprocess
import os
import time
import pickle


class BioSim:
	"""
		BioSim is an closed enviroment that can simulate animals on an given map.
		The animals that can be simulated is listed under `biosim.animal`.


		:param island_map: Multi-line string specifying island geography
		:param ini_pop: List of dictionaries specifying initial population
		:param seed: Integer used as random number seed
		:param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
		:param cmax_animals: Dict specifying color-code limits for animal densities
		:param hist_specs: Specifications for histograms, see below
		:param img_base: String with beginning of file name for figures, including path
		:param img_fmt: String with file type for figures, e.g. 'png'`


		If ymax_animals is None, the y-axis limit should be adjusted automatically.
		If cmax_animals is None, sensible, fixed default values should be used.
		cmax_animals is a dict mapping species names to numbers, e.g.,
		``{'Herbivore': 50, 'Carnivore': 20}``
		hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
		For each property, a dictionary providing the maximum value and the bin width must be
		given, e.g.,
		``{'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}``
		Permitted properties are ``'weight'``, ``'age'``, ``'fitness'``.
		If img_base is None, no figures are written to file.
		Filenames are formed as
		``'{}_{:05d}.{}'.format(img_base, img_no, img_fmt)``
		where img_no are consecutive image numbers starting from 0.
		img_base should contain a path and beginning of a file name.
	"""
	def __init__(self, island_map : str, ini_pop : list, seed : int = None, ymax_animals=None, cmax_animals=None, hist_specs=None,
img_base=None, img_fmt='png', tmean = False):
		# we set the random seed for future random number generation. In other words,
		# we make a random simulation consistent.#
		if seed: ran.seed(seed)

		self.str_map = island_map.strip()

		# We look for posible animals in animals.py, meaning we don't need to add maually
		# new animals. This is assuming no global function except in animal superclass. #
		self.names=[n for n in dir(sys.modules["biosim.animal"]) if not re.match("(\w*__\w*)|(np)|(ran)|(animal)",n)]
		self.default_values_species = {species : dict(eval("{}.default_var".format(species) ) ) for species in self.names }
		self.island, self.illigal_coord = string2map(island_map, self.names)
		self.add_population(ini_pop)
		self._year = 0
		self.viz = None
		self.data = dict()
		self.total_age = dict()
		self.total_weight = dict()
		self.total_fitness = dict()
		self.tmean = tmean
		if self.tmean:
			self.mean = {species:0 for species in self.names}
		self.ymax_animals = ymax_animals
		self._img_base = '../data/{}'.format(img_base) if img_base else None
		self._img_fmt = img_fmt

	def set_animal_parameters(self, species: str, params: dict):
		"""
		Set parameters for animal species.


		:param species: String, name of animal species
		:param params: Dict with valid parameter specification for species
		"""

		for key in params.keys():
			if key not in self.default_values_species[species]:
				raise ValueError("{} not in {}".format(key,species))
			if params[key] < 0:
				raise ValueError("{} is less than zero".format(key))
		self.default_values_species[species].update(params)
		for coord in self.island:
			if species in self.island[coord].default:
				for animal in self.island[coord].default[species]:
					animal.var.update(self.default_values_species[species])


	def set_landscape_parameters(self, landscape : str, params: dict):
		"""
		Set parameters for landscape type.


		:param str landscape: String, code letter for landscape
		:param dict[str:float] params: Dict with valid parameter specification for landscape
		"""
		set_param(self.island,landscape,params)
	
	def simulate(self, num_years, vis_years=1, img_years=None):
		"""
		Run simulation while visualizing the result.


		:param int num_years: number of years to simulate
		:param int vis_years: years between visualization updates
		:param img_years: years between visualizations saved to files (default: vis_years)
		Image files will be numbered consecutively.
		"""
		if vis_years is not None:
			if self._year % vis_years == 0: # visualization not working correctly with vis_years > 1
				if self.viz is None:
					self.viz = Visualization(self.names, self._img_base, self._img_fmt, self.ymax_animals)
					self.viz.convert_map(self.str_map)
				self.viz.setup_graphics(num_years)
		for year in range(num_years):
			year_cycle(self.island,self.illigal_coord)
			if vis_years != None:
				if self._year % vis_years == 0:
					self.get_data()
					self.viz.update_data(self.num_animals_per_species,
									 self.total_age,
									 self.total_weight,
									 self.total_fitness)
				self.viz.update_graphics(self._year, self.data)
				self.viz.create_images()
			self._year += 1
			if self.tmean:
				for species in self.num_animals_per_species:
					self.mean[species] = self.mean[species] + ((self.num_animals_per_species[species] - self.mean[species])/self._year)
	
	def add_population(self, population:list):
		"""
		Add a population to the island


		:param list population: List of dictionaries specifying population (y,x):[{
			'age': int,
			'weight': float,
			'species': str
		}]
		:param names: list of names one can use
		"""
		population = {popul["loc"]:popul["pop"] for popul in population}
		for coord in population:
			if coord in self.illigal_coord:
				raise ValueError("An animal was placed at {} witch is an illegal placement.".format(coord))
			cell = self.island[coord]
			for animal in population[coord]:
				animal_name = animal["species"]
				if animal["age"] < 0:
							raise ValueError("age is less than zero")
				elif animal["weight"] < 0:
					raise ValueError("weight is less than zero")
				if animal_name in self.names:
					if animal_name in cell.default:
						create_animal = eval("{}(a = animal['age'], w = animal['weight'])".format(animal_name))
						create_animal.var.update(self.default_values_species[animal_name])
						cell.default[animal_name].append(create_animal)
					else:
						create_animal = eval("{}(a = animal['age'], w = animal['weight'])".format(animal_name))
						create_animal.var.update(self.default_values_species[animal_name])
						cell.default[animal_name] = [create_animal]
				else:
					raise ValueError("Got '{}'; needs {}".format(animal["species"],self.names))

	def get_data(self):
		"""Get data from the cells in self.island"""
		columns = self.str_map.splitlines()
		rows = list(columns[0])
		
		for species in self.names:
			z = list()
			for y in range(len(columns)):
				temp = list()
				for x in range(len(rows)):
					v = self.island[(y + 1, x + 1)].count_species[species]
					temp.append(v)
				z.append(temp)
			self.data[species] = z

		self.total_age = {'Herbivore': [], 'Carnivore': []}
		for names in self.names:
			for coord in self.island:
				for units in self.island[coord].count_age[names]:
					self.total_age[names].append(units)

		self.total_weight = {'Herbivore': [], 'Carnivore': []}
		for names in self.names:
			for coord in self.island:
				for units in self.island[coord].count_weight[names]:
					self.total_weight[names].append(units)

		self.total_fitness = {'Herbivore': [], 'Carnivore': []}
		for names in self.names:
			for coord in self.island:
				for units in self.island[coord].count_fitness[names]:
					self.total_fitness[names].append(units)

	def create_movie(self, movie_fmt='gif'):
		"""Creates a movie of the simulation"""
		if self._img_base is None:
			raise ValueError("RuntimeError: No filename defined")

		if movie_fmt == 'mp4':
			try:
				subprocess.check_call([
					'ffmpeg',
					'-i', '{}_%05d.png'.format(self._img_base),
					'-y',
					'-profile:v', 'baseline',
					'-level', '3.0',
					'-pix_fmt', 'yuv420p',
					'{}.{}'.format(self._img_base, movie_fmt)])
			except subprocess.CalledProcessError as err:
				raise ValueError('RuntimeError: ERROR: ffmpeg failed with: {}'.format(err))

		elif movie_fmt == 'gif':
			try:
				subprocess.check_call([
					'magick',
					'-delay', '1',
					'-loop', '0',
					'{}_*.png'.format(self._img_base),
					'{}.{}'.format(self._img_base, movie_fmt)])
			except subprocess.CalledProcessError as err:
				raise ValueError('RuntimeError: ERROR: convert failed with: {}'.format(err))

		else:
			raise ValueError('Unknown movie format: ' + movie_fmt)

	@property
	def year(self):
		"""Last year simulated."""
		return self._year
	
	@property
	def num_animals(self):
		"""Total number of animals on island."""
		return sum(self.num_animals_per_species.values())
	
	@property
	def num_animals_per_species(self):
		"""Number of animals per species in island, as dictionary."""
		dict_count = {spesis : 0 for spesis in self.names}
		for coord in self.island:
			for spesis in self.island[coord].default:
				if spesis in dict_count:
					dict_count[spesis] += len(self.island[coord].default[spesis])
				else:
					dict_count[spesis] = len(self.island[coord].default[spesis])
		return dict_count

	def load(self,file):
		"""
		loads a save_file of users choosing.

		:param str file: file to be loaded.
		"""
		try:
			self.__dict__.update(pickle.load(open(file,"br")).__dict__)
		except:
			ValueError("This file is not a BioSim file.")

	def save(self, path: str = ""):
		if type(path) is not str:
			raise ValueError("TypeError: path must be a str, not a {}".format(type(path)))
		if path == "":
			direct = ""
		elif path.endswith("/"):
			direct = path
		else:
			direct = path + "/"

		if not(os.path.isdir(direct)):
			os.mkdir("./"+direct)
		save_file = open(direct + "save_{}.biosim".format(str(time.time())),"bw")
		pickle.dump(self,save_file)

