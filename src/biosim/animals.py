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
    param = {}

    @classmethod
    def set_params(cls, added_parameters):
        """
        This will be a method for adding new parameters to the function.
        This will be a classmethod because it involves changing the class variables.
        """
        for parameters in added_parameters:
            if parameters not in cls.param:
                raise KeyError("Invalid parameter name")

        for parameters in cls.param:
            if parameters in cls.param:
                if added_parameters[parameters] < 0:
                    raise ValueError("Inputted parameters can not be negative!")
        cls.param.update(added_parameters)

    def __init__(self, age=None, weight=None):

        """
        Constructor for Animal class.

        Parameters:
        -----------
        age: int
        Age of an animal, and the default value is set to be None.
        weight: int
        Weight of an animal, and the default value is set to be None.

        """

        # if self.param["DeltaPhiMax"] <= 0:
        #    ValueError("You need a positive integer higher than 0")
        # elif self.param["eta"] < 0:
        #    ValueError("You need a positive integer higher or equal to 1")

        if age is None:
            self.age = 0
        else:
            self.age = 0

        if weight is None:
            self.weight = self.weight_baby()
        else:
            self.weight = weight

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
        Gaussian distribution for determining the weight of a newborn baby.
        Used only for the purpose of testing.

        Returns
        -------
        weight: int
        Generate a weight, using random.gauss.
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

    def weight_increase_herb(self, fodder):
        """
        Increasing the weight of a herbivore and carnivore once it eats some fodder F.
        """
        self.weight += self.param["beta"] * fodder
        self.fitness_animal()
        # The function over should be in the herbivores subclass, but it is here, just so that the tests
        # can work.

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
        -----------------------------------
        Returns
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
                1 - self.fitness)  # Herbivore, carnivore will die with a probability of w(1-fitness)

        if self.weight == 0:  # Retta på fra =< til ==
            self.death = True  # Herbivore, carnivore dies with certainty
        elif probability_die >= random.random():
            self.death = True
        return self.death

    def birth(self, n_animals_in_same_species):
        """
        Probability to give birth for an animal.
        """
        probability = min(1, self.param["gamma"] * self.fitness * (n_animals_in_same_species - 1))
        if random.random() < probability:
            weight = random.gauss(self.param["w_birth"], self.param["sigma_birth"])
            born_baby = type(self)(0, int(weight))  # Herbivore()/Carnivore()

            if self.weight < born_baby.weight * self.param["xi"]:
                return None
            else:
                self.weight -= born_baby.weight * self.param["xi"]
                return born_baby


class Herbivore(Animal):
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

    def weight_increase_herb(self, fodder):
        """
        Increasing the weight of a herbivore once it eats some fodder F.
        """
        self.weight += self.param["beta"] * fodder
        self.fitness_animal()


class Carnivore(Animal):
    param = {
        "w_birth": 6.0,
        "sigma_birth": 1.0,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 40.0,
        "phi_age": 0.3,
        "w_half": 4.0,
        "phi_weight": 0.4,
        "mu": 0.4,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.8,
        "F": 50.0,
        "DeltaPhiMax": 10
    }

    # Have to change the parameters here.

    def __init__(self, age=None, weight=None):
        super().__init__(age=age, weight=weight)
        self.kill_p = None
