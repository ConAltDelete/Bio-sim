# -*- coding: utf-8 -*-

__author__ = "Mats Hoem olsen"
__email__ = "mats.hoem.olsen@nmbu.no"

import numpy as np
import random as ran

"""
Module for animal logic. This file contains
	- class: animal
	- class (animal) : herbavore
	- class (animal) : preditor
"""

class animal:
	"""
	This is the superclass of all the animals.
	Can be used to create other animals however can't be used
	by it self.
	"""
	ret_moves = {
		'N':[0,1],
		'S':[0,-1],
		'W':[1,0],
		'E':[-1,0]
	}
	def __init__(self,a:int,w:float,coor=[0,0]):
		"""
		:param a, int: age of animal.
		:param w, float: waight of animal.
		:param coor, list[int,int]: The coordinate of the animal.
		"""
		self.coor   = coor
		self.w      = w
		self.a      = a
		self.life   = True
		self.sigma  = self.Big_phi()

	def Big_phi(self):
		"""
		'Big_phi' calculates the fitness of the animal based on its age and weight.
		:return, float: Fitness of animal.
		"""
		def q(S: str):
			"""
			Generates a function based on 'S'.
			:param S, str: 'P' for a smaller value, other for bigger.
			"""
			k = 1 if S == "P" else -1
			def new_q(x,xh,phi):
				return 1/(1+np.e**(k*phi*(x-xh)))
			return new_q

		if self.w <= 0:
			return 0 
		else: 
			q_p = q("P")(self.a,self.a_half,self.phi_age)
			q_n = q("N")(self.w,self.w_half,self.phi_weight)
			return q_p*q_n

	@staticmethod
	def bin_choise(p):
		"""
		Gives True by random choise.
		:param p, float: probability 0<=p<=1
		:return, bool: bool
		"""
		return bool(np.random.choice([1,0],size=1,p=[p,1-p])[0])

	@staticmethod
	def N(w,p):
		"""
		Gauss distrebution.
		:param w, float: mean
		:param p, float: standard deviance
		:return, float: a float in range [0,1]
		"""
		return ran.gauss(w,p)

	def death(self):
		"""
		Desides if this animal dies. It got two ways to determen it:
			- Its weight is equal to 0 or less.
			- By random chance based on its fitness.
		"""
		if self.w <= 0 or self.bin_choise(self.omega*(1-self.sigma)):
				self.life = False

	def birth(self,N,necro_birth = False):
		"""
		Determens if chiald is born.
		:param N, int: population number in cell.
		:return None/\{herbavore,preditor\}: either None or a new instace of itself.
		"""
		p_pop = min(1,self.sigma*self.gamma*(N-1))
		if self.w < self.zeta*(self.w_birth + self.sigma_birth) and not self.bin_choise(p_pop):
			return None
		class_name = type(self).__name__
		k = eval("{}(a = 0, w = self.N(self.w_birth,self.sigma_birth))".format(class_name))
		if not necro_birth:
			k.life = self.life
		if self.w <= self.xi*k.w :
			return None
		else:
			self.w -= self.xi*k.w
			return k

	def moveto(self, ret):
		"""
		Animal moves in a given diraction 'ret'
		:param ret, str: a key from 'ret_moves'.
		"""
		self.coor[0] += animal.ret_moves[ret][0]
		self.coor[1] += animal.ret_moves[ret][1]

	def move(self,ild):
		"""
		Given a map 'ild' it moves, or not.
		:param ild: list of illigal coordiants.
		"""
		do_move = self.bin_choise(self.mu*self.sigma)
		direct  = ran.choice([k for k in animal.ret_moves.keys()])
		if self.check(direct,ild) and do_move:
			self.moveto(direct)

	def check(self,r: list,ild):
		"""
		Checks if possible to move in diraction r
		TODO: check if works.
		:param r, list[int]: The diraction this instance moves to.
		:param ild: Contains illigal coordinats.
		:return, bool:
		"""
		c_coor = [self.coor[0] + r[0], self.coor[1] + r[1]]
		if c_coor in ild:
			return False
		else: return True


class herbavor(animal):
	"""
	This is the herbavore class that eats non-meat like vegans.
	"""
	w_birth     = 8
	sigma_birth = 1.5
	beta        = 0.9
	eta         = 0.05
	a_half      = 40
	phi_age     = 0.6
	w_half      = 10
	phi_weight  = 0.1
	mu          = 0.25
	gamma       = 0.2
	zeta        = 3.5
	xi          = 1.2
	omega       = 0.4
	F           = 10

	def eat(self,F_there):
		"""
		Instace consumes a portion of F.
		TODO: determen if return eaten amount
		:param F_there, float/int: number of food.
		"""
		self.w += self.beta * min(F_there,self.F)
		self.sigma = self.Big_phi()

class preditor(animal):
	"""
	This is the preditor class that eat meat like non-vegans.
	"""
	w_birth     = 6
	sigma_birth = 1
	beta        = 0.75
	eta         = 0.125
	a_half      = 40
	phi_age     = 0.3
	w_half      = 4
	phi_weight  = 0.4
	mu          = 0.4
	gamma       = 0.8
	zeta        = 3.5
	xi          = 1.1
	omega       = 0.8
	F           = 50
	DeltaPhiMax = 10

	def yield_life(self,L : list):
		"""
		Generator for life.
		:param L, list[herbavore]: The heard to eat.
		:yield: A soon to be dead animal.
		"""
		for l in L:
			if l.life and self.bin_choise(max(0,min(1,(self.sigma-l.sigma)/self.DeltaPhiMax))):
				yield l

	def eat(self,F_there : list):
		"""
		Animal eats, because it is good.
		:param F_there, list[herbavore]: A list of herbavores.
		:return, list[herbavore]: updated list of herbavores.
		"""
		for pray in self.yield_life(F_there):
			F_got      = min(self.F,pray.w)
			self.w    += self.beta*F_got
			pray.life  = False
			self.F    -= F_got
			self.sigma = self.Big_phi()
			if self.F == 0:
				break
		return F_there

if __name__ == "__main__":
	H = herbavor(1,4)
	H.gamma = 4
	print(H.gamma)
	herbavor.gamma = 3
	print(H.gamma)
	K = herbavor(2,3)
	print(K.gamma)