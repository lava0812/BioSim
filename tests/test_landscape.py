# -*- encoding: utf-8 -*-

__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.landscape import Landscape


# def test_population_update():
#    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
#           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
#           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
#   land = Landscape()
#   land.herb(pop)

#  assert len(land.herb) == 3


def test_disp_population_herbi():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
    land = Landscape()
    land.population_update(pop)

    check = land.display_herb()

    assert check == 3


def test_disp_population_carni():
    pop = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5},
           {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
           {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]
    land = Landscape()
    land.population_update(pop)

    check = land.display_carni()

    assert check == 3


def test_new_fodder():
    """
    Checks if the fodder updates
    """
    land = Landscape()
    land.fodder = 0
    land.new_fodder()

    assert land.fodder != 0
    assert land.fodder == 800


def test_aging_population():
    """
    Test if the aging goes 1 up every year
    Does this by checking age before and after the function
    """
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]

    land = Landscape()
    land.population_update(pop)

    old_age = land.herb[0].age

    land.aging_population()

    new_age = land.herb[0].age

    assert new_age > old_age


def test_weight_loss():
    """
    Same system as aging test

    """
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]

    land = Landscape()
    land.population_update(pop)

    old_weight = land.herb[0].weight

    land.weight_loss()

    new_weight = land.herb[0].weight

    assert new_weight < old_weight


def test_eat_fodder():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
    land = Landscape()
    land.population_update(pop)
    land.new_fodder()

    before_weight = land.herb[0].weight

    land.eat_fodder()

    after_weight = land.herb[0].weight

    assert after_weight > before_weight

def test_eat_fodder2():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]

    land = Landscape()
    land.population_update(pop)
    land.new_fodder()






def test_not_eat():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]
    land = Landscape()
    land.population_update(pop)
    land.fodder = 0

    before = land.herb[1].weight

    land.eat_fodder()

    assert before == land.herb[1].weight


def test_death_population():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]

    land = Landscape()
    land.population_update(pop)
    land.herb[1].weight = 0

    before_population = land.herb

    land.death_population()

    after_population = land.herb

    assert len(before_population) != len(after_population)


def test_prey():
    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
           {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
           {'species': 'Herbivore', 'age': 5, 'weight': 8.1},
           {'species': 'Carnivore', 'age': 10, 'weight': 12.5},
           {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
           {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]

    herbivores_list = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5},
                       {'species': 'Herbivore', 'age': 9, 'weight': 10.3},
                       {'species': 'Herbivore', 'age': 5, 'weight': 8.1}]

    carnivores_list = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5},
                       {'species': 'Carnivore', 'age': 3, 'weight': 7.3},
                       {'species': 'Carnivore', 'age': 5, 'weight': 8.1}]

    land = Landscape()
    land.population_update(pop)

    before_population = len(land.total_pop())

    land.prey(herbivores_list, carnivores_list)

    after_population = len(land.total_pop())

    assert before_population != after_population
# Hvordan teste pray


def test_newborn_herb_false(mocker):
    """
    Newborn test
    """
    mocker.patch("random.random", return_value=0)

    pop = [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]
    land = Landscape()

    land.population_update(pop)

    land.newborn_herb()

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
    population_before = len(land.herb)
    land.newborn_herb()
    assert len(land.herb) > population_before

# def test_newborn_carni(mocker):
#     """
#     Newborn test
#     """
#     mocker.patch("random.random", return_value=0)

# population = [{'species': 'Carnivore', 'age': 10, 'weight': 12.5},
#                     {'species': 'Carnivore','age': 3, 'weight': 7.3},
#                     {'species': 'Carnivore','age': 5, 'weight': 8.1}]

#     land = Landscape()
#
#     land.population_update(pop)
#
#     land.newborn_carni()

# assert len(land.carni) > len(pop)
