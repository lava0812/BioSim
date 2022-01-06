__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.landscape import Lowland
import pytest
import sys


#def population_update():
#   sys.exit(0)


def test_disp_population():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
    low = Lowland()
    low.population_update(pop)
    check = low.display_population()
    assert check == 3


def test_new_fodder():
    """
    Checks if the fodder updates
    """
    low = Lowland()
    low.fodder = 0
    low.new_fodder()

    assert low.fodder != 0
    assert low.fodder == 800


def test_aging_population():
    """
    Test if the aging goes 1 up every year
    Does this by checking age before and after the function
    """
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]

    low = Lowland()
    low.population_update(pop)

    old_age = low.population[0].age

    low.aging_population()

    new_age = low.population[0].age

    assert new_age > old_age


def test_weight_loss():
    """
    Same system as aging test

    """
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]

    low = Lowland()
    low.population_update(pop)

    old_weight = low.population[0].weight

    low.weight_loss()

    new_weight = low.population[0].weight

    assert new_weight < old_weight


def test_eat_fodder():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]

    low = Lowland()
    low.population_update(pop)
    low.new_fodder()

    before_weight = low.population[0].weight

    low.eat_fodder()

    after_weight = low.population[0].weight

    assert after_weight > before_weight


def test_death_population():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]

    low = Lowland()
    low.population_update(pop)

    low.population_update[1].weight = 0






#def test_newborn():
    #sys.exit(0)


#def test_simulate():
