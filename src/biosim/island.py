__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import textwrap

from src.biosim.landscape import Lowland, Water


class Island:
    landscape_types = {"L": Lowland, "W": Water}

    def __init__(self, map=None, initial_population=None):

        self.ini_herbs = []
        self.ini_carns = []
        self.initial_population = initial_population

        if self.initial_population is None:
            self.initial_population = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                                       {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
                                       {'species': 'Herbivore', 'age': 5, 'weight': 8.1},
                                       {'species': 'Carnivore', 'age': 10, 'weight': 12.5},
                                       {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                                       {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]
        else:
            self.initial_population = initial_population

        if map is None:
            map = """\
               WWW
               WLW
               WWW"""

        self.geogr = textwrap.dedent(map)
        self.lines = self.geogr.splitlines()
        self.map = []

    def map_input(self):
        """
        Started on the map_input method here. This will take care of the error messages if
        something is wrong with the input the user have put in.
        """

    def create_map(self):
        """
        Here we create the actual map of the island.
        It can be useful to use two for loops here.
        """
        for rows in self.lines:
            row = []
            for column in rows:
                if column == "W":
                    row.append(Water())
                elif column == "L":
                    row.append(Lowland())
                else:
                    raise ValueError("This is not a valid landscape type. Try again!")
            self.map.append(row)

        # loc = (2, 2)
        # self.map[loc(0) - 1][loc(1) - 1].add_pop(pop)  # This is how the function should be used
        # to access the coordinates(2,2)

    def map_boundaries(self):
        """
        Here we define the boundaries of the map.
        """
        pass

    def set_new_parameters(self):
        """
        Give user the option to set parameters themselves.
        """
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
        Check how many animals there are on a cell, this is for both herbivores and carnivores
        """

    def migrate(self):
        """
        This function gives the animals the ability to move from one cell to another
        """
        pass

    def annual_cycle(self):
        """
        Content of function:
        1. Growth of food
        2. Herbivores eat
        3. Carnivores eat
        4. Herbivores and carnivores give birth
        5. Animals migrate(not relevant atm)
        6. Animals becomes one year older
        7 Animals lose weight
        8. Determining whether animals die or not.
        """
        pass
