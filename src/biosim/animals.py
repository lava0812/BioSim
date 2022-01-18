# -*- encoding: utf-8 -*-
"""
:mod: 'biosim.animals' is the script that holds information on the carnivores and herbivores

.. note::
    This file contains the following superclass and subclasses and can be imported as a module:

    * Animals (superclass) - This Animals class will contain methods for characteristics
      that are common for both herbivores and carnivores.
    * Herbivores(Animals) - Subclass of the Animals class that holds the attributes for the
      Herbivore specie.
    * Carnivores(Animals) - Subclass of the Animals class that holds the attributes for
      the Carnivore specie.
"""
__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import math
import random


class Animal:
    __slots__ = ("age", "weight", "fitness", "death", "migrate", )

    """Superclass Animal in Biosim"""
    parameters_animal = {
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

    @classmethod
    def set_parameters_animals(cls, added_parameters: dict):
        """
        This will be a method for adding new parameters to the function.
        This is a classmethod because it involves changing the class variables.

        Parameters
        ----------
        added_parameters : dict
            The new parameter is a dictionary
        """

        for key, value in added_parameters.items():
            if key == "DeltaPhiMax":
                if value < 0:
                    raise ValueError("DeltaPhiMax must be > 0")
            elif key == "eta":
                if value >= 1:
                    raise ValueError("Eta must be 1 < ")
            elif key not in cls.parameters_animal:
                raise ValueError("Wrong Parameter")
            elif value <= 0:
                raise ValueError("Value must be positive integer")
            cls.parameters_animal[key] = value

    def __init__(self, age=None, weight=None):
        """
        Constructor for Animal class.

        Parameters
        ----------
        age: int
            Age of an animal, and the default value is set to be None.
        weight: float
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

    def birth(self, n_animals_in_same_species: int):
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
        new_baby: #TODO spør hva den returner
            Generating a new baby
        not new baby: boolean
            If the requirements for birth is not filled
        """

        probability = min(1, self.parameters_animal["gamma"] * self.fitness * (
                n_animals_in_same_species - 1))  # TODO trenger vi denne
        if self.weight < self.parameters_animal["zeta"] * (
                self.parameters_animal["w_birth"] + self.parameters_animal["sigma_birth"]):
            return None
        elif random.random() < probability:
            new_baby = type(self)()
            if new_baby.weight * self.parameters_animal["xi"] < self.weight:
                self.weight -= self.parameters_animal["xi"] * new_baby.weight
                self.fitness_animal()
                return new_baby
            else:
                return None
        else:
            return None

    def weight_baby(self):
        r"""
        Gaussian distribution for determining the weight of a newborn baby.
        Used only for the purpose of testing. The formula is given by:

        .. math::
            \begin{equation}
            w \sim \mathcal{N}(w_{birth}, \sigma_{birth})
            \end{equation}

        :math:`\mathcal{N}` = Gaussian distribution

        Returns
        -------
        weight: float
            Generates the new baby weight
        """
        # TODO: Don´t know if I use this function somewhere
        weight_baby = random.gauss(self.parameters_animal["w_birth"],
                                   self.parameters_animal["sigma_birth"])
        return weight_baby

    def weight_increase(self, food: float):
        r"""
        Increasing the weight of an animal once it eats some food F given by: :math:`\beta` F

        Parameters
        ----------
        food: float
        """
        self.weight += self.parameters_animal["beta"] * food
        self.fitness_animal()

    def fitness_animal(self):
        r"""
        Calculate the fitness of an animal.

        .. math::
            \Phi =
            \begin{cases}
            0 & \text{for }w\le0\\
            q^{+}(a, a_{\frac{1}{2}},\phi_{age}) \times
            q^{-}(w, w_{\frac{1}{2}},\phi_{weight}) & \text{else}
            \end{cases}
        Returns
        -------
        fitness: float
            The generated fitness of the animal
        """

        if self.weight == 0:
            self.fitness = 0
        else:

            plus_exp = (self.parameters_animal["phi_age"]) * (
                    self.age - self.parameters_animal["a_half"])
            neg_exp = (-1 * self.parameters_animal["phi_weight"]) * (
                    self.weight - self.parameters_animal["w_half"])

            q_positive = 1 / (1 + math.exp(plus_exp))
            q_negative = 1 / (1 + math.exp(neg_exp))

            self.fitness = q_positive * q_negative

    def migration_probability(self):
        r"""
        This calculates the probability of an animal moving with :math:`\mu \Phi`

        Returns
        -------
        # TODO finn ut hva den gjør
        """
        migrate_probability = self.fitness * self.parameters_animal["mu"]
        return random.random() < migrate_probability

    def weight_decrease(self):
        r"""
        Decrease the weight of an animal, which will happen every year with :math:`\eta w`
        """
        # TODO
        self.migrate = False

        self.weight -= self.weight * self.parameters_animal["eta"]  # Can put this in aging
        self.fitness_animal()

    def aging(self):
        """Aging the animals every year with +1."""
        self.age += 1.0

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
        Death: Boolean
            Returning if death is equal to true or false.
        """
        probability_die = self.parameters_animal["omega"] * (1 - self.fitness)

        if self.weight == 0:
            self.death = True
        elif probability_die > random.random():
            self.death = True
        return self.death


class Herbivore(Animal):
    """Subclass of the Animals class. This class is for the herbivore species in Biosim"""
    parameters_animal = {
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
           This is a constructor that gives us new herbivores

           Parameters
           ----------
           age : int
                   Gives age to a new herbivore. This will start at 0 by default.

           weight : float
                   Gives weight to a new herbivore. Here we use Gaussian distribution for
                   determining the weight of a newborn baby.
           """
        super().__init__(age, weight)


class Carnivore(Animal):
    """Subclass of the Animals class. This class is for the carnivore species in Biosim"""
    parameters_animal = {
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

        weight : float
                Gives weight to a new carnivore. Here we use Gaussian distribution for determining
                the weight of a newborn baby.
        """
        super().__init__(age=age, weight=weight)
        # self.kill_p = None

    def kill_probability(self, herbivore):
        r"""
        This method will show the kill probability, The carnivores will kill a herbivore
        with probability:

        .. math::
            \begin{equation}
            p =
            \begin{cases}
                0, & \text{if} \Phi_{carn} \leq \Phi_{herb} \\
                0, & \text{if}\ 0 < \phi_{carn} - \phi_{herb} < \Delta\Phi_{max} \\
                1, & \text{otherwise}
            \end{cases}
            \end{equation}

        carnivore's weight increases by :math:`\beta w_{birth}`

        Parameters
        ----------
        herbivore: #TODO

        Returns
        -------


        """

        if self.fitness < herbivore.fitness:
            return 0
        elif 0 < self.fitness - herbivore.fitness < self.parameters_animal["DeltaPhiMax"]:
            return (self.fitness - herbivore.fitness) / self.parameters_animal["DeltaPhiMax"]
        else:
            return 1
