"""
This file wll contain a main class Landscape(Superclass). The Landscape class will have four subclasses, Highland,
Lowland, Desert and Water.
"""
__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from animals import Herbivores
# import random


class Lowland:
    parameters = {"f_max": 800}

    def __init__(self):
        """
        Empty list to count the population.
        Food count starts at 0 which will be updated
        """
        self.population = []
        self.fodder = self.parameters["f_max"]



    def population_update(self, pop):
        """
        Append to list
        """
        for herbivores in pop:
            self.population.append(Herbivores(age=herbivores["age"], weight=herbivores["weight"]))

    def disp_population(self):
        """
        This function will display the number of herbivores
        """

        return len(self.population)


    def new_fodder(self):
        """
        Function to add fixed amount of fodder in the lowland
        """
        self.fodder = self.parameters["f_max"]


    def simulate(self):
        for every_animal in self.population:
            every_animal.feed()
            if every_animal.birth():
                pass
            every_animal.death(len(self.population))




