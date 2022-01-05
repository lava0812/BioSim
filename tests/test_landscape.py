__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.landscape import Lowland
import pytest
def population_update():
    pass

def disp_population():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]

    low = Lowland()
    low.population_update(pop)
    check = low.disp_population()
    assert check != 6


def test_new_fodder():
    loow = Lowland()
    loow.fodder = 0
    loow.new_fodder()

    assert loow.fodder != 0
    assert loow.fodder == 800


#def test_simulate():
    #pass