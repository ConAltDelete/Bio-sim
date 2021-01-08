# -*- coding: utf-8 -*-

"""
functioning logic of the island simulation
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'

from biosim.island import Cells
from biosim.animal import *
from colorama import Fore
from colorama import Style
import random


def gen_cells():
    """
    function for generating cells at the zeroth year
    1. generates cells based on given map
    2. generates a cell for each coordinate
    3. does not generate a cell if the coordinate is a water cell
    4. for L, H and D generates different food
    """
    list_of_cells = list()
    list_of_cells.append(Cells(3, [0, 0]))
    return list_of_cells


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


def season_feeding(f_max_H, f_max_L, cell, herb: list):
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
    9. food value for carnivores gets reset
    """
    if cell.type == 3:
        cell.fill_food(f_max_L)
    elif cell.type == 2:
        cell.fill_food(f_max_H)

    if cell.n_herb != 0:
        random.shuffle(herb)
        for animal in herb:
            if cell.food > 0:
                cell.reduce_food(animal.eat(cell.food, return_food=True))
            else:
                break


def season_breeding(*animal: list):
    """
    N_herbivore = number of herbivores in cell
    N_carnivore = number of carnivores in cell

    1. check cells where animals can breed, N > 1
    2. check every animal in given cell if they can breed, w < zeta * (w_birth + sigma_birth)

    3. loops through all animals that can breed and randomly gives birth given by min(1, gamma * Phi * (N_species - 1))
    4. on each success give the newborn a random weight w based on normal distribution N(w_birth, sigma_birth)
       then the mothers w = w - xi * w_newborn, if w < xi * w_newborn then no one is born

    :return: [new of what ever you put in first,new of whatever comes second, ...]
    """

    for species in animal:
        if len(species) > 1:
            pred_len = len(species)
            species.extend([p for p in [P.birth(pred_len) for P in species] if p is not None])


def season_migration(cells: dict, illigal_moves: list):
    """
    Animals moves to desired location if possible.
    :param cells: dictonary with coordinats as key, and Cells objects as value
    :return:
    """
    moving_animals = {"herb":{},"pred":{}}
    for cell in cells.values():
        cell.migration(illigal_moves)
        for mov_herb in cell.herb_migrate:
            moving_animals["herb"][mov_herb.var["coord"]] = mov_herb
        for mov_carn in cell.carn_migrate:
            moving_animals["pred"][mov_carn.var["coord"]] = mov_carn

    # moving animals
    for mov_herb in moving_animals["herb"]:
        cells[mov_herb].herb_default.extend(moving_animals["herb"][mov_herb])
    for mov_pred in moving_animals["pred"]:
        cells[mov_pred].carn_default.extend(moving_animals["pred"][mov_pred])


def season_aging(*animals: list):
    """
    for loop outside of function that check every cell and animals:list = cells.herb_default of that cell
    age += 1
    """

    for specis in animals:
        for turd in specis:
            turd.age()


def season_loss(*animal: list):
    """
    for loop outside of function that check every cell and animals:list = cells.herb_default of that cell
    w -= eta * w
    """
    for species in animal:
        for animals in species:
            animals.var["w"] -= animals.var["eta"] * animals.var["w"]


def season_death(cell, herb: list, carn: list):
    """
    for loop outside of function that check every cell and animals:list = cells.herb_default of that cell
    death = yes if w = 0
        else
        death = omega(1 - Phi)
    """
    """[B.death() for B in herb]
    cell.herb_default = [A for A in herb if A.var["life"]]

    [B.death() for B in carn]
    cell.carn_default = [A for A in carn if A.var["life"]]"""
    for animal in herb:
        if animal.var["w"] == 0 or (animal.var["omega"] * (1 - animal.var["sigma"])) > random.random():
            herb.remove(animal)


def yearly_cycle(end_year=100, visual_year=100):
    """
    1. generation of cells
    2. loop through the year
    """
    gen_cells()
    cells = gen_cells()
    cells[0].herb_default = [herbavor(5, 20.0) for _ in range(50)]
    start_year = 0
    while start_year < end_year:
        for c in cells:
            c.count_herb()
            season_feeding(300, 800, c, c.herb_default)
            sumw = 0.0
            for a in c.herb_default:
                sumw = sumw + a.var["w"]
            print("sum of weight before breeding", sumw)

        for c in cells:
            season_breeding(c.herb_default, c.carn_default)
            sumb = 0.0
            for a in c.herb_default:
                sumb = sumb + a.var["w"]
            print("sum of weight after breeding", sumb)

        """season_migration(cells)"""

        for c in cells:
            season_aging(c.herb_default, c.carn_default)

        for c in cells:
            season_loss(c.herb_default, c.carn_default)
            suml = 0.0
            for a in c.herb_default:
                suml = suml + a.var["w"]
            print("sum of weight after loss", suml)

        for c in cells:
            season_death(c, c.herb_default, c.carn_default)
            sumd = 0.0
            for a in c.herb_default:
                sumd = sumd + a.var["w"]
            print("sum of weight after death", sumd)

        start_year += 1
        if start_year % visual_year == 0:
            print(f"{Fore.RED}Current year{Style.RESET_ALL}", start_year)
            if len(cells[0].herb_default) > 0:
                for a in cells[0].herb_default:
                    print("Age", a.var["a"])
                    print("Weight", a.var["w"])
                    print("Fitness", a.var["sigma"])
                cells[0].count_herb()
                print(cells[0].n_herb)


if __name__ == '__main__':
    yearly_cycle()

