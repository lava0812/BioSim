# -*- encoding: utf-8 -*-

"""
This file wll contain a main class Landscape(Superclass). The Landscape class will have four subclasses, Highland,
Lowland, Desert and Water.
"""
__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import random

from src.biosim.animals import Animal


class Landscape:
    parameters = {"f_max": 800}

    def __init__(self):
        """
        Empty list to count the population.
        Food count starts at f_max which will be updated
        """
        self.param = None
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

        for individuals in pop_list:
            if individuals["species"] == "Carnivore":
                self.carni.append(Animal(age=individuals["age"], weight=individuals["weight"]))

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

    def total_pop(self):
        return self.herb + self.carni

    def new_fodder(self):
        """
        Function to add fixed amount of fodder in the lowland
        """
        self.fodder = self.parameters["f_max"]

    def aging_population(self):
        """
        A method for aging all the herbivores in the lowland cell.
        """

        for individuals in self.herb:
            individuals.aging()

        for individuals in self.carni:
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
        self.carni = [individuals for individuals in self.herb if not individuals.death_animal()]

    def newborn_herb(self):
        """
        Adding the newborn babies to the population list
        Making a new list, then we can extend the population list
        """
        individuals_count = len(self.herb)

        if individuals_count < 2:
            return False

        newborn_individuals = []
        if individuals_count >= 2:
            for individuals in self.herb:
                newborn = individuals.birth(individuals_count)
                if newborn is not None:
                    newborn_individuals.append(newborn)
        self.herb.extend(newborn_individuals)

    def newborn_carni(self):
        """
        Adding the newborn babies to the population list
        Making a new list, then we can extend the population list
        """
        individuals_count = len(self.herb)

        if individuals_count < 2:
            return False

        newborn_individuals = []
        if individuals_count >= 2:
            for individuals in self.carni:
                newborn = individuals.birth(individuals_count)
                if newborn is not None:
                    newborn_individuals.append(newborn)
        self.carni.extend(newborn_individuals)

    def weight_loss(self):
        """
        The annual weight loss every year
        """

        for individuals in self.herb:
            return individuals.weight_decrease()

        for individuals in self.carni:
            return individuals.weight_decrease()

    def prey(self, carnivores_list, herbivores_list):
        """
        Method for the prey of a herbivore by the carnivore.
        I have to add a way of calculating how much the carnivore has eaten.
        """
        # herbivores_newlist = sorted(herbivores_list, key=lambda x: "fitness", reverse=True)
        carnivores_newlist = random.shuffle(carnivores_list)
        carnivore = carnivores_newlist[0]
        herbivores_newlist = sorted(herbivores_list, key=lambda x: "fitness", reverse=True)

        #self.herb.sort(key=lambda x: "fitness", reverse=True)
        herbivores_lowest_fitness = self.herb[0]
        ate = 0

        if ate >= self.param["F"]:
            pass
        elif carnivore.fitness <= herbivores_lowest_fitness.fitness:
            self.kill_p = 0
        elif 0 < carnivore.fitness - herbivores_lowest_fitness.fitness < self.param["DeltaPhiMax"]:
            self.kill_p = (carnivore.fitness - herbivores_lowest_fitness.fitness) / self.param["DeltaPhiMax"]
            if self.kill_p > random.random():
                ate += herbivores_lowest_fitness.weight
                herbivores_lowest_fitness.death_animal()
                carnivore.fitness_animal()
        else:
            self.kill_p = 1

            carnivore.weight += self.param["beta"] * herbivores_lowest_fitness.weight
            ate += herbivores_lowest_fitness.weight
            herbivores_lowest_fitness.death_animal()
            carnivore.fitness_animal()

    def simulate(self):
        self.new_fodder()
        self.eat_fodder()
        self.death_population()
        self.newborn_herb()
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

# L = Landscape()
# L.herb = [Animal(5, 20) for i in range(50)]
# for i in range(1000):
#     L.simulate()
#     print(len(L.herb), L.fodder)
