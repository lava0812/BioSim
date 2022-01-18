# -*- encoding: utf-8 -*-
"""
:mod: 'biosim.simulation' gives us the interface to the package

This script will provide us with simulation of Rossumøya.
"""
__author__ = "Sathuriyan Sivathas & Lavanyan Rathy"
__email__ = "sathuriyan.sivathas@nmbu.no & lavanyan.rathy@nmbu.no"

import random
import subprocess

from matplotlib import pyplot as plt

from biosim.animals import Carnivore, Herbivore
from biosim.island import Island, Water, Lowland, Highland, Desert
from biosim.visualization import _FFMPEG_BINARY, Visualization

"""
simulation.py is highly inspired by Hans Ekkehard Plesser´s
randvis project. This is the link for the gitlab project: 
https://gitlab.com/nmbu.no/emner/inf200/h2021
/inf200-course-materials/-/tree/main/january_block/examples/randvis_project. 
The template for this file is also given by Hans Ekkehard Plesser. 
"""


# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU


class BioSim:
    """Class for BioSim"""

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
        self._img_count = None
        random.seed(seed)

        if img_dir is None:
            # f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'
            # No figures are written to file.
            pass

        if img_base is not None:
            self._img_base = img_base
        else:
            self._img_base = None

        self.island_map = island_map
        self.island = Island(island_map)

        if ini_pop is not None:
            self.island.population_cell(ini_pop)

        self._current_year = 0
        self.vis_years = vis_years
        self.img_fmt = img_fmt if img_fmt is not None else "png"

        self.visualization = Visualization(ymax_animals, cmax_animals, hist_specs, img_dir,
                                           img_base, img_fmt, img_years)

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species == "Herbivore" or species == "herbivore":
            Herbivore.set_parameters_animals(params)
        elif species == "Carnivore" or species == "carnivore":
            Carnivore.set_parameters_animals(params)
        else:
            raise ValueError("Choose a valid species! Choose between herbivore and carnivore.")

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape == "W":
            Water.set_parameters_fodder(params)
        elif landscape == "L":
            Lowland.set_parameters_fodder(params)
        elif landscape == "H":
            Highland.set_parameters_fodder(params)
        elif landscape == "D":
            Desert.set_parameters_fodder(params)
        else:
            raise ValueError("Choose a valid landscape type!")

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """
        self.visualization.setup(self._current_year + num_years, 1, self.island_map)
        for num_year in range(self._current_year, self._current_year + num_years):
            self.island.annual_cycle()
            print(self.num_animals_per_species)

            self.visualization.update(self._current_year, self.num_animals_per_species,
                                      self.island.matrix_herbivores(),
                                      self.island.matrix_carnivores(),
                                      self.island.get_all_herbivores(),
                                      self.island.get_all_carnivores())
            self._current_year += 1

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
        return sum(self.num_animals_per_species.values())

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        animal_count_per_species = {"Herbivore": 0, "Carnivore": 0}

        for loc, landscape in self.island.map.items():
            animal_count_per_species["Herbivore"] += len(landscape.herbivores)
            animal_count_per_species["Carnivore"] += len(landscape.carnivores)
        return animal_count_per_species

    def save_fig(self):
        if self._img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_count,
                                                     type=self._img_fmt))
        self._img_count += 1

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""

        if self.img_base is None:
            raise RuntimeError("A filename is not defined!")

        try:
            subprocess.check_call([_FFMPEG_BINARY,
                                   '-i', '{}_%05d.png'.format(self.img_base),
                                   '-y',
                                   '-profile:v', 'baseline',
                                   '-level', '3.0',
                                   '-pix_fmt', 'yuv420p',
                                   '{}.{}'.format(self.img_base, "mp4")])
        except subprocess.CalledProcessError as err:
            raise RuntimeError("ERROR: convert failed with: {}".format(err))

        else:
            raise ValueError("Unknown movie format:" + "mp4")
