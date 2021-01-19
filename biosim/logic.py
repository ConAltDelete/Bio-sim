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
    ´´season_feeding´´ goes over the animals ´´Herbivore´´, and ´´Carnivore´´ (in that order) and feeds them.
    The Herbivore eats off the cell while Carnivore eats Herbivore after they have eaten.

    :param Cells cell: The cell of the island.
    """
    except_list = ["Herbivore", "Carnivore"]
    herb_test = "Herbivore" in cell.default and len(cell.default["Herbivore"]) != 0
    carn_test = "Carnivore" in cell.default and len(cell.default["Carnivore"]) != 0

    # assumes single cell given, otherwise put in loop
    if herb_test:
        ran.shuffle(cell.default["Herbivore"])
        for animals in cell.default["Herbivore"]:
            if cell.food > 0:
                animals.eat(cell)
            else:
                cell.food = 0
                break
    if carn_test and herb_test:
        # We need to sort the list so the fittest goes first. #
        cell.default["Carnivore"].sort(key=lambda o: o.var["phi"], reverse=True)
        for animals in cell.default["Carnivore"]:
            if all(not H.var["life"] for H in cell.default["Herbivore"]):
                break  # Time saver, but `predator` object can distinguish between dead animal and an alive one.
            # replace original list with new list with not dead animals#
            animals.eat(cell)
    # Resets the food in the cell since we are done for the year. If 
    # feeding season happens multiple times per year, or irregularly
    # , it must either be done at the last iteration of feeding, or
    # create a 'end of the year' season that handles anything that must
    # be reset at the end of the year. #
    for species in [A for A in cell.default if A not in except_list]:
        for animals in cell.default[species]:
            animals.eat(cell)


def season_breeding(cell: Cells):
    """
    ``season_breeding`` goes through all of the species in the cell and tells them to give birth.

    :param Cells cell: Cells object.
    """

    for species in cell.default:
        new_born = []
        # Since we are going do this multiple times, we're going
        # to just calculate the length once. #
        len_species = len(cell.default[species])
        for animals in cell.default[species]:
            new_born.append(animals.birth(len_species))
        new_born = [n for n in new_born if n is not None]  # N1
        cell.default[species].extend(new_born)


def season_migration(cells: dict, illegal_moves: list):
    """
    Animals moves to desired location if possible, else they don't move from cell and remain in ´´Cells.default´´.


    :param Cells cells: dictionary with coordinates as key, and Cells objects as value
    :param illegal_moves: list with coordinates values which animals can't move to

    .. note::
        N1: we pre-calculate the length since we manipulate the lists
        N2: This is strictly not necessary, but if it happens; There is a bug somewhere.
        N3: Just a safety precaution. Better safe than sorry.
    """
    moving_animals = dict()
    for cell in cells:
        cells[cell].migration(illegal_moves)
        mig_len = {species: len(cells[cell].migrate[species]) for species in cells[cell].migrate}  # N1
        mig_n = 0
        for species in cells[cell].migrate:
            while mig_n < mig_len[species]:
                try:
                    moving_animal = cells[cell].migrate[species].pop(0)
                except IndexError:  # N2
                    raise ValueError(
                        "IndexError in logic::season_migration::cells[cell].migrate, length of array changed.")
                # if this is a new species, we will remember it in the future.#
                if species not in moving_animals:
                    moving_animals[species] = dict()

                if tuple(moving_animal.var["coord"]) not in moving_animals[species]:
                    moving_animals[species][tuple(moving_animal.var["coord"])] = [moving_animal]
                else:
                    moving_animals[species][tuple(moving_animal.var["coord"])].append(moving_animal)
                mig_n += 1
            mig_n = 0
    for species in moving_animals:
        for coord in moving_animals[species]:
            if species not in cells[coord].default:
                cells[coord].default[species] = moving_animals[species][coord]
            else:
                cells[coord].default[species].extend(moving_animals[species][coord])
            moving_animals[species][coord] = list()  # N3


def season_ageing(cell: Cells):
    """
    ´´season_ageing´´ goes through all of the species and tells them to get old.

    :param Cells cell: Cells object.
    """

    for species in cell.default:
        for animals in cell.default[species]:
            animals.age()
            animals.loss_weight()
            animals.death()
        cell.default[species] = [animals for animals in cell.default[species] if animals.var["life"]]


def season_end(island: dict):
    """
    Does 'end of season' procedure. Anything that needs manual wrap-up get done here.


    :param island: the entire island.
    """
    for coord in island:
        island[coord].food = float(island[coord].f_max)
        island[coord].count()


def year_cycle(island, illegal_coords):
    """
    Simulates an entire year on the island.


    :param island: The map of the island.
    :param illegal_coords: Every coordinates that an animal can't walk on.
    """

    for c in island:
        season_feeding(island[c])
        season_breeding(island[c])

    season_migration(island, illegal_coords)

    for c in island:
        season_ageing(island[c])

    season_end(island=island)
