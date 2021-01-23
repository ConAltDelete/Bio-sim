# -*- coding: utf-8 -*-

"""
Module for animal logic. This file contains:
    - class: animal
    - class (animal) : herbivore
    - class (animal) : carnivore
Any global function must start and/or end with '__' to not be included
in valid names.
"""

__author__ = "Mats Hoem olsen, Roy Erling Granheim"
__email__ = "mats.hoem.olsen@nmbu.no, roy.erling.granheim@nmbu.no"

import numpy as np
import random as ran


class animal:
    """
    This is the superclass of all the animals.
    Can be used to create other animals however can't be used
    by it self.
    """
    default_var = {
        "w_birth": 10,
        "sigma_birth": 1,
        "beta": 0.5,
        "eta": 0.5,
        "a_half": 43,
        "phi_age": 0.4,
        "w_half": 5,
        "phi_weight": 0.001,
        "mu": 0.3,
        "gamma": 2000,
        "zeta": 1233,
        "xi": 1,
        "omega": 0.2,
        "F": 0}
    ret_moves = {
        'N': [1, 0],
        'S': [-1, 0],
        'W': [0, -1],
        'E': [0, 1]
    }

    def __init__(self, a: int, w: float, coord=None, random_name=False):
        """
        :param int a: age of animal.
        :param float w: weight of animal.
        :param list[int,int] coord: The coordinate of the animal.
        """
        self.name = self.random_name() if random_name else None
        self.var["coord"] = coord
        self.var["w"] = w
        self.var["a"] = a
        self.var["life"] = True
        self.var["phi"] = self.big_phi()

    def big_phi(self):
        """
        'big_phi' calculates the fitness of the animal based on its age and weight. This value is
        crucial to this entire operation.


        :return: Fitness of animal.
        """

        def q(s: str):
            """
            Generates a function based on 'S'.


            :param s: 'P' for a smaller value, other for bigger.
            :return: function
            """
            k = 1 if s == "P" else -1

            def new_q(x: float, xh: float, phi: float):
                """
                calculates the function


                :param x: number
                :param xh: number
                :param phi: number
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
    def n(w: float, p: float):
        """
        Gaussian distribution.


        :param w: mean
        :param p: standard deviance
        :return: a float in range [0,1]
        """
        return ran.gauss(w, p)

    def age(self):
        self.var["a"] += 1

    def death(self):
        """
        Decides if this animal dies. It got two ways to determine it:
                - Its weight is equal to 0 or less.
                - By random chance based on its fitness.
        """
        if self.var["w"] <= 0 or (ran.random() < (self.var["omega"] * (1 - self.var["phi"]))):
            self.var["life"] = False

    def birth(self, n: int):
        """
        Birth it determined by the fitness of the animal, its weight, and the number of the species around.
        If the weight of the mother is smaller than the weight of the child, it will not give birth.

        Another factor to consider is chance, even if the conditions are met there is still no guarantee to
        give birth. Unless you mess with its default values.


        :param n: population number in cell.
        :return: either None or a new instance of itself.
        """
        self.var["phi"] = self.big_phi()
        test_w = self.var["w"] >= (self.var["zeta"] * (self.var["w_birth"] + self.var["sigma_birth"]))
        test_chance = ran.random() < min(1, self.var["phi"] * self.var["gamma"] * (n - 1))
        if not (test_w and test_chance):
            return None
        k = type(self)(a=0, w=self.n(self.var['w_birth'], self.var['sigma_birth']))

        if self.var["w"] <= self.var["xi"] * k.var["w"]:
            return None
        else:
            self.var["w"] -= self.var["xi"] * k.var["w"]
            self.var["phi"] = self.big_phi()
            return k

    def move(self, ild: list):
        """
        For an animal to move it must first be fit enough to move. This is determined by its fitness and ``mu``.

        If an animal is fit to move but tries to move to an cell that is not possible, it won't move at all.
        This illegal move is determined by the parameter ``ild`` which is an list generated from ``string2map``.


        :param ild: list of illegal coordinates.
        """
        # Let the animal choose it's direction based on what it
        # knows, by that we need not worry about what it must
        # rather we let it do what it was born to do #

        do_move = ran.random() < (self.var["mu"] * self.var["phi"])
        direct = ran.choice([k for k in animal.ret_moves.keys()])
        direct_list = animal.ret_moves[direct]
        if ((self.var["coord"][0] + direct_list[0], self.var["coord"][1] + direct_list[1]) not in ild) and do_move:
            self.var["coord"][0] += direct_list[0]
            self.var["coord"][1] += direct_list[1]

    def loss_weight(self):
        """
        calculates the new weight of the animal and
        reevaluates its fitness.
        """
        self.var["w"] -= self.var["eta"] * self.var["w"]

    @staticmethod
    def random_name():
        """
        Method to give each newly initialized animal a mostly unique name
        """
        name_given = str()
        name_length = 5
        name_list = ['Roy', 'Mats', 'Hans', 'Sabina', 'Amir', 'Ngoc', 'Mike', 'the', 'Mario', 'Sephiroth', 'McMuffin',
                     'Herby', 'McHerbface', 'Carny', 'McCarnface', 'Cthulhu', 'Harambe', 'Cheems', 'Sonic', 'Hawk',
                     'Vinny', 'Pog', 'Jotaro', 'Giovanni', 'Super', 'Penny', 'Jack', 'Jill', 'Golden', 'Jugemu',
                     'Unlucky', 'Lucky']
        for name in range(name_length):
            name_given += ran.choice(name_list) + ' '
        name_given = name_given[:-1]
        return name_given


class Herbivore(animal):
    """
    This is the herbivore class that eats non-meat like vegans.
    """
    default_var = {
        "w_birth": 8,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40,
        "phi_age": 0.6,
        "w_half": 10,
        "phi_weight": 0.1,
        "mu": 0.25,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10}

    def __init__(self, a: int, w: float, coord=None):
        self.var = dict(self.default_var)
        super().__init__(a, w, coord=coord)

    def eat(self, f_there):
        """
        ``herbivore`` eats of the cell (which is represented by the number ``f_there``) and improves its own fitness.


        :param f_there: number of food.
        :return: returns eaten amount if `return_food` is true.
        """
        # We gain what is possible, which is what the animal want or get.#
        self.var["w"] += self.var["beta"] * min(f_there.food, self.var["F"])
        self.var["phi"] = self.big_phi()
        f_there.food -= float(min(f_there.food, self.var["F"]))


class Carnivore(animal):
    """
    This is the carnivore class that eat meat like non-vegans.
    """
    default_var = {
        "w_birth": 6,
        "sigma_birth": 1,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 40,
        "phi_age": 0.3,
        "w_half": 4,
        "phi_weight": 0.4,
        "mu": 0.4,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.8,
        "F": 50,
        "DeltaPhiMax": 10}

    def __init__(self, a: int, w: float, coord=None):
        self.var = dict(self.default_var)
        super().__init__(a, w, coord=coord)

    def _yield_life(self, fresh_meat: list):
        """
        Generator for life that is about to be murdered.


        :param fresh_meat: The heard to eat.
        :yield: A soon to be dead animal.
        """
        for meat in fresh_meat:
            # we know that the limits of the function is 0 and 1, and by analyzing the curve of the function
            # with the limits we can see that on negative values we get 0, note 0 > than a negative number
            # (excluding -0 for computers sake) and 1 when the function is greater than the max value
            # (e.i. greater than 1) for that reason we can with comfort use max(1,min(0,f(x))) to determine
            # the probability.
            probability = max(0, min(1, (self.var["phi"] - meat.var["phi"]) / self.var["DeltaPhiMax"]))
            # we agree that for a predator to eat a pray it must be alive and the predator must choose to accept
            # the pray.#
            if meat.var["life"] and (ran.random() < probability):
                yield meat

    def eat(self, cell):
        """
        ``Carnivore`` eats ``Herbivore`` given both fitness. For the predator to have an chance to eat the herbivore
         it must have better fitness than the herbivore.


        :param Cells cell: The entire cell
        """
        # Every predator must try itself on all the pray available given it want to.
        # We will therefore iterate over all the animals until it is feed up or have tried on all of them.#
        herb_herd = list(cell.default["Herbivore"])
        herb_herd.sort(key=lambda o: o.var["phi"])
        default_f = float(self.var["F"])
        for pray in self._yield_life(herb_herd):
            f_got = min(self.var["F"], pray.var["w"])
            self.var["w"] += self.var["beta"] * f_got
            pray.var["life"] = False
            self.var["F"] -= f_got
            self.var["phi"] = self.big_phi()
            if self.var["F"]:
                self.var["F"] = default_f
                break
        # Since we don't care for dead animals we will discard all dead animals to the void
        # before returning them to the next predator.#
        self.var["F"] = default_f
        cell.default["Herbivore"] = [f for f in herb_herd if f.var["life"]]


if __name__ == "__main__":
    pass
