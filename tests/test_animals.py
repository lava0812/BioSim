# -*- encoding: utf-8 -*-

__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import random
from src.biosim.animals import Herbivore
from scipy import stats
import numpy as np


def test_aging():
    herbivore = Herbivore()
    herbivore.aging()

    assert herbivore.age == 1


# def test_weight_baby():
#     """
#     Check if the baby will be given a weight.
#     """
#     herbivore1 = Herbivore()
#     herbivore2 = Herbivore()
#
#     herbivore1.weight_baby()
#     herbivore2.weight_baby()
#
#     assert herbivore1.weight != herbivore2.weight


def test_gaussian_distribution():
    """
    Check if weight of baby actually is a gaussian distribution.
    """
    random.seed(12345)
    weights = [Herbivore().weight_baby() for _ in range(5000)]

    numpy_weights = np.array(weights)

    k2, p_value = stats.normaltest(numpy_weights)
    a = 0.05
    print(k2, p_value)

    assert a < p_value

    # Something wrong with this test.


def test_weight_increase():
    """
    Test on the weight increase once a herbivore eats fodder.
    """
    herbivore = Herbivore()

    pre_weight = herbivore.weight
    herbivore.weight_increase(5)
    after_weight = herbivore.weight

    assert pre_weight < after_weight


def test_weight_decrease():
    """
    Test on the weight decrease every year.
    """

    herbivore = Herbivore(5, 10)
    herbivore.weight_baby()

    pre_weight = herbivore.weight
    herbivore.weight_decrease()
    post_weight = herbivore.weight

    assert pre_weight > post_weight


def test_fitness_herbivores():
    """
    Fitness is dependent on the age and the weight of the animal.
    Test if fitness calculation is updated correct when age and weight is positive, and
    the fitness is set to 0.
    """
    herbivore1 = Herbivore(40, 10)
    herbivore1.fitness = 0
    herbivore1.fitness_herbivore()
    assert herbivore1.fitness > 0


def test_fitness_herbivores_zero_weight():
    """
    Test if fitness is equal to 0, when weight is zero.
    """
    herbivore2 = Herbivore(30, 0)
    herbivore2.fitness_herbivore()

    assert herbivore2.fitness == 0


def test_death_herbivores_certain():
    """
    Test death when herbivore weight is zero.
    """
    herbivores = Herbivore(30, 0)

    herbivores.death_herbivore()
    assert herbivores.death == True


# noinspection SpellCheckingInspection
def test_death_herbivores_bychance(mocker):
    """
    Test the chance of death, using mocker.
    """
    mocker.patch("random.random", return_value=0)
    herbivores = Herbivore(10, 20)
    herbivores.death_herbivore()

    assert herbivores.death == True


def test_birth(mocker):
    """
    Test the probability of birth.
    """
    mocker.patch("random.random", return_value=0)
    herbivore = Herbivore(3, 14)
    birth_herbivore = herbivore.birth(5)

    assert birth_herbivore is not None
    herbivore.weight = 1
    birth_herbivore = herbivore.birth(5)
    assert birth_herbivore is None

# def test_birth_weight_loss():
#     """
#     Testing if weight of mother pre birth is larger than weight of mother
#     post birth.
#     """
#     herbivore = Herbivore(10, 20)
#     pre_weight = herbivore.weight
#     herbivore.birth_weight_loss()
#
#     post_weight = herbivore.weight
#
#     assert pre_weight > post_weight
