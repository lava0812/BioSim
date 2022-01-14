# -*- encoding: utf-8 -*-

__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import textwrap

from src.biosim.landscape import Lowland, Water, Highland, Desert


class Island:
    landscape_types = {"L": Lowland, "W": Water, "H": Highland, "D": Desert}

    def __init__(self, map_of_island=None):

        self.ini_herbs = []
        self.ini_carns = []

        if map_of_island is None:
            map_of_island = """\
               WWW
               WLW
               WWW"""

        self.geogr = textwrap.dedent(map_of_island)
        self.lines = self.geogr.splitlines()
        self.map = {}
        self.create_map()

    def map_input(self):
        """
        Started on the map_input method here. This will take care of the error messages if
        something is wrong with the input the user have put in.
        """
        # Dont know if we need this.

    def create_map(self):
        """
        Here we create the actual map of the island.
        It can be useful to use two for loops here.
        """
        self.map_lines()
        self.map_boundaries()
        for i, rows in enumerate(self.lines):
            for j, column in enumerate(rows):
                if column == "W":
                    self.map[(i + 1, j + 1)] = Water()
                elif column == "L":
                    self.map[(i + 1, j + 1)] = Lowland()
                elif column == "H":
                    self.map[(i + 1, j + 1)] = Highland()
                elif column == "D":
                    self.map[(i + 1, j + 1)] = Desert()
                else:
                    raise ValueError("This is not a valid landscape type. Try again!")

        for loc, cell in self.map.items():
            neighbor_loc = (loc[0], loc[1] - 1), \
                           (loc[0], loc[1] + 1), \
                           (loc[0] - 1, loc[1]), \
                           (loc[0] + 1, loc[1])

            for n_loc in neighbor_loc:
                neighbor_cell = self.map.get(n_loc)
                if neighbor_cell is not None:
                    cell.neighbors.append(neighbor_cell)

    def map_boundaries(self):
        """
        Here we define the boundaries of the map.
        """
        # fix this function, check on geogr instead
        for row in self.lines[0] + self.lines[-1]:
            for elements in row:
                if elements != "W":
                    raise ValueError("The inputted map is not surrounded by water. Try again!")

        for row in self.lines:
            for i in range(len(row[0])):
                if row[0][i] != "W" and row[-1][i] != "W":
                    raise ValueError("The inputted map is not surrounded by water. Try again!")

    def set_new_parameters(self):
        """
        Give user the option to set parameters themselves.
        """
        # I dont know if we need to do this.
        pass

    def map_lines(self):
        """
        Check if the map lines are the equal length.
        """

        for line in self.lines:
            if len(self.lines[0]) != len(line):  # len(self.lines[0]) != len(self.lines[1])
                raise ValueError("All the lines on the map should have equal lengths!")
            else:
                pass

    def population_cell(self, population):
        """
        Check how many animals there are in a cell, for both herbivores and carnivores
        """
        for item in population:
            population = item["pop"]
            loc = item["loc"]

            self.map[loc].population_update(population)

    def annual_cycle(self):
        """
        This method will run the annual cycle method, which is used in landscape.
        """

        for cell in self.map.values():
            cell.annual_cycle()
        pass
# in island, we move the animals from one cell to another cell. move only if the cell is not water.
# after we move, we change self.migrate to true, this is for checking if it has migrated.
# get fitness, age and weight of all animals in the map.
# get herbivore population in each location.
