# -*- coding: utf-8 -*-

"""
functioning logic of the island simulation
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'

from .island import Cells
from .animal import *
#from .colorama import Fore
#from .colorama import Style
from .simulation import BioSim

def gen_cells():
    """
    function for generating cells at the zeroth year
    1. generates cells based on given map
    2. generates a cell for each coordinate
    3. does not generate a cell if the coordinate is a water cell
    4. for L, H and D generates different food


    NOTE: Made code in `visual.py` that generates map from string.
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

    NOTE: animal class has this covered.
    """
    pass


def season_feeding(f_max_H, f_max_L, cell: Cells):
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
    # possible to make happen in `Cells` object by `__init__`
    if cell.type == 3:
        cell.fill_food(f_max_L)
    elif cell.type == 2:
        cell.fill_food(f_max_H)
    cell.count_herb()
    # assums single cell given, othervise put in loop
    if cell.n_herb != 0:
        for animal in cell.herb_default:
            if cell.food > 0:
                cell.reduce_food(animal.eat(cell.food, return_food=True))
            else:
                break
    for animal in cell.carn_default:
        if all( not H.life for H in cell.herb_default):
            break # Timesaver, but `preditor` object can distigvish between dead animal and an alive one.
        cell.herb_default = [ h for h in animal.eat(cell.herb_default) if h.var["life"]] # replace original list with new list with not dead animals
    # preditor food reset
    for animal in cell.carn_default:
        animal.var["F"] = animal.var["F_max"]


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
            pups = list()
            pred_len = len(species)
            new_pred = [p for p in [P.birth(pred_len) for P in species] if p is not None]
            pups = pups + new_pred
            species.extend(pups)


def season_migration(cells: dict, illigal_moves: list):
    """
    Animals moves to desired location if possible, else they don't move from cell.
    :param cells: dictonary with coordinats as key, and Cells objects as value
    :return:
    """
    moving_animals = {"herb":{},"pred": {} }
    for cell in cells:
        cells[cell].migration(illigal_moves)
        herb_migrating_len = len(cells[cell].herb_migrate)
        carn_migrating_len = len(cells[cell].carn_migrate)
        for mov_herb in range(herb_migrating_len):
            try:
                moving_animal = cells[cell].herb_migrate.pop(0)
            except IndexError:
                print("IndexError in logic::season_migration::mov_herb")
                break
            if tuple(moving_animal.var["coord"]) not in moving_animals["herb"]:
                moving_animals["herb"][tuple(moving_animal.var["coord"])] = [moving_animal]
            else:
                moving_animals["herb"][tuple(moving_animal.var["coord"])].append(moving_animal)
        for mov_carn in range(carn_migrating_len):
            try:
                moving_animal = cells[cell].carn_migrate.pop(0)
            except IndexError:
                print("IndexError in logic::season_migration::mov_carn")
                break
            if tuple(moving_animal.var["coord"]) not in moving_animals["pred"]:
                moving_animals["pred"][tuple(moving_animal.var["coord"])] = [moving_animal]
            else:
                moving_animals["pred"][tuple(moving_animal.var["coord"])].append(moving_animal)
    # moving animals, possibaly her shit hit the fan
    for mov_herb in moving_animals["herb"]:
        cells[mov_herb].herb_default.extend(moving_animals["herb"][mov_herb])
    for mov_carn in moving_animals["pred"]:
        cells[mov_carn].carn_default.extend(moving_animals["pred"][mov_carn])



def season_aging(*animals : list):
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
            animals.loss_weight()


def season_death(cell, herb: list, carn: list):
    """
    for loop outside of function that check every cell and animals:list = cells.herb_default of that cell
    death = yes if w = 0
        else
        death = omega(1 - Phi)
    """
    [B.death() for B in herb]
    cell.herb_default = [A for A in herb if A.var["life"]]

    [B.death() for B in carn]
    cell.carn_default = [A for A in carn if A.var["life"]]


def yearly_cycle(end_year=10, visual_year=1):
    """
    1. generation of cells
    2. loop through the year
    """
    gen_cells()
    cells = gen_cells()
    cells[0].herb_default = [herbavor(0, 8.0), herbavor(0, 8.0), herbavor(0, 8.0)]
    start_year = 0
    while start_year < end_year:
        for c in cells:
            c.count_herb()
            season_feeding(800, 300, c, c.herb_default)

        for c in cells:
            season_breeding(c.herb_default, c.carn_default)

        season_migration(cells)

        for c in cells:
            season_aging(c.herb_default, c.carn_default)

        for c in cells:
            season_loss(c.herb_default, c.carn_default)

        for c in cells:
            season_death(c, c.herb_default, c.carn_default)

        start_year += 1
        if start_year % visual_year == 0:
            # print(f"{Fore.RED}Current year{Style.RESET_ALL}", start_year)
            if len(cells[0].herb_default) > 0:
                for a in cells[0].herb_default:
                    print("Age", a.var["a"])
                    print("Weight", a.var["w"])
                    print("Fitness", a.var["sigma"])
                    print("Alive", a.var["life"])

"""
if __name__ == '__main__':
    this_fucking_thing = BioSim(island_map = "WWWW\nWLLW\nWWWW", ini_pop = [{'loc':(2,2) , 'pop':[ {"species":"herbivore","age":5,"weight":20} for _ in range(10)] } ] , seed = 1234)
    the_map = this_fucking_thing.island
    illigal_moves = this_fucking_thing.illigal_coord
    for _ in range(30):
        season_migration(the_map,illigal_moves)
    for cell in the_map:
        print("coord:",the_map[cell].coord,"animals:",the_map[cell].herb_default)
        for C in the_map[cell].herb_default:
            print(C.var["coord"], C.var["a"]) """
