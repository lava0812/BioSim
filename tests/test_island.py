__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.island import Island
import pytest


def test_init_wrong():
    geogr = """\
               WWW
               WLW
               WWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]
    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(20)]}]
    with pytest.raises(ValueError):
        Island(map=geogr, initial_population=None)


def test_create_map():
    pass


def test_map_input():
    pass


def test_map_boundaries():
    pass


def test_set_new_parameters():
    pass


def test_map_lines():
    pass


def test_population_cell():
    pass


def test_migrate():
    pass


def test_annual_cycle():
    pass