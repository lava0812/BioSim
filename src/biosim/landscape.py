"""
This file wll contain a main class Landscape(Superclass). The Landscape class will have four subclasses, Highland,
Lowland, Desert and Water.
"""
__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.animals import Herbivore
import random


class Lowland:
    parameters = {"f_max": 800}

    def __init__(self):
        """
        Empty list to count the population.
        Food count starts at 0 which will be updated
        """
        self.population = []
        self.fodder = self.parameters["f_max"]

    def population_update(self, pop_list):
        """
        Append to list
        """
        for individuals in pop_list:
            if individuals["species"] == "Herbivore":
                self.population.append(Herbivore(age=individuals["age"], weight=individuals["weight"]))

    def display_population(self):
        """
        This function will display the number of herbivores
        """

        return len(self.population)

    def new_fodder(self):
        """
        Function to add fixed amount of fodder in the lowland
        """
        self.fodder = self.parameters["f_max"]

    def aging_population(self):
        """
        A method for aging all the herbivores in the lowland cell.
        """

        # herbivore = Herbivore()
        for individuals in self.population:
            individuals.aging()

    def eat_fodder(self):
        """
        Function to reduce the fodder
        """
        random.choice(self.population)
        herbivore = Herbivore()
        for individuals in self.population:
            individuals.weight_increase(Lowland.new_fodder())

    def death_population(self):
        """
        Remove the animals that have died from the population list
        """
        self.population = [individuals for individuals in self.population if not Herbivore.death_herbivore()]

    def newborn(self):
        """
        Adding the newborn babies to the population list
        """
        if len(self.population) < 2:
            return False

        if len(self.population) >= 2:
            for herbivores in self.population:
                return None

    def weight_loss(self):
        """
        The annual weight loss every year
        """

        for individuals in self.population:
            return individuals.weight_decrease()

#   def simulate(self):
#        for individuals in self.population:
#            individuals.feed()
#            if individuals.birth():
#                pass
#            if individuals.death():
#                return [herbivores for herbivores in self.population if not individuals.death()]
#            individuals.age()
