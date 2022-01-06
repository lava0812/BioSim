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


class Herbivore:
    param_herbivores = {
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
        "F": 10.0
    }

    def __init__(self, age=0, weight=0):
        """
        Here we define our data for this function, and these are age and weight. Fitness is also a part of the data,
        but does not need to be included here because it is dependent on both the age and weight.
        """
        self.age = age
        self.weight = weight
        self.fitness = None
        self.fitness_herbivore()
        self.probability_birth = None
        self.probability_die = None
        self.death = False
        pass

    def aging(self):
        """
        This is a method for making the herbivores age. This function will be in the Animals
         superclass once we create it.
        """
        self.age += 1

    # @classmethod
    def weight_baby(self):
        """
        This method will use a Gaussian distribution for determining the weight of a Herbivore baby. In the
        Gaussian(normal distribution), w_birth is the mean value, and sigma_birth is our standard deviation.
        Can be useful to do this in a classmethod.
        """
        # The random.gauss function will go as a return statement.
        self.weight = random.gauss(self.param_herbivores["w_birth"], self.param_herbivores["sigma_birth"])
        # return self.weight

    def weight_increase(self, fodder):
        """
        This method will increase the weight of the herbivores once it eats some fodder F. It will increase with
        beta times the amount of fodder it eats.
        """
        self.weight = self.param_herbivores["beta"] * fodder

    def weight_decrease(self):
        """
        This method will decrease the weight of a herbivore every year. Every year, the weight of the animal
        decreases by eta times the weight
        """
        self.weight = self.weight * self.param_herbivores["eta"]  # Can put this in aging

    def fitness_herbivore(self):
        """
        This method will update the fitness of a herbivore. Fitness of a herbivore is calculated using age and weight.
        It can be smart to use if statements here.
        """
        q_positive = 1 / (1 + math.exp((self.param_herbivores["phi_age"])
                                       * (self.age - self.param_herbivores["a_half"])
                                       ))
        q_negative = 1 / (1 + math.exp((-self.param_herbivores["phi_weight"])
                                       * (self.weight - self.param_herbivores["w_half"])
                                       ))
        if self.weight <= 0:
            self.fitness = 0
        else:
            self.fitness = q_positive * q_negative

    def death_herbivore(self):
        """
        This will be a method for the death of a herbivore.
        """
        probability_die = self.param_herbivores["omega"] * (
                1 - self.fitness)  # Herbivore will die with a probability of w(1-fitness)

        if self.weight <= 0:
            self.death = True  # Herbivore dies with certainty
        elif probability_die >= random.random():
            self.death = True

    def birth_herbivore_probability(self, n_herbivore):
        """
        This method will handle the probability for a herbivore to give birth.
        """
        probability = min(1, Herbivore.param_herbivores["gamma"] * self.fitness * (n_herbivore - 1))
        if random.random() < probability:
            born_baby = type(self)()  # Herbivore()

            if self.weight < born_baby.weight * self.param_herbivores["xi"]:
                return None
            else:
                return born_baby
        return None

    # def birth_weight_loss(self):
    #     """
    #     This method makes the herbivore mother lose a weight of zeta times the weight of the baby.
    #     """
    #     self.weight -= self.weight_baby() * self.param_herbivores["xi"]
