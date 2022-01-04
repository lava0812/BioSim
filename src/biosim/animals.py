"""
This file will contain a main class Animals(Superclass). This Animals class will contains methods for characteristics
that are common for both herbivores and carnivores. The Animals class will have to subclasses,
Herbivores and Carnivores.
These to subclasses will contain methods specifically for herbivores and carnivores.
"""

import math

class Herbivores:

    def __init__(self,age = None, weight = None):
        self.age = 0
        self.weight = weight


    def aging(self):
        """
        A method for making the herbivores age. This function will be in the Animals superclass once we create it.
        """
        self.age += 1

    def weight_baby(self):
        """
        This will use a Gaussian distribution for determining the weight of a Herbivore baby
        """
        pass

    def weight_increase(self):
        """

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

