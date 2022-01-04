"""
This file wll contain a main class Landscape(Superclass). The Landscape class will have four subclasses, Highland,
Lowland, Desert and Water.
"""
from animals import Herbivores


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

        return self.population

    def pop(self):
        """
        This function will add values to the empty list
        """
        return len(self.population)
        pass

    def death(self):
        """
        Removing the animals that have died from the count
        """
        pass

    def new_babies(self):
        """
        Adding the newborn babies to the population count
        """
        pass

    def new_fodder(self):
        """
        Function to add fixed amount of fodder in the lowland
        """
        self.fodder = self.parameters["f_max"]
        pass

    def eat(self):
        """
        This part will calculate the amount of fodder, and will be
        reduced after the animal has consumed the fodder
        """
        pass
