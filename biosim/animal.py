# -*- coding: utf-8 -*-

__author__ = "Mats Hoem olsen"
__email__ = "mats.hoem.olsen@nmbu.no"

import numpy as np
import random as ran

"""
Module for animal logic. This file contains
	- class: animal
	- class (animal) : herbivore
	- class (animal) : carnivore
Any global function must start and/or end with '__' to not be included
in valid names.
"""


class animal:
	"""
	This is the superclass of all the animals.
	Can be used to create other animals however can't be used
	by it self.
	"""
	ret_moves = {
		'N': [1, 0],
		'S': [-1, 0],
		'W': [0, -1],
		'E': [0, 1]
	}

	def __init__(self, a: int, w: float, coord=[0, 0]):
		"""
		:param a: age of animal.
		:param w: waight of animal.
		:param coord: The coordinate of the animal.
		"""
		self.var["coord"] = coord
		self.var["w"] = w
		self.var["a"] = a
		self.var["life"] = True
		self.var["sigma"] = self.Big_phi()

	def Big_phi(self):
		"""
		'Big_phi' calculates the fitness of the animal based on its age and weight.
		:return: Fitness of animal.
		"""

		def q(S: str):
			"""
			Generates a function based on 'S'.
			:param S: 'P' for a smaller value, other for bigger.
			:return: function
			"""
			k = 1 if S == "P" else -1

			def new_q(x: float, xh: float, phi: float):
				r"""
				calculates the function $\frac{1}{1+e^{\pm\phi(x-x_h)}}$
				:param x: number
				:parma xh: number
				:parma phi: number
				:return: float
				"""
				return 1 / (1 + np.e ** (k * phi * (x - xh)))

			return new_q

		if self.var["w"] <= 0:
			return 0
		else:
			q_p = q("P")(self.var["a"], self.var["a_half"], self.var["phi_age"])
			q_n = q("N")(self.var["w"], self.var["w_half"], self.var["phi_weight"])
			return q_p * q_n

	@staticmethod
	def bin_choise(p):
		"""
		Gives True by random choise.
		:param p: probability 0<=p<=1
		:return: bool
		"""
		# By using the random.random function we utilise the seed declared in
		# the BioSim class, assuming uniform distribution since the length from
		# 0 to p is p, then the probability to hit <= p is p/1 = p
		return ran.random() < p

	@staticmethod
	def N(w: float, p: float):
		"""
		Gauss distrebution.
		:param w: mean
		:param p: standard deviance
		:return: a float in range [0,1]
		"""
		return ran.gauss(w, p)
	
	def age(self):
		self.var["a"] += 1
		self.var["sigma"] = self.Big_phi()

	def death(self):
		"""
		Desides if this animal dies. It got two ways to determen it:
				- Its weight is equal to 0 or less.
				- By random chance based on its fitness.
		"""
		if self.var["w"] <= 0 or self.bin_choise(self.var["omega"] * (1 - self.var["sigma"])):
			self.var["life"] = False

	def birth(self, N: int, necro_birth: bool = False):
		"""
		Determens if child is born. 
		This is determend by
		.. math:: w \leq \zeta ( w_{birth} + \sigma_{birth} )
		:param N:population number in cell.
		:param necro_birth: Give birth even when dead.
		:return: either None or a new instace of itself.
		"""
		p_pop = min(1, self.var["sigma"] * self.var["gamma"] * (N - 1))
		test_w = self.var["w"] >= (self.var["zeta"] * (self.var["w_birth"] + self.var["sigma_birth"]))
		test_chanse = self.bin_choise(p_pop)
		if not (test_w and test_chanse) :
			return None
		class_name = type(self).__name__
		k = eval(
			"{}(a = 0, w = self.N(self.var['w_birth'],self.var['sigma_birth']))".format(class_name))
		if not necro_birth:
			k.life = self.var["life"]
		if self.var["w"] <= self.var["xi"] * k.var["w"]:
			return None
		else:
			self.var["w"] -= self.var["xi"] * k.var["w"]
			self.var["sigma"] = self.Big_phi()
			return k

	def moveto(self, ret):
		"""
		Animal moves in a given diraction 'ret'
		:param ret: a key from 'ret_moves'.
		"""
		self.var["coord"][0] += animal.ret_moves[ret][0]
		self.var["coord"][1] += animal.ret_moves[ret][1]

	def move(self, ild: list):
		"""
		Given a map 'ild' it moves, or not.
		:param ild: list of illigal coorddiants.
		"""
		# Let the animal choose it's diraction based on what it
		# knows, by that we need not worry about what it must 
		# rather we let it do what it was born to do #
		do_move = self.bin_choise(self.var["mu"] * self.var["sigma"])
		direct = ran.choice([k for k in animal.ret_moves.keys()])
		direct_list = animal.ret_moves[direct]
		if self.check(direct_list, ild) and do_move:
			self.moveto(direct)

	def check(self, r: list, ild: list):
		"""
		Checks if possible to move in diraction r
		TODO: check if works.
		:param r: The diraction this instance moves to.
		:param ild: Contains illigal coorddinats.
		:return: bool
		"""
		c_coord = [self.var["coord"][0] + r[0], self.var["coord"][1] + r[1]]
		if tuple(c_coord) in ild:
			return False
		else:
			return True

	def loss_weight(self):
		"""
		calculates the new weight of the animal and
		reevaluets its fitness.
		"""
		self.var["w"] -= self.var["eta"] * self.var["w"]
		self.var["sigma"] = self.Big_phi()

	def feed(self,cell):
		pass



