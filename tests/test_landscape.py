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
    lowland = Lowland()
    lowland.fodder = 0
    lowland.new_fodder()

    assert lowland.fodder != 0
    assert lowland.fodder == 800

def test_aging_population():
    sys.exit(0)


def test_eat_fodder():
    sys.exit(0)


def test_death_population():
    sys.exit(0)


def test_newborn():
    sys.exit(0)


def test_simulate():
    sys.exit(0)
