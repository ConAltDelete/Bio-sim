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
		It takes 
		"""
		return bool(np.random.choice([1,0],size=1,p=[p,1-p])[0])

	def N(self,w,p):
		return ran.gauss(w,p)