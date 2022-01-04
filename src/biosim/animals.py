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
from landscape import Lowland


class Herbivores:
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

    def __init__(self, age=None, weight=None):
        """
        Here we define our data for this function, and these are age and weight. Fitness is also a part of the data,
        but does not need to be included here because it is dependent on both the age and weight.
        """
        self.age = age
        self.weight = weight
        self.fitness = None
        self.probability_die = None
        self.probability_birth = None

    def aging(self):
        """
        This is a method for making the herbivores age. This function will be in the Animals
         superclass once we create it.
        """
        self.age += 1
        return self.age

    def weight_baby(self):
        """
        This method will use a Gaussian distribution for determining the weight of a Herbivore baby. In the
        Gaussian(normal distribution), w_birth is the mean value, and sigma_birth is our standard deviation.
        Will use the random library, as it is has been recommended not to use the numpy library.
        """
        self.weight = random.gauss(self.param_herbivores["w_birth"], self.param_herbivores["sigma_birth"])
        return self.weight

    def weight_increase(self):
        """
        This method will increase the weight of the herbivores once it eats some fodder F. It will increase with
        beta times the amount of fodder it eats.
        """
        self.weight = self.param_herbivores["beta"] * Lowland.new_fodder()
        return self.weight

    def weight_decrease(self):
        """
        This method will decrease the weight of a herbivore every year. Every year, the weight of the animal
        decreases by eta times the weight
        """
        self.weight = self.weight * self.param_herbivores["eta"]
        return self.weight

    def fitness_herbivores(self):
        """
        This method will update the fitness of a herbivore. Fitness of a herbivore is calculated using age and weight.
        It can be smart to use if statements here.
        """

        """
        if weight is <= 0
            Fitness will be 0
        else
            Fitness will be --> (1/(1+e*^(phi_age(+a_half)))*(1/(1+e*^(-phi_weight(w_half)))
        """

        if self.weight <= 0:
            self.fitness = 0
        else:
            self.fitness = (1 / (1 + math.e ** ((self.param_herbivores["phi_age"]) * self.param_herbivores["a_half"])) *
                            1 / (1 + math.e ** (
                            (self.param_herbivores["phi_weight"]) * self.param_herbivores["w_half"])))
        return self.fitness

    def death_herbivore(self):
        """
        This will be a method for the death of a herbivore. Will it be better to split up the death of a herbivore,
        into two methods. A method for the certain death of a herbivore, and a method with the probability of death
        for a herbivore.
        """

        """
        If the weight == 0:
            Herbivore dies with certainty
        else
            It will die with a probability of w(1-fitness). 
        """

        self.probability_die = None
        if self.weight == 0:
            self.probability_die = 1  # Herbivore dies with certainty
        else:
            self.probability_die = self.param_herbivores["omega"] * (
                    1 - self.fitness)  # Herbivore will die with a probability of w(1-fitness)
        return self.probability_die

    def birth_herbivore(self):
        """
        This will be a function that will do the birth of a herbivore. This creates a new baby.
        """

    def birth_herbivore_probability(self):
        """
        This method will handle the probability for a herbivore to give birth.
        """
        if len(Lowland.disp_population()) < 2 and self.weight < (self.param_herbivores["zeta"]
                                                                 + self.param_herbivores["sigma_birth"]):
            self.probability_birth = 0

        elif len(Lowland.disp_population()) > 2:
            self.probability_birth = min(1, self.param_herbivores * self.fitness * (len(Lowland.disp_population() - 1)))
            if self.weight <= Herbivores.birth_weight_loss():
                # No birth!!
                # self.weight = weight
                pass

            else:
                # Birth!
                pass

        return self.probability_birth

    def birth_weight_loss(self):
        """
        This method makes the herbivore mother lose a weight of zeta times the weight of the baby.
        """
        self.weight -= Herbivores.weight_baby() * self.param_herbivores["xi"]

        return self.weight


"""
class Animals:
    
    This is the Animals class. This class will contain these methods:
        - Age
        - Weight
        - Fitness
        - Migration
        - Birth
        - Death

    Both herbivores and carnivores will have given example parameters, but it must be possible to change these
    example values to values we prefer. Therefore we need to create a method for changing the parameters that are given
    in the project description.
    
    @classmethod
    def updated_parameters(cls):
        #Will add something here, as soon as I define the name of the list that contains the parameter names.
        pass


    def __init__(self):
        pass



"""