class Herbivore(animal):
	"""
	This is the herbavore class that eats non-meat like vegans.
	"""
	default_var = {
		"w_birth"     : 8,
		"sigma_birth" : 1.5,
		"beta"        : 0.9,
		"eta"         : 0.05,
		"a_half"      : 40,
		"phi_age"     : 0.6,
		"w_half"      : 10,
		"phi_weight"  : 0.1,
		"mu"          : 0.25,
		"gamma"       : 0.2,
		"zeta"        : 3.5 ,
		"xi"          : 1.2,
		"omega"       : 0.4,
		"F"           : 10}
	def __init__(self, a: int, w: float, coord = [0,0]):
		self.var = dict(Herbivore.default_var)
		super().__init__(a, w, coord= coord)

	def eat(self, F_there, return_food = False):
		"""
		Instace consumes a portion of F.
		:param F_there: number of food.
		:return: returns eaten amount if `return_food` is true.
		"""
		# Animals eat what is available, or can eat...#
		if not(type(F_there) == int or type(F_there) == float):
			raise ValueError("animal::herbavore::eat expected number, got {}".format(type(F_there)))
		# We gain what is possible, whitch is what the animal want or get.#
		self.var["w"] += self.var["beta"] * min(max(F_there,0), self.var["F"])
		self.var["sigma"] = self.Big_phi()
		if return_food:
			# This is handy when needed.#
			return min(max(F_there,0), self.var["F"])




class Carnivore(animal):
	"""
	This is the carnivore class that eat meat like non-vegans.
	"""
	default_var = {
		"w_birth"     : 6,
		"sigma_birth" : 1,
		"beta"        : 0.75,
		"eta"         : 0.125,
		"a_half"      : 40,
		"phi_age"     : 0.3,
		"w_half"      : 4,
		"phi_weight"  : 0.4,
		"mu"          : 0.4,
		"gamma"       : 0.8,
		"zeta"        : 3.5,
		"xi"          : 1.1,
		"omega"       : 0.8,
		"F"           : 50,
		"DeltaPhiMax" : 10}
	def __init__(self, a: int, w: float, coord = [0,0]):
		self.var = dict(Carnivore.default_var)
		super().__init__(a, w, coord=coord)

	def yield_life(self, L: list):
		"""
		Generator for life.
		:param L: The heard to eat.
		:yield: A soon to be dead animal.
		"""
		for l in L:
			# we know that the limits of the function is 0 and 1, and by analyzing the curve of the function with the limits
			# we can see that on negative values we get 0, note 0 > than a negativ number (excluding -0 for computers sake) and
			# 1 when the function is greater than the max value (e.i. greater than 1) for that reson we can with comfor use
			# max(1,min(0,f(x))) to determen the probability.
			probebility = max(0, min(1, (self.var["sigma"] - l.var["sigma"]) / self.var["DeltaPhiMax"]))
			# we agree that for a preditor to eat a pray it must be alive and the preditor must choose to accept the pray.
			# we use the function `bin_choise` to determen if it will.#
			if l.var["life"] and self.bin_choise(probebility):
				yield l

	def eat(self, F_there: list):
		"""
		Animal eats, because it is good.
		:param F_there: A list of herbavores.
		:return: updated list of herbavores.
		"""
		# Every preditor must try itself on all the pray available given it want to. 
		# We will therefor iterate over all the animals until it is feed up or have tryed on all of them.#
		F_there.sort(key= lambda O: O.var["sigma"])
		default_F = float(self.var["F"])
		for pray in self.yield_life(F_there):
			F_got = min(self.var["F"], pray.var["w"])
			self.var["w"] += self.var["beta"] * F_got
			pray.var["life"] = False
			self.var["F"] -= F_got
			self.var["sigma"] = self.Big_phi()
			if self.var["F"] == 0:
				self.var["F"] = default_F
				break
		# Since we don't care for dead animals we will discard all dead animals to the void before returing them to the next 
		# preditor.#
		self.var["F"] = default_F
		return [f for f in F_there if f.var["life"]]


if __name__ == "__main__":
	H = Herbivore(1, 4)
	H.gamma = 4
	print(H.gamma)
	Herbivore.gamma = 3
	print(H.gamma)
	K = Herbivore(2, 3)
	print(K.gamma)
