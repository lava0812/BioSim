# -*- encoding: utf-8 -*-

"""
This script purpose is to test the functions from landscape.py file.
"""

__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import random

from src.biosim.landscape import Landscape, Lowland, Water


def test_disp_population_herbivores():
    """
    This test will check if the function append the right amount of herbivores from the given list
    """
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
    land = Landscape()
    land.population_update(pop)

    check = land.display_herbivores()

    assert check == 3


def test_disp_population_carni():
    """
    This will test if the function append the right amount of carnivores from the given list
    """
    pop = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5},
           {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
           {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]
    land = Landscape()
    land.population_update(pop)

    check = land.display_carni()

    assert check == 3


def test_new_fodder():
    """
    Checks if the fodder updates every year
    """
    land = Landscape()
    land.fodder = 0
    land.new_fodder()
    assert land.fodder == 800

def test_new_fodder_not_updated():
    """
    Checks if the fodder updates every year, in this case it does not
    """
    land = Landscape()
    land.fodder = 0
    land.new_fodder()

    assert land.fodder != 0


def test_aging_population_herbi():
    """
    Test if the aging goes 1 up every year for herbivores
    Does this by checking age before and after the function
    """
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]

    land = Landscape()
    land.population_update(pop)

    old_age = land.herbivores[0].age

    land.aging_population()

    new_age = land.herbivores[0].age

    assert new_age == old_age + 1


def test_aging_population_carni():
    """
    Test if the aging goes 1 up every year for carnivores
    Does this by checking age before and after the function
    """
    pop = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5}]

    land = Landscape()
    land.population_update(pop)

    old_age = land.carnivores[0].age

    land.aging_population()

    new_age = land.carnivores[0].age

    assert new_age == old_age + 1


def test_weight_loss_herbi():
    """
    Test if the herbivores lose weight over the years

    """
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 10}]

    land = Landscape()
    land.population_update(pop)

    old_weight = land.herbivores[0].weight

    land.weight_loss()

    new_weight = land.herbivores[0].weight

    assert new_weight == 9.5


def test_weight_loss_carni():
    """
    Test if the carnivores lose weight over the year

    """
    pop = [{'species': 'Carnivore', 'age': 10, 'weight': 10}]

    land = Landscape()
    land.population_update(pop)

    old_weight = land.carnivores[0].weight

    land.weight_loss()

    new_weight = land.carnivores[0].weight

    assert new_weight < old_weight


def test_eat_fodder():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
    land = Landscape()
    land.population_update(pop)
    land.new_fodder()

    before_weight = land.herbivores[0].weight

    land.eat_fodder()

    after_weight = land.herbivores[0].weight

    assert after_weight > before_weight


def test_eat_fodder2():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]

    land = Landscape()
    land.population_update(pop)
    land.new_fodder()


# def test_eat_fodder3(mocker):
#
#     population = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
#            {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
#            {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
#     land = Landscape()
#     land.population_update(population)
#     land.fodder = 0
#     land.eat_fodder()


def test_eat_fodder_not_eat():
    population = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]

    land = Landscape()
    land.population_update(population)
    land.fodder = 0

    before = land.herbivores[0].weight

    land.eat_fodder()

    assert before == land.herbivores[0].weight


def test_death_population():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]

    land = Landscape()
    land.population_update(pop)
    land.herbivores[1].weight = 0

    before_population = land.herbivores

    land.death_population()

    after_population = land.herbivores

    assert len(after_population) == 2

  #  assert len(before_population) != len(after_population)


def test_prey():
    """
    We should test if the list gets shuffled or not here too.
    We should also test if the method sorts the herbivore after the lowest to highest fitness.
    """
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1},
           {'species': 'Carnivore', 'age': 10, 'weight': 50},
           {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
           {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]

    land = Landscape()
    land.population_update(pop)

    before_population = land.herbivores

    land.prey()

    after_population = land.herbivores

    assert len(before_population) != len(after_population)


def test_prey2():
    """
    Test randomize list
    """
    random.seed(123456)
    carni = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5},
             {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
             {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]
    land = Landscape()
    land.population_update(carni)

    population_list_before = land.carnivores

    land.prey()

    population_list_after = land.carnivores

    assert population_list_before != population_list_after


def test_newborn_herb_false(mocker):
    """
    Newborn test
    """
    mocker.patch("random.random", return_value=0)

    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]
    land = Landscape()

    land.population_update(pop)

    land.newborn_herbivore()

    assert len(pop) + 1 != len(pop)


def test_newborn_herb(mocker):
    """
    Newborn test
    """
    mocker.patch("random.random", return_value=0)

    population = [{'species': 'Herbivore', 'age': 18, 'weight': 12.5},
                  {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
                  {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
    land = Landscape()

    land.population_update(population)
    population_before_herb = len(land.herbivores)
    land.newborn_herbivore()

    assert len(land.herbivores) > population_before_herb


def test_newborn_carni_false(mocker):
    """
    Newborn test
    """
    mocker.patch("random.random", return_value=0)

    pop = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5}]
    land = Landscape()

    land.population_update(pop)

    land.newborn_carnivore()

    assert len(pop) + 1 != len(pop)


def test_newborn_carni(mocker):
    """
    Newborn test
    """
    mocker.patch("random.random", return_value=0)

    population_carni = [{'species': 'Carnivore', 'age': 18, 'weight': 12.5},
                        {'species': 'Carnivore', 'age': 9, 'weight': 10.3},
                        {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]
    land = Landscape()

    land.population_update(population_carni)
    population_before_carni = len(land.carnivores)
    land.newborn_carnivore()

    assert len(land.carnivores) > population_before_carni


def test_parameters_lowland():
    L = Lowland()
    f_max = L.parameters["f_max"]

    assert f_max == 800


def test_parameters_water():
    L = Water()
    f_max = L.parameters["f_max"]

    assert f_max == 0
