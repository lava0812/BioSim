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
        Using random shuffle to let the herbivores eat in a random order
        """
        random.shuffle(self.population)
        for individuals in self.population:

            if self.fodder >= individuals.param_herbivores["F"]:
                individuals.weight_increase(individuals.param_herbivores["F"])
                self.fodder -= individuals.param_herbivores["F"]

            if self.fodder < individuals.param_herbivores["F"]:
                individuals.weight_increase(self.fodder)
                self.fodder = 0

            if self.fodder == 0:
                break

    def death_population(self):
        """
        Remove the animals that have died from the population list
        """
        self.population = [individuals for individuals in self.population if not individuals.death_herbivore()]

    def newborn(self):
        """
        Adding the newborn babies to the population list
        Making a new list, then we can extend the population list
        """
        individuals_count = len(self.population)

        if individuals_count < 2:
            return None

        newborn_individuals = []
        if individuals_count >= 2:
            for individuals in self.population:
                newborn = individuals.birth_herbivore_probability(individuals_count)
                if newborn is not None:
                    newborn_individuals.append(newborn)
        self.population.extend(newborn_individuals)

    def weight_loss(self):
        """
        The annual weight loss every year
        """

        for individuals in self.population:
            return individuals.weight_decrease()

    def simulate(self):
        self.new_fodder()
        self.eat_fodder()
        self.death_population()
        self.newborn()
        self.weight_loss()
        self.aging_population()


