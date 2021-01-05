# -*- coding: utf-8 -*-

"""
functioning logic of the island simulation
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, matshoemolsen@nmbu.no'


target_year = 100
current_year = 0


def cycling_cells():
    """
    function for going through cells on the map as this is required for multiple functions
    """
    pass


def cycling_animals():
    """
    function for going through animals in cells as this is required for multiple functions
    """
    pass


def fitness_calc():
    """
    function for calculating fitness as this is needed ALL THE TIME
    """
    pass


def season_feeding():
    """
    1. spawns in f_max amount of food in each cell

Herbivores
    2. herbivores eat an amount F in a residing cell in random order
    3. each time an herbivore eats F, f_max changes in the given cell
    4. herbivores gain weight beta * F~ where F~ = F if F < f_max and F~ = f_max if F > f_max
    -  loops for every herbivore until f_max = 0 in the given cell then the next cell

Carnivores
    5. fitness Phi gets calculated for each carnivore and herbivore and gets sorted by Phi
       (fitness for herbivores gets calculated once)
    6. each carnivore hunts a herbivore in order of Phi with success p (each herbivore gets hunted once?)
       on success carnivores gain weight beta * w_herb up to threshold F that year and targeted herbivore dies
    7. carnivores stop hunting until the sum of beta * w_herb => F for the given carnivore or all herbivores in a given
       cell has been targeted
    -  loops until all carnivores stop

    8. fitness Phi for carnivores gets calculated again
    """
    pass


def season_breeding(animals: list):
    """
    N_herbivore = number of herbivores in cell
    N_carnivore = number of carnivores in cell

    1. check cells where animals can breed, N > 1
    2. check every animal in given cell if they can breed, w < zeta * (w_birth + sigma_birth)

    3. loops through all animals that can breed and randomly gives birth given by min(1, gamma * Phi * (N_species - 1))
    4. on each success give the newborn a random weight w based on normal distribution N(w_birth, sigma_birth)
       then the mothers w = w - xi * w_newborn, if w < xi * w_newborn then no one is born
    """
    herb = filter(lambda O: type(O) == "herbavore", animals)
    herb_len = len(herb)
    pred = filter(lambda O: type(O) == "preditor", animals)
    pred_len = len(pred)
    new_herb = [ h for h in [H.birth(herb_len) for H in herb] if h != None ]
    new_pred = [ p for p in [P.birth(pred_len) for P in pred] if p != None ]
    return [ new_herb , new_pred ]





def season_migration():
    """

    :return:
    """
    pass


def season_aging(animals: list):
    """
    age += 1
    """
    for animal in animals:
        animal.a += 1
    return animals


def season_loss(animals: list):
    """
    w -= eta * w
    """
    for animal in animals:
        animal.w -= animal.eta * animal.w
    return animals


def season_death(animals : list):
    """
    check every animal if they die
    cycling_cells():
    cycling_animals():
    death = yes if w = 0
        else
        death = omega(1 - Phi)
    """
    animals = [A for A in [B.death() for B in animals] if A.life]
    return animals


def yearly_cycle(start_year, end_year, visual_year):
    """

    :return:
    """
    start_year = 0
    while start_year <= end_year:
        season_feeding()
        season_breeding()
        season_migration()
        season_aging()
        season_loss()
        season_death()
        start_year += 1
        if start_year % visual_year == 0:
            print('visuals')



if __name__ == '__main__':
    yearly_cycle(current_year, target_year)
