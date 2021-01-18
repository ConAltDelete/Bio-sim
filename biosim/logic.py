# -*- coding: utf-8 -*-

"""
functioning logic of the island simulation
"""

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'

from .island import Cells
from .animal import *

def season_feeding(cell: Cells):
    """
    ´´season_feeding´´ goes over the animals ´´Herbivore´´, and ´´Carnivore´´ (in that order) and feeds them. The Herbavore eats off the cell while Carnivore eats Herbivore after they have eaten.

    :param Cells cell: The cell of the island.
    """
    herb_test = "Herbivore" in cell.default and len(cell.default["Herbivore"]) != 0
    carn_test = "Carnivore" in cell.default and len(cell.default["Carnivore"]) != 0

    # assums single cell given, othervise put in loop
    if herb_test:
        ran.shuffle(cell.default["Herbivore"])
        for animal in cell.default["Herbivore"]:
            if cell.food > 0:
                cell.food -= animal.eat(cell.food, return_food=True)
            else:
                cell.food = 0
                break
    if carn_test and herb_test:
        # We need to sort the list so the fittest goes first. #
        cell.default["Carnivore"].sort(key=lambda O: O.var["phi"],reverse = True)
        for animal in cell.default["Carnivore"]:
            if all( not H.var["life"] for H in cell.default["Herbivore"]):
               break # Timesaver, but `preditor` object can distigvish between dead animal and an alive one.
            # replace original list with new list with not dead animals#
            cell.default["Herbivore"] = [ h for h in animal.eat(cell.default["Herbivore"]) if h.var["life"]] 
    # Resets the food in the cell since we are done for the year. If 
    # feeding seson happens multiple times per year, or irregulary
    # , it must either be done at the last iteration of feeding, or
    # create a 'end of the year' seson that handels anything that must
    # be reset at the end of the year. #

def season_breeding(cell: Cells):
    """
    ``season_breeding`` goes through all of the species in the cell and tells them to give birth.

    :param Cells cell: Cells object.
    """

    for spesis in cell.default:
        new_born = []
        # Since we are going do this multiple times, we'r going
        # to just calculate the length once. #
        len_spesis = len(cell.default[spesis])
        for animal in cell.default[spesis]:
            new_born.append(animal.birth(len_spesis))
        new_born = [n for n in new_born if n != None] # N1
        cell.default[spesis].extend(new_born)



def season_migration(cells: dict, illigal_moves: list):
    """
    Animals moves to desired location if possible, else they don't move from cell and remain in ´´Cells.default´´.
    :param dict[tuple[int,int] : Cells] cells: dictonary with coordinats as key, and Cells objects as value

    .. note::
        N1: we pre-calculate the length since we manipulate the lists
        N2: This is strictly not nessesery, but if it happens; There is a bug somwhere.
        N3: Just a safty percausion. Better safe than sorry.
    """
    moving_animals = dict()
    for cell in cells:
        cells[cell].migration(illigal_moves)
        mig_len = {spesis: len(cells[cell].migrate[spesis]) for spesis in cells[cell].migrate} # N1
        for spesis in cells[cell].migrate:
            for _ in range(mig_len[spesis]):
                try:
                    moving_animal = cells[cell].migrate[spesis].pop(0)
                except IndexError: # N2
                    raise ValueError("IndexError in logic::season_migration::cells[cell].migrate, lenght of array changed.")
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
            moving_animals[spesis][coord] = list() # N3



def season_ageing(cell: Cells):
    """
    ´´season_ageing´´ goes through all of the species and tells them to get old.

    :param Cells cell: Cells object.
    """

    for spesis in cell.default:
        for animal in cell.default[spesis]:
            animal.age()
            animal.loss_weight()
            animal.death()
        cell.default[spesis] = [animal for animal in cell.default[spesis] if animal.var["life"]]

def season_end(island: dict):
    """
    Does 'end of season' procedure. Anything that needs manual wrap-up get done here.


    :param island: the entire island.
    """
    for coord in island:
        island[coord].food = float(island[coord].f_max)
        island[coord].count()

def year_cycle(island,illigal_coords):
    """
    

    :param dict[tuple[int,int]:Cells] island: The map of the island.
    :param list[tuple[int,int]]: Every coordinates that an animal can't walk on.
    :param int year: The current year.
    :param int visual_year: send data after n years.
    """

    for c in island:
        season_feeding(island[c])
        season_breeding(island[c])

    season_migration(island,illigal_coords)

    for c in island:
        season_ageing(island[c])

    season_end(island=island)


if __name__ == '__main__':
    pass
