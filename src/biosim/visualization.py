# -*- encoding: utf-8 -*-
import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np

"""
:mod:`randvis.graphics` provides graphics support for BioSim.

.. note::
   * This module requires the program ``ffmpeg`` or ``convert``
     available from `<https://ffmpeg.org>` and `<https://imagemagick.org>`.
   * You can also install ``ffmpeg`` using ``conda install ffmpeg``
   * You need to set the  :const:`_FFMPEG_BINARY` and :const:`_CONVERT_BINARY`
     constants below to the command required to invoke the programs
   * You need to set the :const:`_DEFAULT_FILEBASE` constant below to the
     directory and file-name start you want to use for the graphics output
     files.

"""

"""
visualization.py is highly inspired by Hans Ekkehard Plesser´s
randvis project. This is the link for the gitlab project: 
https://gitlab.com/nmbu.no/emner/inf200/h2021
/inf200-course-materials/-/tree/main/january_block/examples/randvis_project
"""

# Update these variables to point to your ffmpeg and convert binaries
# If you installed ffmpeg using conda or installed both softwares in
# standard ways on your computer, no changes should be required.
_FFMPEG_BINARY = 'ffmpeg'
_MAGICK_BINARY = 'magick'

# update this to the directory and file-name beginning
# for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join('../..', 'data')
_DEFAULT_GRAPHICS_NAME = 'dv'
_DEFAULT_IMG_FORMAT = 'png'
_DEFAULT_MOVIE_FORMAT = 'mp4'  # alternatives: mp4, gif


