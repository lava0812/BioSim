"""
This file will contain a main class Animals(Superclass). This Animals class will contains methods for characteristics
that are common for both herbivores and carnivores. The Animals class will have to subclasses,
Herbivores and Carnivores.
These to subclasses will contain methods specifically for herbivores and carnivores.
"""

import math

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

    def __init__(self,age = None, weight = None):
        self.age = 0
        self.weight = weight




    def aging(self):
        """
        This is a method for making the herbivores age. This function will be in the Animals superclass once we create it.
        """
        self.age += 1

    def weight_baby(self):
        """
        This method will use a Gaussian distribution for determining the weight of a Herbivore baby
        """
        pass

    def weight_increase(self):
        """
        This method will increase the weight of the herbivores once it eats some fodder F.
        """
        pass

    def weight_decerase(self):
        """
        This method will decrease the weight of a herbivore every year.
        """
        pass

    def fitness_herbivores(self):
        """
        This method will update the fitness of a herbivore,
        """
        pass

    def death_herbivore(self):
        """
        This will be a method for the death of a herbivore.
        """
        pass

    def eat_herbivore(self):
        """
        This is a method that makes the herbivores eat an amount of F fodder
        """






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






class Herbivores(Animals):
    """
    This is the Herbivores subclass and will contain these methods:
        - Eat
    """
    pass




class Carnivores(Animals):
    """
    This is the Carnivores subclass and will contain these methods:
        - Eat
        - Kill
    """
    pass

