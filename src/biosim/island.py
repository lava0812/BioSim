__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from .landscape import Lowland, Water


class Island:
    types = {"L": Lowland, "W": Water}

    def __init__(self, map, pop_ini):
        self.ini_herbs = []
        self.ini_carns = []
        pass
