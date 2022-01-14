__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.island import Island
import pytest


def test_create_map():
    pass


#def test_map_input():
 #   pass


def test_map_boundaries():
    geogr = """\
            WWW
            WLW
            MWW"""

    with pytest.raises(ValueError):
        Island(map_of_island=geogr)


#def test_set_new_parameters():
  #  pass


def test_map_lines():
    geogr = """\
            WWWW
            WLW
            WWW"""

    with pytest.raises(ValueError):
        Island(map_of_island=geogr)


def test_population_cell():
    geogr = """\
            WWW
            WLW
            WWW"""

    population = [{'loc': (2, 2),
                 'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]},
                  {'loc': (2, 2),
                   'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]},
                  {'loc': (2, 2),
                   'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]}]

    island = Island(map_of_island=geogr)
    island.population_cell(population)

    assert len(island.map[(2, 2)].herbivores) == 3


#def test_migrate():
#   geogr = """\
#                WWW
#                WLW
#                WWW"""
#
#   population = [{'loc': (2, 2),
#                      'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]},
#                     {'loc': (2, 2),
#                      'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]},
#                     {'loc': (2, 2),
#                      'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]}]


#   island = Island(map_of_island=geogr)


#def test_annual_cycle():
   # pass


def test_get_all_herbivores():
    geogr = """\
               WWW
               WLW
               WWW"""

    population = [{'loc': (2, 2),
                   'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]},
                  {'loc': (2, 2),
                   'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]},
                  {'loc': (2, 2),
                   'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]}]

    island = Island(map_of_island=geogr)
    island.population_cell(population)

    check = island.get_all_carnivores()

    assert check == 3

    pass
def test_get_all_herbivores():
    geogr = """\
               WWW
               WLW
               WWW"""

    population = [{'loc': (2, 2),
                   'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]},
                  {'loc': (2, 2),
                   'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]},
                  {'loc': (2, 2),
                   'pop': [{'species': 'Herbivore', 'age': 10, 'weight': 12.5}]}]

    island = Island(map_of_island=geogr)
    island.population_cell(population)

    check = island.get_all_herbivores()

    assert len(check) == 9


def test_get_all_carnivores():
    geogr = """\
               WWW
               WLW
               WWW"""

    population = [{'loc': (2, 2),
                   'pop': [{'species': 'Carnivore', 'age': 10, 'weight': 12.5}]},
                  {'loc': (2, 2),
                   'pop': [{'species': 'Carnivore', 'age': 10, 'weight': 12.5}]},
                  {'loc': (2, 2),
                   'pop': [{'species': 'Carnivore', 'age': 10, 'weight': 12.5}]}]

    island = Island(map_of_island=geogr)
    island.population_cell(population)

    check = island.get_all_carnivores()

    assert len(check) == 9
