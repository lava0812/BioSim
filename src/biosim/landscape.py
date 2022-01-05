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
        self.fodder = 0

    def population_update(self, pop_list):
        """
        Append to list
        """
        for herbivores in pop_list:
            self.population.append(Herbivores(age=herbivores["age"], weight=herbivores["weight"]))

    def disp_population(self):
        """
        This function will display the number of herbivores
        """

        return len(self.population)

    def death(self):
        """
        Removing the animals that have died from the count

        I'm thinking about having an if statement here,
        with the pop() method that removes animals with weight = 0 from the list
        """

        pass

    def new_babies(self):
        """
        Adding the newborn babies to the population count

        Will append to the population list  --> make own list then fusion it or add directly to the population list
        """

        pass

    def new_fodder(self):
        """
        Function to add fixed amount of fodder in the lowland
        """
        self.fodder = self.parameters["f_max"]

    def eat(self):
        """
        This part will calculate the amount of fodder, and will be
        reduced after the animal has consumed the fodder
        """
        pass

    def aging(self):
        """
        This function will iterate through all the animals in the lowland cell(population list), and use the age()
         function from the animal class, and make the herbivores age.
        """