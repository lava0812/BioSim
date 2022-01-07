# -*- encoding: utf-8 -*-

"""
This file will contain a main class Animals(Superclass). This Animals class will contains methods for characteristics
that are common for both herbivores and carnivores. The Animals class will have to subclasses,
Herbivores and Carnivores.
These to subclasses will contain methods specifically for herbivores and carnivores.
"""
__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import math
import random


class Animal:
    param = {
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.6,
        "w_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0,
        "DeltaPhiMax": None
    }

    def __init__(self, age=None, weight=None):

        """
        Here we define our data for this function, and these are age and weight.
        """
        if age is None:
            self.age = 0
        else:
            self.age = 0

        if weight is None:
            self.weight = self.weight_baby()
        else:
            self.weight = weight

        # self.age = age
        # self.weight = weight
        self.fitness = None
        self.fitness_animal()
        # self.probability_birth = None
        # self.probability_die = None
        self.death = False

    def aging(self):
        """
        Aging the animals.
        """
        self.age += 1
        self.fitness_animal()

    # @classmethod
    def weight_baby(self):
        """
        Using a Gaussian distribution for determining the weight of a newborn baby. In the
        Gaussian(normal distribution), w_birth is the mean value, and sigma_birth is our standard deviation.
        """
        # The random.gauss function will go as a return statement.
        weight = random.gauss(self.param["w_birth"], self.param["sigma_birth"])
        return weight

    # def weight_increase(self, fodder):
    #     """
    #     This method will increase the weight of the herbivores once it eats some fodder F. It will increase with
    #     beta times the amount of fodder it eats.
    #     """
    #     self.weight += self.param["beta"] * fodder
    #     self.fitness_animal()
    #
    def weight_decrease(self):
        """
        Decrease the weight of an animal, which will happen every year.
        Updates the fitness right after.
        """
        self.weight -= self.weight * self.param["eta"]  # Can put this in aging
        self.fitness_animal()

    def fitness_animal(self):
        """
        Calculate the fitness of an animal.
        ------------------------------
        Param:
        age, weight
        """
        q_positive = 1 / (1 + math.exp((self.param["phi_age"])
                                       * (self.age - self.param["a_half"])
                                       ))
        q_negative = 1 / (1 + math.exp((-self.param["phi_weight"])
                                       * (self.weight - self.param["w_half"])
                                       ))
        if self.weight <= 0:
            self.fitness = 0
        else:
            self.fitness = q_positive * q_negative

    def death_animal(self):
        """
        Death of an animal, using probability.
        """
        probability_die = self.param["omega"] * (
                1 - self.fitness)  # Herbivore will die with a probability of w(1-fitness)

        if self.weight == 0:  # Retta på fra =< til ==
            self.death = True  # Herbivore dies with certainty
        elif probability_die >= random.random():
            self.death = True
        return self.death

    def birth(self, n_herbivore):
        """
        Probability to give birth for an animal.
        """
        probability = min(1, Animal.param["gamma"] * self.fitness * (n_herbivore - 1))
        if random.random() < probability:
            weight = random.gauss(self.param["w_birth"], self.param["sigma_birth"])
            born_baby = type(self)(0, int(weight))  # Herbivore()

            if self.weight < born_baby.weight * self.param["xi"]:
                return None
            else:
                self.weight -= born_baby.weight * self.param["xi"]
                return born_baby

    # def birth_weight_loss(self):
    #     """
    #     This method makes the herbivore mother lose a weight of zeta times the weight of the baby.
    #     """
    #     self.weight -= self.weight_baby() * self.param_herbivores["xi"]


class Herbivore(Animal):

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)

    def weight_increase(self, fodder):
        """
        Increasing the weight of a herbivore once it eats some fodder F.
        """
        self.weight += self.param["beta"] * fodder
        self.fitness_animal()


class Carnivore(Animal):
    param = {
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.6,
        "w_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0,
        "DeltaPhiMax": None
    }

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)
        self.kill_p = None




    def kill_herbivore(self):
        """
        Create a method for killing a herbivore.
        """


        pass
