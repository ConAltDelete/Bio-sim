# -*- coding: utf-8 -*-

__author__ = 'Roy Erling Granheim, Mats Hoem Olsen'
__email__ = 'roy.erling.granheim@nmbu.no, mats.hoem.olsen@nmbu.no'


class Cells:
    """
    The ``Cells`` class keeps track of information of the cells on the island.
    """
    default_food = {
        0: 0,
        1: 0,
        2: 300,
        3: 800
    }

    def __init__(self, cell_type: int, coord=None, names: list = None):
        """
        :param int cell_type: Describes the cell type as an integer.
        :param list/None coord: Tells the cell where it is on the map. The default value is ``[0,0]``.
        :param list[str] names: ``names`` contain the names of all species on the island.
        """
        self.coord = coord if coord is not None else [0, 0]
        self.count_species = dict() if not names else {species: 0 for species in names}
        self.count_age = {species: [] for species in names}
        self.count_weight = {species: [] for species in names}
        self.count_fitness = {species: [] for species in names}
        self.type = cell_type
        self.f_max = float(Cells.default_food[self.type])
        self.food = self.f_max
        self.default = dict()
        self.migrate = dict()

    def migration(self, illegal_moves):
        """
        Animals in the cell get the opportunity to move to
        another cell.


        :param list[tuple[int,int]] illegal_moves: a list of tuples with illegal cells
        """
        # We tell the animal to move to a reasonable spot#
        for species in self.default:
            for animals in self.default[species]:
                animals.var["coord"] = list(self.coord)
                animals.move(illegal_moves)
        # Now we check if it moves, if it does we move it, else ignore it.#
        for species in self.default:
            len_animal = len(self.default[species])
            for _ in range(len_animal):
                animals = self.default[species].pop(0)
                if tuple(animals.var["coord"]) != tuple(self.coord):
                    if species in self.migrate:
                        self.migrate[species].append(animals)
                    else:
                        self.migrate[species] = [animals]
                else:
                    self.default[species].insert(-1, animals)

    def count(self):
        """
        Counts the number of animals in the cell per species.
        """
        self.count_age = {species: [] for species in self.count_age}
        self.count_weight = {species: [] for species in self.count_weight}
        self.count_fitness = {species: [] for species in self.count_fitness}
        for species in self.default:
            self.count_species[species] = len(self.default[species])
            if len(self.default[species]) != 0:
                for animals in self.default[species]:
                    self.count_age[species].append(animals.var["a"])
                    self.count_weight[species].append(animals.var["w"])
                    self.count_fitness[species].append(animals.var["phi"])


if __name__ == '__main__':
    pass