class Visualization:
    """Provides graphics support for BioSim."""
    default_cmax = {"Herbivore": 200, "Carnivore": 100}
    default_specs = {'fitness': {'max': 1.0, 'delta': 0.05},
                     'age': {'max': 60.0, 'delta': 2},
                     'weight': {'max': 60, 'delta': 2}}

    def __init__(self, ymax=None, cmax=None, hist_specs=None, img_dir=None, img_name=None,
                 img_fmt=None):
        """
        :param img_dir: directory for image files; no images if None
        :type img_dir: str
        :param img_name: beginning of name for image files
        :type img_name: str
        :param img_fmt: image file format suffix
        :type img_fmt: str
        """

        self.cmax = None
        self._count_ax_herbi = None
        if img_name is None:
            img_name = _DEFAULT_GRAPHICS_NAME

        if img_dir is not None:
            self._img_base = os.path.join(img_dir, img_name)
        else:
            self._img_base = None

        self._img_fmt = img_fmt if img_fmt is not None else _DEFAULT_IMG_FORMAT

        self._img_ctr = 0
        self._img_step = 1

        # the following will be initialized by _setup_graphics

        self.ymax = ymax if ymax is not None else 18000
        self.cmax = cmax if cmax is not None else self.default_cmax
        self.hist_specs = hist_specs if hist_specs is not None else self.default_specs

        # We have added these
        self._fig = None
        self._map_ax = None
        self._count_ax = None
        self._herb_line = None
        self._carn_line = None
        self._yearly_count_disp = None
        self._heat_herbivore_ax = None
        self._heat_carnivore_ax = None
        self._count_fitness_ax = None
        self._count_age_ax = None
        self._count_weight_ax = None
        self._year_ax = None
        self.yearly_disp_text = None

    def update(self, step, cnt_animals, herb_map,
               carn_map, h_list, c_list):  # Very important method, sys_map will be matrix
        """
        Updates graphics with current data and save to file if necessary.

        :param step: current time step (current year)
        :param sys_map: current system status (2d array)
        :param sys_mean: current mean value of system
        """
        self._update_count_graph(step, cnt_animals["Herbivore"], cnt_animals["Carnivore"])

        self.heat_map_carnivores(carn_map)
        self.heat_map_herbivores(herb_map)
        # self.year_update(current_year)

        fitness_herb = [h.fitness for h in h_list]
        fitness_carn = [c.fitness for c in c_list]
        self.histo_fitness_update(fitness_herb, fitness_carn)

        age_herb = [h.age for h in h_list]
        age_carn = [c.age for c in c_list]
        self.histo_age_update(age_herb, age_carn)

        weight_herb = [h.weight for h in h_list]
        weight_carn = [c.weight for c in c_list]
        self.histo_weight_update(weight_herb, weight_carn)

        self.update_yearly_counter(step)

        # self._update_mean_graph(step, sys_mean)
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-5)  # pause required to pass control to GUI

        self._save_graphics(step)

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        The movie is stored as img_base + movie_fmt
        """

        if self._img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = _DEFAULT_MOVIE_FORMAT

        if movie_fmt == 'mp4':
            try:
                # Parameters chosen according to http://trac.ffmpeg.org/wiki/Encode/H.264,
                # section "Compatibility"
                subprocess.check_call([_FFMPEG_BINARY,
                                       '-i', '{}_%05d.png'.format(self._img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([_MAGICK_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self._img_base),
                                       '{}.{}'.format(self._img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)

    def setup(self, final_step, img_step,
              island_map):  # setup and update are the most important files.
        """
        Prepare graphics.

        Call this before calling :meth:`update()` for the first time after
        the final time step has changed.

        :param final_step: last time step to be visualised (upper limit of x-axis)
        :param img_step: interval between saving image to file
        """

        self._img_step = img_step

        # create new figure window
        if self._fig is None:
            self._fig = plt.figure(figsize=(12, 8))
            self._fig.set_facecolor("lightgray")

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        # this is for the heat map of animal distribution

        # This will be the first subplot, and is the subplot for the map
        # of the island.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(3, 3, 1)
            plt.title("Island")
            self.map_graphics_plot(island_map)

        # Add right subplot for line graph of mean.
        # this is for the line plot for both herbs and carns
        # This is the subplot for the animal count, and will be at the top right corner
        # of the subplot.
        if self._count_ax is None:
            self._count_ax = self._fig.add_subplot(3, 3, 3)
            self._count_ax.set_ylim(0, self.ymax + 1)
            self._img_count_axis = None

        if self._herb_line is None:
            # plot one line (herb_line)
            count_plot_herbi = self._count_ax.plot(np.arange(0, final_step + 1),
                                                   np.full(final_step + 1, np.nan),
                                                   label="Herbivore")

            self._herb_line = count_plot_herbi[0]

        else:
            x_data, y_data = self._herb_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._herb_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        if self._carn_line is None:
            # plot one line (herb_line)
            count_plot_carni = self._count_ax.plot(np.arange(0, final_step + 1),
                                                   np.full(final_step + 1, np.nan),
                                                   label="Carnivore")

            self._carn_line = count_plot_carni[0]

        else:
            x_data, y_data = self._carn_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carn_line.set_data(np.hstack((x_data, x_new)),
                                         np.hstack((y_data, y_new)))

        self._count_ax.set_title("Animal count")

        self._count_ax.set_xlim(0, final_step + 1)
        self._count_ax.legend(handles=[self._herb_line, self._carn_line])

        # This will be the subplot for the heatmap for herbivores.
        if self._heat_herbivore_ax is None:
            self._heat_herbivore_ax = self._fig.add_subplot(3, 3, 4)
            self._heat_herbivore_ax.set_title("Herbivore distribution")
            self._img_herb_axis = None

        # Heatmap for carnivores.
        if self._heat_carnivore_ax is None:
            self._heat_carnivore_ax = self._fig.add_subplot(3, 3, 6)
            self._heat_carnivore_ax.set_title("Carnivore distribution")
            self._img_carni_axis = None

        # Histogram for fitness(herbivores, carnivores).
        if self._count_fitness_ax is None:
            self._count_fitness_ax = self._fig.add_subplot(3, 3, 7)
            self._count_fitness_ax.set_title("Fitness")
            self._img_count_fit_axis = None

        # Histogram for age(herbivores, carnivores).
        if self._count_age_ax is None:
            self._count_age_ax = self._fig.add_subplot(3, 3, 8)
            self._count_age_ax.set_title("Age")
            self._img_count_age_axis = None

        # Histogram for weight(herbivores, carnivores).
        if self._count_weight_ax is None:
            self._count_weight_ax = self._fig.add_subplot(3, 3, 9)
            self._count_weight_ax.set_title("Weight")
            self._img_count_weight_axis = None

        if self._year_ax is None:
            self._year_ax = self._fig.add_subplot(3, 3, 2)
            template = 'Count: {:5d}'
            self._yearly_count_disp = self._year_ax.text(0.5, 0.5, template.format(0),
                                                         horizontalalignment='center',
                                                         verticalalignment='center',
                                                         transform=self._year_ax.transAxes)
            self._year_ax.axis('off')

        # needs updating on subsequent calls to simulate()
        # add 1 so we can show values for time zero and time final_step

    def heat_map_herbivores(self, herb_matrix):
        """Update the 2D-view of the system.
        This is the heatmap for herbivores.
        """

        if self._img_herb_axis is not None:
            self._img_herb_axis.set_data(herb_matrix)  # will be the matrix
        else:
            self._img_herb_axis = self._heat_herbivore_ax.imshow(herb_matrix,
                                                                 interpolation='nearest',
                                                                 vmin=0,
                                                                 vmax=self.cmax["Herbivore"])
            plt.colorbar(self._img_herb_axis, ax=self._heat_herbivore_ax,
                         orientation='vertical')

    def heat_map_carnivores(self, carn_matrix):
        """Update the 2D-view of the system.
        This is the heatmap for carnivores.
            """

        if self._img_carni_axis is not None:
            self._img_carni_axis.set_data(carn_matrix)
        else:
            self._img_carni_axis = self._heat_carnivore_ax.imshow(carn_matrix,
                                                                  interpolation='nearest',
                                                                  vmin=0,
                                                                  vmax=self.cmax["Carnivore"])
            plt.colorbar(self._img_carni_axis, ax=self._heat_carnivore_ax,
                         orientation='vertical')

    def _update_count_graph(self, step, count_h, count_c):
        # [nan, nan, nan, nan]
        y_data = self._herb_line.get_ydata()
        # if step = 0, the list becomes [1, nan, nan, nan]
        y_data[step] = count_h
        self._herb_line.set_ydata(y_data)

        y_data = self._carn_line.get_ydata()
        # if step = 0, the list becomes [1, nan, nan, nan]
        y_data[step] = count_c
        self._carn_line.set_ydata(y_data)

    def histo_fitness_update(self, herbivores, carnivores):
        # Here we create the histogram for the fitness update.
        # This will be a histogram at the bottom left of the plot window.
        self._count_fitness_ax.clear()
        self._count_fitness_ax.set_title("Fitness")
        self._count_fitness_ax.hist(herbivores, color="blue", histtype="step", label="Herbivore")
        self._count_fitness_ax.hist(carnivores, color="red", histtype="step", label="Carnivore")
        self._count_fitness_ax.legend()

    def histo_age_update(self, herbivores, carnivores):
        # Here we create the histogram for the age update.
        # This will be a histogram at the bottom center of the plot window.
        self._count_age_ax.clear()
        self._count_age_ax.set_title("Age")
        self._count_age_ax.hist(herbivores, color="blue", histtype="step", label="Herbivore")
        self._count_age_ax.hist(carnivores, color="red", histtype="step", label="Carnivore")
        self._count_age_ax.legend()

    def histo_weight_update(self, herbivores, carnivores):
        # Here we create the histogram for the weight update.
        # This will be a histogram at the bottom right of the plot window.

        self._count_weight_ax.clear()
        self._count_weight_ax.set_title("Weight")
        self._count_weight_ax.hist(herbivores, color="blue", histtype="step", label="Herbivore")
        self._count_weight_ax.hist(carnivores, color="red", histtype="step", label="Carnivore")
        self._count_weight_ax.legend()

    def update_yearly_counter(self, year):

        self._yearly_count_disp.set_text(f'Count: {year:5d}')

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1

    def map_graphics_plot(self, island_map):
        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in island_map.splitlines()]

        # self._map_ax = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h

        self._map_ax.imshow(map_rgb)

        self._map_ax.set_xticks(range(len(map_rgb[0])))
        self._map_ax.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        self._map_ax.set_yticks(range(len(map_rgb)))
        self._map_ax.set_yticklabels(range(1, 1 + len(map_rgb)))

        self._bar_ax = self._fig.add_axes([0.36, 0.7, 0.1, 0.4])  # llx, lly, w, h
        self._bar_ax.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            self._bar_ax.add_patch(plt.Rectangle((0., ix * 0.05), 0.15, 0.05,
                                                 edgecolor='none',
                                                 facecolor=rgb_value[name[0]]))
            self._bar_ax.text(0.35, ix * 0.05, name, transform=self._bar_ax.transAxes)

    def year_update(self, year_on_island):
        """
        This is a counter lapsed years on the island.
        """
        self.yearly_disp_text.set_text(f"Year: {year_on_island}")
