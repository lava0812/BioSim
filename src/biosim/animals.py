# -*- encoding: utf-8 -*-

"""
This file will contain a main class Animals(Superclass).
These Animals class will contain methods for characteristics
that are common for both herbivores and carnivores. The Animals class will have two subclasses,
Herbivores and Carnivores.
These to subclasses will contain methods specifically for herbivores and carnivores.
"""
__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import math
import random


class Animal:
    param = {}

    # Set param metoden vår er litt feil.
    @classmethod
    def set_param(cls, added_parameters):
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
        if age is None:
            self.age = 0
        else:
            self.age = age

        if weight is None:
            self.weight = self.weight_baby()
        else:
            self.weight = weight

        self.fitness = None
        self.fitness_animal()
        self.death = False
        self.migrate = False
        # self.migrate should be false after aging.in the same year.

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
        weight_baby = random.gauss(self.param["w_birth"], self.param["sigma_birth"])
        return weight_baby
        # Bruker ikke denne funksjonen noen steder.

    def weight_decrease(self):
        """
        Decrease the weight of an animal, which will happen every year.
        Updates the fitness right after.
        """
        # reset the migrate state
        self.migrate = False

        self.weight -= self.weight * self.param["eta"]  # Can put this in aging
        self.fitness_animal()

    def fitness_animal(self):
        """
        Calculate the fitness of an animal.

        Returns
        -------

        """

        if self.weight <= 0:
            self.fitness = 0
            return False  # Kan vurdere å returnere false.
        else:

            tall = round((self.param["phi_age"]) * (self.age - self.param["a_half"]), 10)
            tall2 = round((-self.param["phi_weight"]) * (self.weight - self.param["w_half"]), 10)

            q_positive = 1 / (1 + math.exp(tall))
            q_negative = 1 / (1 + math.exp(tall2))

            self.fitness = q_positive * q_negative

        # if self.weight <= 0:
        #     self.fitness = 0
        # else:
        #     self.fitness = q_positive * q_negative

    def death_animal(self):
        """
        Death of an animal, using probability.

        Returns
        -------
        self.death: Boolean
        Returning if death is equal to true or false.
        """
        probability_die = self.param["omega"] * (
                1 - self.fitness)
        # Herbivore, carnivore will die with a probability of w(1-fitness)

        if self.weight <= 0:  # Retta på fra =< til ==
            self.death = True  # Herbivore, carnivore dies with certainty
        elif probability_die > random.random():
            self.death = True
        return self.death

    def birth(self, n_animals_in_same_species):
        """
        Probability to give birth for an animal.

        Returns
        -------
        new_baby: Generating a new baby
        """

        probability = min(1, self.param["gamma"] * self.fitness * (n_animals_in_same_species - 1))

        if self.weight < self.param["zeta"] * (self.param["w_birth"] + self.param["sigma_birth"]):
            return None
        elif random.random() < probability:
            new_baby = type(self)()
            if new_baby.weight * self.param["xi"] < self.weight:
                self.weight -= self.param["xi"] * new_baby.weight
                self.fitness_animal()
                return new_baby
            else:
                return None
        else:
            return None

    def migration_probability(self):
        """
        This calculates the probability of an animal moving.
        """

        migrate_probability = self.fitness * self.param["mu"]
        return random.random() < migrate_probability


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

    def weight_increase(self, fodder):
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

    def __init__(self, age=None, weight=None):
        super().__init__(age=age, weight=weight)
        self.kill_p = None

