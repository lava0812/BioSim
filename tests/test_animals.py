__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.animals import Herbivore
import pytest


def test_aging():
    herbivore = Herbivore()
    herbivore.aging()

    assert herbivore.age == 1


def test_weight_baby():
    """
    Check if the baby will have a weight.
    """
    herbivore1 = Herbivore()
    herbivore2 = Herbivore()

    herbivore1.weight_baby()
    herbivore2.weight_baby()

    assert herbivore1.weight != herbivore2.weight


def test_weight_increase():
    herbivore = Herbivore()

    pre_weight = herbivore.weight
    herbivore.weight_increase(5)
    after_weight = herbivore.weight

    assert pre_weight < after_weight


def test_weight_decrease():
    herbivore = Herbivore()

    pre_weight = herbivore.weight
    herbivore.weight_decrease()
    after_weight = herbivore.weight

    assert pre_weight == after_weight


def test_fitness_herbivores():
    pass


def test_death_herbivores():
    pass


def test_birth_herbivore():
    pass


def test_birth_herbivore_probability():
    pass


def test_birth_weight_loss():
    pass
