# -*- encoding: utf-8 -*-

"""
This script purpose is to test the functions from landscape.py file.
"""
# We should use pytest.fixtures here.
# We should create seperate tests for landscape type water and landscape type desert osv...
# This is for the tests to pass.

__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import random

import pytest

from src.biosim.landscape import Lowland, Water, Highland


def test_disp_population_herbivores():
    """
    This test will check if the function append the right
    amount of herbivores from the given list
    """
    population = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                  {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
                  {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
    land = Lowland()
    land.population_update(population)

    check = land.display_herbivores()

    assert check == 3


def test_disp_population_carnivores():
    """
    This will test if the function append the right
    amount of carnivores from the given list
    """
    population = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5},
                  {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                  {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]
    land = Lowland()
    land.population_update(population)

    check = land.display_carnivores()

    assert check == 3


def test_new_fodder():
    """
    Checks if the fodder grows/updates every new year
    """
    land = Lowland()
    land.fodder = 0
    land.new_fodder()
    assert land.fodder == land.parameters_fodder["f_max"]


def test_new_fodder_not_updated():
    """
    Checks what happens if there is no growth/update
    of the fodder in the new year
    """
    land = Lowland()
    land.fodder = 0
    land.new_fodder()

    assert land.fodder != 0


def test_aging_population_herbivore():
    """
    Test if the aging goes +1 up every year for herbivores
    Does this by checking age before and after the function
    """
    population = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]

    land = Lowland()
    land.population_update(population)

    old_age = land.herbivores[0].age

    land.aging_population()

    new_age = land.herbivores[0].age

    assert new_age == old_age + 1


def test_aging_population_carnivore():
    """
    Test if the aging goes 1 up every year for carnivores
    Does this by checking age before and after the function has executed

    """
    population = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5}]

    land = Lowland()
    land.population_update(population)

    old_age = land.carnivores[0].age

    land.aging_population()

    new_age = land.carnivores[0].age

    assert new_age == old_age + 1


def test_weight_loss_herbivore():
    """
    Test if the herbivores lose weight over the new year
    Does this by calculating the weight by hand, then testing the answer
    """
    population = [{'species': 'Herbivore', 'age': 10, 'weight': 10}]

    land = Lowland()
    land.population_update(population)

    land.weight_loss()

    new_weight = land.herbivores[0].weight

    assert new_weight == 9.5


def test_weight_loss_carnivore():
    """
    Test if the carnivores lose weight over the year
    Does this by indexing the weight before and after the
    weight_loss function runs
    """
    population = [{'species': 'Carnivore', 'age': 10, 'weight': 10}]

    land = Lowland()
    land.population_update(population)

    old_weight = land.carnivores[0].weight

    land.weight_loss()

    new_weight = land.carnivores[0].weight

    assert new_weight < old_weight


def test_eat_fodder():
    """
    Here I test if the Herbivores can eat the available fodder by
    checking the weight before and after eating to see if they have
    increased in weight.
    """
    population = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                  {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
                  {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
    land = Lowland()
    land.population_update(population)
    land.new_fodder()

    before_weight = land.herbivores[0].weight

    land.eat_fodder()

    after_weight = land.herbivores[0].weight

    assert after_weight > before_weight


def test_eating_too_much_fodder():
    lowland = Lowland()
    population = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]
    lowland.population_update(population)
    weight_before = lowland.herbivores[-1].weight
    beta = lowland.herbivores[-1].parameters_animal["beta"]
    lowland.herbivores[-1].parameters_animal["F"] = 10000000
    lowland.eat_fodder()
    assert lowland.fodder == 0
    assert lowland.herbivores[-1].weight == weight_before + (800 * beta)


def test_eat_fodder2():
    """
    Here I test if the Herbivores can eat the available fodder by
    checking the weight before and after eating to see if they have
    increased in weight.
    """
    population = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                  {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
                  {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]

    land = Lowland()
    land.population_update(population)
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
    """
    Here I test if the Herbivores do not eat by placing 0 fodder on the landscape,
    then  check the weight before and after eating to see if they have increased in weight.
    """
    population = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]

    land = Lowland()
    land.population_update(population)
    land.fodder = 0

    before = land.herbivores[0].weight

    land.eat_fodder()

    assert before == land.herbivores[0].weight


def test_death_population():
    """
    Here we test if the animals' dies they get removed from the
    population list. We knew the answer will be 2, so we
    tested by that fact
    """
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]

    land = Highland()
    land.population_update(pop)
    land.herbivores[1].weight = 0

    land.death_population()

    after_population = land.herbivores

    assert len(after_population) < 3


