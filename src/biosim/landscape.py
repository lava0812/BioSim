# -*- encoding: utf-8 -*-

"""
This file wll contain a main class Landscape(Superclass). The Landscape class will have four subclasses, Highland,
Lowland, Desert and Water.
"""
__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.animals import Animal, Herbivore
import random


class Landscape:
    parameters = {"f_max": 800}

    def __init__(self):
        """
        Empty list to count the population.
        Food count starts at 0 which will be updated
        """
        self.herb = []
        self.carni = []
        self.fodder = self.parameters["f_max"]
        self.kill_p = None

    def population_update(self, pop_list):
        """
        Append to list
        """
        for individuals in pop_list:
            if individuals["species"] == "Herbivore":
                self.herb.append(Animal(age=individuals["age"], weight=individuals["weight"]))

    def display_herb(self):
        """
        This function will display the number of herbivores
        """
        return len(self.herb)

    def display_carni(self):
        """
        This function will display the number of carnivores
        """
        return len(self.carni)

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
        for individuals in self.herb:
            individuals.aging()

    def eat_fodder(self):
        """
        Function to reduce the fodder
        Using random shuffle to let the herbivores eat in a random order
        """
        random.shuffle(self.herb)
        for individuals in self.herb:

            if self.fodder >= individuals.param["F"]:
                individuals.weight_increase_herb(individuals.param["F"])
                self.fodder -= individuals.param["F"]

            elif self.fodder < individuals.param["F"]:
                individuals.weight_increase_herb(self.fodder)
                self.fodder = 0

            elif self.fodder == 0:
                break

    def death_population(self):
        """
        Remove the animals that have died from the population list
        """
        self.herb = [individuals for individuals in self.herb if not individuals.death_animal()]

    def newborn(self):
        """
        Adding the newborn babies to the population list
        Making a new list, then we can extend the population list
        """
        individuals_count = len(self.herb)

        if individuals_count < 2:
            return None

        newborn_individuals = []
        if individuals_count >= 2:
            for individuals in self.herb:
                newborn = individuals.birth(individuals_count)
                if newborn is not None:
                    newborn_individuals.append(newborn)
        self.herb.extend(newborn_individuals)

    def weight_loss(self):
        """
        The annual weight loss every year
        """

        for individuals in self.herb:
            return individuals.weight_decrease()

    def prey(self, carnivores):

        shuffled_carnivores = random.shuffle(self.carni)
        carnivore = shuffled_carnivores[0]
        herbivore = Herbivore(Animal)
        if carnivore.fitness <= herbivore.fitness:
            self.kill_p = 0


    def simulate(self):
        self.new_fodder()
        self.eat_fodder()
        self.death_population()
        self.newborn()
        self.weight_loss()
        self.aging_population()


class Lowland(Landscape):
    """
    Lowland
    """
    parameters = {"f_max": 800}

    def __init__(self):
        super().__init__()


class Water(Landscape):
    """
    Water
    """
    parameters = {"f_max": 0}

    def __init__(self):
        super().__init__()



L = Landscape()
L.herb = [Animal(5, 20) for i in range(50)]
for i in range(100):
    L.simulate()
    print(len(L.herb), L.fodder)
