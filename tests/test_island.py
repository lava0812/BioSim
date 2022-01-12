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
            WWW
            WLW
            MWW"""

    with pytest.raises(ValueError):
        Island(map=geogr, initial_population=[])


def test_set_new_parameters():
    pass



def test_map_lines():
    geogr = """\
            WWWW
            WLW
            WWW"""

    with pytest.raises(ValueError):
        Island(map=geogr, initial_population=[])


def test_population_cell():
  geogr = """\
            WWW
            WLW
            WWW"""

  population =  [{'loc': (3, 4),
      'pop': [{'species': 'Herbivore',
               'age': 10, 'weight': 12.5},
              {'species': 'Herbivore',
               'age': 9, 'weight': 10.3},
              {'species': 'Carnivore',
               'age': 5, 'weight': 8.1}]}]

  island = Island(map=geogr,initial_population=population)
  island.population_cell(population)

  assert len(island.map[])



def test_migrate():
    pass


def test_annual_cycle():
    pass
