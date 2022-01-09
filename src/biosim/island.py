__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.landscape import Landscape, Lowland, Water
from src.biosim.animals import Animal, Herbivore, Carnivore


class Island:
    landscape_types = {"L": Lowland, "W": Water}

    def __init__(self, map, ini_population=None):
        self.ini_herbs = []
        self.ini_carns = []
        self.map = {}
        self.ini_population = ini_population

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

    def create_map(self):
        pass

    def map_boundaries(self):
        pass
