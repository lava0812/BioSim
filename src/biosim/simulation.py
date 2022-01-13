# -*- encoding: utf-8 -*-

"""
Template for BioSim class.
"""
__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import random

from biosim.animals import Carnivore, Herbivore
from biosim.island import Island, Water, Lowland


# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU


class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param img_years: years between visualizations saved to files (default: vis_years)
        :param log_file: If given, write animal counts to this file

        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_dir is None, no figures are written to file. Filenames are formed as

            f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'

        where img_number are consecutive image numbers starting from 0.

        img_dir and img_base must either be both None or both strings.
        """
        random.seed(seed)
        if ymax_animals is None:
            self.ymax_animals = 100
            # y axis limit should be adjusted automatically
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is None:
            self.cmax_animals = {'Herbivore': 230, 'Carnivore': 30}
            # Sensible fixed default values should be used. Should check over plesser´s notebook
            # for exact answers
        else:
            self.cmax_animals = cmax_animals

        if img_dir is None:
            # No figures are written to file.
            pass

        self.ini_pop = ini_pop
        self.island_map = island_map
        self.island = Island(island_map, ini_pop)
        self._current_year = 0
        self.vis_years = vis_years

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == "Herbivore" or species == "herbivore":
            Herbivore.set_param(params)
        elif species == "Carnivore" or species == "carnivore":
            Carnivore.set_param(params)
        else:
            raise ValueError("Choose a valid species! Choose between herbivore and carnivore.")

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == "Water" or landscape == "water":
            Water.set_parameters(params)
        elif landscape == "Lowland" or landscape == "lowland":
            Lowland.set_parameters(params)
        else:
            raise ValueError("Choose a valid landscape type!")
        # I should add highland and desert here eventually.
        # But this looks okay for now

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """
        for _ in range(num_years):
            Island().annual_cycle()

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island.population_cell(population)

    @property
    def year(self):
        """Last year simulated."""
        return self._current_year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.ini_pop

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        animal_count_per_species = {"Herbivore": 0, "Carnivore": 00}
        

        number_of_animals = {}
        # for cell in self.island_map:

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
