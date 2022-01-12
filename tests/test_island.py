__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

from src.biosim.island import Island
import pytest




def test_create_map():
    pass


def test_map_input():
    pass


def test_map_boundaries():
    geogr = """\
            EEW
            WRW
            WWW"""

    with pytest.raises(ValueError):
        Island(map=geogr, initial_population=[])


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
