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


def season_feeding(cell: Cells):
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

    # assums single cell given, othervise put in loop
    if "herbivore" in cell.default and len(cell.default["herbivore"]) != 0:
        ran.shuffle(cell.default["herbivore"])
        for animal in cell.default["herbivore"]:
            if cell.food > 0:
                cell.reduce_food(animal.eat(cell.food, return_food=True))
            else:
                break
    if "carnivore" in cell.default and len(cell.default["carnivore"]) != 0:
        cell.default["carnivore"].sort(key=lambda O: O.var["sigma"],reverse = True)
        for animal in cell.default["carnivore"]:
            if all( not H.life for H in cell.default["herbivore"]):
               break # Timesaver, but `preditor` object can distigvish between dead animal and an alive one.
            cell.herb_default = [ h for h in animal.eat(cell.default["herbivore"]) if h.var["life"]] # replace original list with new list with not dead animals


def season_breeding(cell: Cells):
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

    for spesis in cell.default:
        new_born = []
        len_spesis = len(cell.default[spesis])
        for animal in cell.default[spesis]:
            new_born.append(animal.birth(len_spesis))
        new_born = [n for n in new_born if n != None]
        cell.default[spesis].extend(new_born)



def season_migration(cells: dict, illigal_moves: list):
    """
    Animals moves to desired location if possible, else they don't move from cell.
    :param cells: dictonary with coordinats as key, and Cells objects as value
    :return:
    """
    moving_animals = dict()
    for cell in cells:
        cells[cell].migration(illigal_moves)
        mig_len = {spesis: len(cells[cell].migrate[spesis]) for spesis in cells[cell].migrate}
        for spesis in cells[cell].migrate:
            for _ in range(mig_len[spesis]):
                try:
                    moving_animal = cells[cell].migrate[spesis].pop(0)
                except IndexError:
                    print("IndexError in logic::season_migration::cells[cell].migrate")
                    break
                # if this is a new spesis, we will remember it in the future.#
                if spesis not in moving_animals:
                    moving_animals[spesis] = dict()

                if tuple(moving_animal.var["coord"]) not in moving_animals[spesis]:
                    moving_animals[spesis][tuple(moving_animal.var["coord"])] = [moving_animal]
                else:
                    moving_animals[spesis][tuple(moving_animal.var["coord"])].append(moving_animal)
        for spesis in moving_animals:
            for coord in moving_animals[spesis]:
                if spesis not in cells[coord].default:
                    cells[coord].default[spesis] = moving_animals[spesis][coord]
                else:
                    cells[coord].default[spesis].extend(moving_animals[spesis][coord])
                moving_animals[spesis][coord] = list()



def season_aging(cell: Cells):
    """
    for loop outside of function that check every cell and animals:list = cells.herb_default of that cell
    age += 1
    """

    for spesis in cell.default:
        for animal in cell.default[spesis]:
            animal.age()


def season_loss(cell: Cells):
    """
    for loop outside of function that check every cell and animals:list = cells.herb_default of that cell
    w -= eta * w
    """
    for species in cell.default:
        for animals in cell.default[species]:
            for animal in animals:
                animal.loss_weight()


def season_death(cell: Cells):
    """
    for loop outside of function that check every cell and animals:list = cells.herb_default of that cell
    death = yes if w = 0
        else
        death = omega(1 - Phi)
    """
    for spesis in cell.default:
        for animal in cell.default[spesis]:
            animal.death()
    for spesis in cell.default:
        cell.default[spesis] = [animal for animal in cell.default[spesis] if animal.var["life"]]


def yearly_cycle(end_year=10, visual_year=1):
    """
    1. generation of cells
    2. loop through the year
    """
    gen_cells()
    cells = gen_cells()
    cells[0].herb_default = [herbivore(0, 8.0), herbivore(0, 8.0), herbivore(0, 8.0)]
    start_year = 0
    while start_year < end_year:
        for c in cells:
            season_feeding(c)

        for c in cells:
            season_breeding(c)

        season_migration(cells)

        for c in cells:
            season_aging(c)

        for c in cells:
            season_loss(c)

        for c in cells:
            season_death(c)

        start_year += 1
        if start_year % visual_year == 0:
            # print(f"{Fore.RED}Current year{Style.RESET_ALL}", start_year)
            if len(cells[0].herb_default) > 0:
                for a in cells[0].herb_default:
                    print("Age", a.var["a"])
                    print("Weight", a.var["w"])
                    print("Fitness", a.var["sigma"])
                    print("Alive", a.var["life"])


if __name__ == '__main__':
    pass
