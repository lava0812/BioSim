__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import pytest

from src.biosim.island import Island


def test_create_map():
    pass


def test_map_boundaries():
    """
    This test will check if the map boundaries are water(W).
    """
    geogr = """\
            WWW
            WLW
            MWW"""

    with pytest.raises(ValueError):
        Island(map_of_island=geogr)


def test_map_lines():
    """
    This test will check if the map lines are equal length
    """
    geogr = """\
            WWWW
            WLW
            WWW"""

    with pytest.raises(ValueError):
        Island(map_of_island=geogr)


def test_population_cell():
    """
    Test
    """
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


# def test_migrate():
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


# def test_annual_cycle():


def test_get_all_herbivores():
    """
    This tests if all herbivores on the same location gets appended to the list.
    """
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

    assert len(check) == 3


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

    assert len(check) == 3


def test_matrix_herbivores():
    pass


def test_matrix_carnivores():
    pass
