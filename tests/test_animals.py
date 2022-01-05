__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.animals import Herbivore
import sys


def test_aging():
    herbivore = Herbivore()
    herbivore.aging()

    assert herbivore.age == 1


def test_weight_baby():
    """
    Check if the baby will be given a weight.
    """
    herbivore1 = Herbivore()
    herbivore2 = Herbivore()

    herbivore1.weight_baby()
    herbivore2.weight_baby()

    assert herbivore1.weight != herbivore2.weight


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

    herbivore = Herbivore()
    herbivore.weight_baby()

    pre_weight = herbivore.weight
    herbivore.weight_decrease()
    after_weight = herbivore.weight

    assert pre_weight > after_weight


def test_fitness_herbivores():
    """
    Fitness is dependent on the age and the weight of the animal.
    Test if fitness calculation is correct when age and weight is positive.
    """
    herbivore1 = Herbivore(40, 10)
    herbivore1.fitness_herbivore()

    assert herbivore1.fitness == 0.25


def test_fitness_herbivores_zero():
    """
    Test if fitness is equal to 0, when weight is zero.
    """
    herbivore2 = Herbivore(30, 0)
    herbivore2.fitness_herbivore()

    assert herbivore2.fitness == 0


def test_death_herbivores_certain():
    herbivores = Herbivore(30, 0)

    herbivores.death_herbivore()
    assert herbivores.death == True


# noinspection SpellCheckingInspection
def test_death_herbivores_bychance():
    pass


def test_birth_herbivore():
    sys.exit(0)


def test_birth_herbivore_probability():
    sys.exit(0)


def test_birth_weight_loss():
    sys.exit(0)
