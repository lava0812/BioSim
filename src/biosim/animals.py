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

        Parameters
        ----------
        added_parameters : dict
            The new parameter is a dictionary
        """
        for parameter in added_parameters.keys():
            if parameter not in cls.param.keys():
                raise KeyError("Invalid parameter name")

        for parameter, value in added_parameters.items():
            if value < 0:
                raise ValueError("Inputted parameters can not be negative!")
            if parameter == "eta" and value > 1:
                raise ValueError
            cls.param[parameter] = value
        cls.param.update(added_parameters)

    def __init__(self, age=None, weight=None):

        """
        Constructor for Animal class.

        Parameters
        ----------
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
        Aging the animals every year with +1.
        """
        self.age += 1.0
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
        float
            The generated fitness of the animal
        """

        if self.weight == 0:  # ==
            self.fitness = 0
        #   return False  # Kan vurdere å returnere false.
        else:

            plus_exp = (self.param["phi_age"]) * (self.age - self.param["a_half"])
            neg_exp = (-1 * self.param["phi_weight"]) * (self.weight - self.param["w_half"])

            q_positive = 1 / (1 + math.exp(plus_exp))
            q_negative = 1 / (1 + math.exp(neg_exp))

            self.fitness = q_positive * q_negative

        # if self.weight <= 0:
        #     self.fitness = 0
        # else:
        #     self.fitness = q_positive * q_negative

    def death_animal(self):
        r"""
        Death of an animal, using probability. If the animal is fitter then the other,
        the chance of survival increase a lot.

        If an animal has a weight higher than zero, the probability to die is given by the formula:

        .. math::
            \begin{equation}
            \omega(1 - \Phi)
            \end{equation}

        Returns
        -------
        self.death: Boolean
        Returning if death is equal to true or false.
        """
        probability_die = self.param["omega"] * (1 - self.fitness)
        # Herbivore, carnivore will die with a probability of w(1-fitness)

        if self.weight == 0:  # Retta på fra =< til ==
            self.death = True  # Herbivore, carnivore dies with certainty
        elif probability_die > random.random():
            self.death = True
        return self.death

    def birth(self, n_animals_in_same_species):
        r"""
        Probability to give birth for an animal.

        The probability to give birth is given by the formula:

        .. math::
            \begin{equation}
            min(1,\gamma \times \Phi \times (N-1))
            \end{equation}

        N = The number of same type of animals.

        If the weight is zero, the probability of birth is given by this formula:

        .. math::
            \begin{equation}
            w < \zeta(w_{birth} + \sigma_{birth})
            \end{equation}

        Parameters
        ----------
        n_animals_in_same_species : int
            The number of same species in one cell.
        Returns
        -------
        new_baby
            Generating a new baby
        boolean
            If the requirements for birth is not filled
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
    """Subclass of the Animals class. This class is for the herbivore species in Biosim"""
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
           This is a constructor that gives us new carnivores

           Parameters
           ----------
           age : int
                   Gives age to a new herbivore. This will start a 0 by default.

           weight : int
                   Gives weight to a new herbivore. Here we use Gaussian distribution for
                   determining the weight of a newborn baby.
           """
        super().__init__(age, weight)

    def weight_increase(self, fodder):
        r"""
        Increasing the weight of a herbivore once it eats some fodder F.

        .. math::
            \begin{equation}
            \beta \times \F
            \end{equation}

        """
        self.weight += self.param["beta"] * fodder
        self.fitness_animal()


class Carnivore(Animal):
    """Subclass of the Animals class. This class is for the carnivore species in Biosim"""
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
        """
        This is a constructor that gives us new carnivores

        Parameters
        ----------
        age : int
                Gives age to a new carnivore. This will start a 0 by default.

        weight : int
                Gives weight to a new carnivore. Here we use Gaussian distribution for determining
                the weight of a newborn baby.
        """
        super().__init__(age=age, weight=weight)
        #self.kill_p = None

    def kill_probability(self, herbivore):
        if self.fitness < herbivore.fitness:
            return 0
        elif 0 < self.fitness - herbivore.fitness < self.param["DeltaPhiMax"]:
            return (self.fitness - herbivore.fitness) / self.param["DeltaPhiMax"]
        else:
            return 1



"""
    def prey(self):

        random.shuffle(self.carnivores)

        self.herbivores.sort(key=lambda x: "fitness", reverse=True)
        # ate = 0

        for carnivore in self.carnivores:
            #    if carnivore.hungryØ
            #        self.hunt?herbivores(carnivore)

            ate = 0

            for herbivore in self.herbivores:

                kill_probability = 0

                if ate >= carnivore.param["F"] or carnivore.fitness <= herbivore.fitness:
                    break
                elif 0 < carnivore.fitness - herbivore.fitness < carnivore.param["DeltaPhiMax"]:
                    kill_probability = (carnivore.fitness - herbivore.fitness) / \
                                       carnivore.param["DeltaPhiMax"]

                else:

                    kill_probability = 1
                if kill_probability > random.random():
                    # w = herbivore.weight
                    if ate + herbivore.weight > carnivore.param["F"]:
                        w = carnivore.param["F"] - ate
                        ate = carnivore.param["F"]
                    else:
                        w = herbivore.weight
                        ate += herbivore.weight

                    herbivore.death = True
                    carnivore.weight += carnivore.param["beta"] * w
                    carnivore.fitness_animal()

                # carnivore.weight += carnivore.param["beta"] * herbivore.weight
                # ate += herbivore.weight
                # carnivore.fitness_animal()

            self.death_population()  # finne en ny måte å fjerne herb på
        # print(ate)

    # def hunting carnirvore(carnivore)?
    #    survivores =
    #    for herbivore in self.herbivores
    #        if carnivore.kill(herbivore)

    # self.herbivores = survivors
"""
