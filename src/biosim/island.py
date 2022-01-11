__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import textwrap

from src.biosim.landscape import Landscape, Lowland, Water
from src.biosim.animals import Animal, Herbivore, Carnivore


class Island:
    landscape_types = {"L": Lowland, "W": Water}

    def __init__(self, map, initial_population=None):

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

        self.geogr = textwrap.dedent(map)
        self.lines = self.geogr.splitlines()

        if self.map is None:
            self.map = """\
               WWW
               WLW
               WWW"""
        else:
            self.map = {}

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

    def map_input(self):
        """
        Started on the map_input method here. This will take care of the error messages if
        something is wrong with the input the user have put in.
        """

    def create_map(self):

        pass

    def map_boundaries(self):
        pass

    def set_new_parameters(self):
        pass

    def map_lines(self):
        pass