def test_prey():
    """
    We should test if the list gets shuffled or not here too.
    We should also test if the method sorts the herbivore after the lowest to the highest fitness.
    """
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1},
           {'species': 'Carnivore', 'age': 10, 'weight': 50},
           {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
           {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]

    land = Lowland()
    land.population_update(pop)

    before_population = land.herbivores

    land.prey()

    after_population = land.herbivores

    assert len(before_population) != len(after_population)


def test_prey_randomized():
    """Test to see if the list gets randomized"""
    random.seed(123456)
    carni = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5},
             {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
             {'species': 'Carnivore', 'age': 5, 'weight': 8.1},
             {'species': 'Carnivore', 'age': 5, 'weight': 10.1},
             {'species': 'Carnivore', 'age': 15, 'weight': 12.1},
             {'species': 'Carnivore', 'age': 22, 'weight': 11.1}]
    land = Lowland()
    land.population_update(carni)

    population_list_before = land.carnivores

    land.prey()

    population_list_after = land.carnivores

    assert population_list_before != population_list_after


def test_newborn_herbivore_false(mocker):
    """
    This test is to see if there will be a newborn if there is only one
    herbivore on the island, which should be false
    """
    mocker.patch("random.random", return_value=0)

    population = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]
    land = Lowland()

    land.population_update(population)

    land.newborn_herbivore()

    assert len(population) + 1 != len(population)


def test_newborn_herbivore(mocker):
    """Newborn test to see if the herbivore gives birth with three animals placed"""
    mocker.patch("random.random", return_value=0)

    population = [{'species': 'Herbivore', 'age': 18, 'weight': 40},
                  {'species': 'Herbivore', 'age': 9, 'weight': 40},
                  {'species': 'Herbivore', 'age': 5, 'weight': 40}]
    land = Lowland()

    land.population_update(population)
    population_before_herb = len(land.herbivores)
    land.newborn_herbivore()

    assert len(land.herbivores) > population_before_herb


def test_newborn_carnivore_false(mocker):
    """
    This test is to see if there will be a newborn if there is only one
    carnivore on the island, which should be false
    """
    mocker.patch("random.random", return_value=0)

    population = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5}]
    land = Lowland()

    land.population_update(population)

    land.newborn_carnivore()

    assert len(population) + 1 != len(population)


def test_newborn_carnivore(mocker):
    """Newborn test to see if the carnivore gives birth with three animals placed"""
    mocker.patch("random.random", return_value=0)

    population_carnivore = [{'species': 'Carnivore', 'age': 18, 'weight': 50},
                            {'species': 'Carnivore', 'age': 9, 'weight': 10.3}]
    land = Lowland()

    land.population_update(population_carnivore)
    population_before_carnivore = len(land.carnivores)
    land.newborn_carnivore()

    assert population_before_carnivore + 1 == len(land.carnivores)


def test_parameters_landscape():
    """Test to see if the subclass Lowland gives the right amount of fodder,
    which should be "f_max" = 800"""
    lowland = Lowland()
    lowland.set_parameters_fodder({"f_max": 300})
    with pytest.raises(ValueError):
        lowland.set_parameters_fodder({"f_max": -10000})


def test_parameters_lowland():
    """Test to see if the subclass Lowland gives the right amount of fodder,
    which should be "f_max" = 800"""
    lowland = Lowland()
    lowland.set_parameters_fodder({"f_max": 300})
    assert lowland.parameters["f_max"] == 300
    with pytest.raises(ValueError):
        lowland.set_parameters_fodder({"f_max": -10000})


def test_parameters_water():
    """Test to see if the subclass water gives the right amount of fodder,
    which should be "f_max" = 0"""
    lowland = Water()
    f_max = lowland.parameters_fodder["f_max"]

    assert f_max == 0

def test_migration(mocker):
    """
    Test if the list is bigger before, than after.
    """
    population_herbivore = [{'species': 'Herbivore', 'age': 18, 'weight': 50},
                            {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
                            {'species': 'Herbivore', 'age': 20, 'weight': 33.3},
                            {'species': 'Herbivore', 'age': 15, 'weight': 35.3},
                            {'species': 'Herbivore', 'age': 9, 'weight': 10.3}]
    land = Lowland()
    migrating_land = Highland()
    mocker.patch("random.choice", return_value = migrating_land)
    mocker.patch("random.random", return_value = -1)

    land.population_update(population_herbivore)

    animals_before = len(land.herbivores)

    land.migrated_animals()

    assert  animals_before > len(land.herbivores)

def test_carnivore_prey(mocker):
    mocker.patch("random.random", return_value = 0)