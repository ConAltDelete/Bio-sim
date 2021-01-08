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
        'N': [0, 1],
        'S': [0, -1],
        'W': [1, 0],
        'E': [-1, 0]
    }

    def __init__(self, a: int, w: float, coord=[0, 0]):
        """
        :param a: age of animal.
        :param w: waight of animal.
        :param coord, list[int,int]: The coorddinate of the animal.
        """
        self.var["coord"] = coord
        self.var["w"] = w
        self.var["a"] = a
        self.var["life"] = True
        self.var["sigma"] = self.Big_phi()

    def Big_phi(self):
        """
        'Big_phi' calculates the fitness of the animal based on its age and weight.
        :return, float: Fitness of animal.
        """

        def q(S: str):
            """
            Generates a function based on 'S'.
            :param S: 'P' for a smaller value, other for bigger.
            """
            k = 1 if S == "P" else -1

            def new_q(x, xh, phi):
                return 1 / (1 + np.e ** (k * phi * (x - xh)))

            return new_q

        if self.var["w"] <= 0:
            return 0
        else:
            q_p = q("P")(self.var["a"],
                         self.var["a_half"], self.var["phi_age"])
            q_n = q("N")(self.var["w"],
                         self.var["w_half"], self.var["phi_weight"])
            return q_p * q_n

    @staticmethod
    def bin_choise(p):
        """
        Gives True by random choise.
        :param p: probability 0<=p<=1
        :return: bool
        """
        return ran.uniform(0, 1) <= p

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
        Determens if chiald is born.
        :param N:population number in cell.
        :param necro_birth: Give birth even when dead.
        :return: either None or a new instace of itself.
        """
        self.var["sigma"] = self.Big_phi()
        p_pop = min(1, self.var["sigma"] * self.var["gamma"] * (N - 1))
        if self.var["w"] < self.var["zeta"] * (self.var["w_birth"] + self.var["sigma_birth"]):
            return None
        if p_pop < ran.random():
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
            return k

    def moveto(self, ret):
        """
        Animal moves in a given diraction 'ret'
        :param ret: a key from 'ret_moves'.
        """
        self.var["coord"][0] += animal.ret_moves[ret][0]
        self.var["coord"][1] += animal.ret_moves[ret][1]

    def move(self, ild):
        """
        Given a map 'ild' it moves, or not.
        :param ild: list of illigal coorddiants.
        """
        do_move = self.bin_choise(self.var["mu"] * self.var["sigma"])
        direct = ran.choice([k for k in animal.ret_moves.keys()])
        direct_list = animal.ret_moves[direct]
        if self.check(direct_list, ild) and do_move:
            self.moveto(direct)

    def check(self, r: list, ild):
        """
        Checks if possible to move in diraction r
        TODO: check if works.
        :param r: The diraction this instance moves to.
        :param ild: Contains illigal coorddinats.
        :return, bool:
        """
        c_coord = [self.var["coord"][0] + r[0], self.var["coord"][1] + r[1]]
        if tuple(c_coord) in ild:
            return False
        else:
            return True


class herbavor(animal):
    """
    This is the herbavore class that eats non-meat like vegans.
    """

    def __init__(self, a: int, w: float, coord=[0, 0]):
        self.var = {"w_birth": 8,
                    "sigma_birth": 1.5,
                    "beta": 0.9,
                    "eta": 0.05,
                    "a_half": 40,
                    "coord": [0, 0],
                    "phi_age": 0.6,
                    "w_half": 10,
                    "phi_weight": 0.1,
                    "mu": 0.25,
                    "gamma": 0.2,
                    "zeta": 3.5,
                    "xi": 1.2,
                    "omega": 0.4,
                    "F": 10}
        super().__init__(a, w, coord=coord)

    def eat(self, F_there, return_food=False):
        """
        Instace consumes a portion of F.
        TODO: determen if return eaten amount
        :param F_there: number of food.
        """
        self.var["w"] += self.var["beta"] * min(max(F_there, 0), self.var["F"])
        self.var["sigma"] = self.Big_phi()
        if return_food:
            return min(max(F_there, 0), self.var["F"])


class preditor(animal):
    """
    This is the preditor class that eat meat like non-vegans.
    """
    def __init__(self, a: int, w: float, coord=[0, 0]):
        self.food = 50.0
        self.var = {"w_birth"     : 6,
            "coord"        : [0,0],
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
        super().__init__(a, w, coord=coord)

    def food_reset(self):
        self.food = self.var["F"]

    def hunting_chance(self, prey: object):
        """
        Generator for life.
        :param L: The heard to eat.
        :return: the probability.
        """
        if self.var["sigma"] <= prey.var["sigma"]:
            return 0
        if 0 < self.var["sigma"] - prey.var["sigma"] < self.var["DeltaPhiMax"]:
            return (self.var["sigma"] - prey.var["sigma"]) / self.var["DeltaPhiMax"]
        return 1

    def eat(self, F_there: object):
        """
        Animal eats, because it is good.
        :param F_there: A herbivore.
        """
        food_to_eat = min(self.food, F_there.var["w"])
        self.var["w"] += self.var["beta"] * food_to_eat
        self.food -= food_to_eat
        self.var["sigma"] = self.Big_phi()


if __name__ == "__main__":
    H = herbavor(1, 4)
    H.gamma = 4
    print(H.gamma)
    herbavor.gamma = 3
    print(H.gamma)
    K = herbavor(2, 3)
    print(K.gamma)
