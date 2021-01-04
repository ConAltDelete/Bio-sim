# -*- coding: utf-8 -*-

import numpy as np
import random as ran

__author__ = "Mats Hoem olsen"
__email__ = "mats.hoem.olsen@nmbu.no"

class animal:
	"""
	This is the superclass of all the animals.
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
		if self.w <= 0:
			return 0 
		else: 
			q_p = self.q("P")(self.a,self.a_half,self.phi_age)
			q_n = self.q("N")(self.w,self.w_half,self.phi_weight)
			return q_p*q_n

	def q(self,S):
		k = 1 if S == "P" else -1
		def new_q(x,xh,phi):
			return 1/(1+np.e**(k*phi*(x-xh)))
		return new_q

	def bin_choise(self,p):
		"""
		Gives True by random choise.
		:param p: probability 0<=p<=1
		"""
		return bool(np.random.choice([1,0],size=1,p=[p,1-p])[0])

	def N(self,w,p):
		"""
		Gauss distrebution.
		:param w:
		:param p:
		"""
		return ran.gauss(w,p)

	def death(self):
		if self.w <= 0 or self.bin_choise(self.omega*(1-self.sigma)):
				self.life = False

	def birth(self,N,necro_birth = False):
		"""
		Determens if chiald is born.
		:param N, int: population number in cell.
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
		:param ild: list of illigal spots.
		"""
		do_move = self.bin_choise(self.mu*self.sigma)
		direct  = ran.choice([k for k in animal.ret_moves.keys()])
		if self.check(direct,ild) and do_move:
			self.moveto(direct)

	def check(self,r,ild):
		"""
		Checks if posible to move 
		TODO: check if works.
		"""
		c_coor = [self.coor[0] + r[0], self.coor[1] + r[1]]
		if c_coor in ild:
			return False
		else: return True