# -*- encoding: utf-8 -*-


"""
:mod:`randvis.graphics` provides graphics support for RandVis.

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

import os
import subprocess

import matplotlib.pyplot as plt
import numpy as np

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
    """Provides graphics support for RandVis."""

    def __init__(self, img_dir=None, img_name=None, img_fmt=None):
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
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._count_ax = None
        self._count_line = None

        # We have added these
        self._yearly_count_disp = None
        self._heat_herbivore_ax = None
        self._heat_carnivore_ax = None
        self._count_fitness_ax = None
        self._count_age_ax = None
        self._count_weight_ax = None
        self._img_herb_axis = None
        self._img_count_axis = None
        self._img_carni_axis = None
        self._img_count_fit_axis = None
        self._img_count_age_axis = None
        self._img_count_weight_axis = None
        self._img_herb_figure = None
        self._img_carni_figure = None

    def update(self, step, sys_map, sys_mean):  # Very important method, sys_map will be matrix
        """
        Updates graphics with current data and save to file if necessary.

        :param step: current time step (current year)
        :param sys_map: current system status (2d array)
        :param sys_mean: current mean value of system
        """

        self.heat_map_carnivores(sys_map)
        self.heat_map_herbivores(sys_map)

        self._update_mean_graph(step, sys_mean)
        self._fig.canvas.flush_events()  # ensure every thing is drawn
        plt.pause(1e-6)  # pause required to pass control to GUI

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

    def setup(self, final_step, img_step):  # setup and update are the most important files.
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
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        # this is for the heat map of animal distribution

        # This will be the first subplot, and is the subplot for the map
        # of the island.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(3, 3, 1)
            self._img_axis = None

        # Add right subplot for line graph of mean.
        # this is for the line plot for both herbs and carns
        # This is the subplot for the animal count, and will be at the top right corner
        # of the subplot.
        if self._count_ax is None:
            self._count_ax = self._fig.add_subplot(3, 3, 3)
            self._count_ax.set_ylim(-0.05, 0.05)
            self._img_count_axis = None

        # This will be the subplot for the heatmap for herbivores.
        if self._heat_herbivore_ax is None:
            self._heat_herbivore_ax = self._fig.add_subplot(3, 3, 4)
            self._heat_herbivore_ax.set_ylim(-0.05, 0.05)
            self._img_herb_axis = None

        # Heatmap for carnivores.
        if self._heat_carnivore_ax is None:
            self._heat_carnivore_ax = self._fig.add_subplot(3, 3, 6)
            self._heat_carnivore_ax.set_ylim(-0.05, 0.05)
            self._img_carni_axis = None

        # Histogram for fitness(herbivores, carnivores).
        if self._count_fitness_ax is None:
            self._count_fitness_ax = self._fig.add_subplot(3, 3, 7)
            self._count_fitness_ax.set_ylim(-0.05, 0.05)
            self._img_count_fit_axis = None

        # Histogram for age(herbivores, carnivores).
        if self._count_age_ax is None:
            self._count_age_ax = self._fig.add_subplot(3, 3, 8)
            self._count_age_ax.set_ylim(-0.05, 0.05)
            self._img_count_age_axis = None

        # Histogram for weight(herbivores, carnivores).
        if self._count_weight_ax is None:
            self._count_weight_ax = self._fig.add_subplot(3, 3, 9)
            self._count_weight_ax.set_ylim(-0.05, 0.05)
            self._img_count_weight_axis = None

        # needs updating on subsequent calls to simulate()
        # add 1 so we can show values for time zero and time final_step
        self._count_ax.set_xlim(0, final_step + 1)

        if self._count_line is None:
            # plot one line (herb_line)
            count_plot_herbi = self._count_ax.plot(np.arange(0, final_step + 1).
                                                   np.full(final_step + 1, np.nan))

            count_plot_carni = self._count_ax.plot(np.arange(0, final_step + 1).
                                                   np.full(final_step + 1, np.nan))
            # mean_plot = self._mean_ax.plot(np.arange(0, final_step + 1),
            #                                np.full(final_step + 1, np.nan))

            self._herb_line = count_plot_herbi[0]

            self._carn_line = count_plot_carni[0]

        else:
            x_data, y_data = self._count_line.get_data()
            x_new = np.arange(x_data[-1] + 1, final_step + 1)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._count_line.set_data(np.hstack((x_data, x_new)),
                                          np.hstack((y_data, y_new)))

    def heat_map_herbivores(self, amt_herbivores):
        """Update the 2D-view of the system.
        This is the heatmap for herbivores.
        """

        if self._img_herb_axis is not None:
            self._img_herb_axis.set_data(amt_herbivores)  # will be the matrix
        else:
            self._img_herb_axis = self._heat_herbivore_ax.imshow(amt_herbivores,
                                                                 interpolation='nearest',
                                                                 vmin=0,
                                                                 vmax=self.cmax["Herbivores"])
            plt.colorbar(self._img_herb_axis, ax=self._heat_herbivore_ax,
                         orientation='vertical')

    def heat_map_carnivores(self, amt_carnivores):
        """Update the 2D-view of the system.
        This is the heatmap for carnivores.
            """

        if self._img_carni_axis is not None:
            self._img_carni_axis.set_data(amt_carnivores)
        else:
            self._img_carni_axis = self._heat_carnivore_ax.imshow(amt_carnivores,
                                                                  interpolation='nearest',
                                                                  vmin=0,
                                                                  vmax=self.cmax["Carnivores"])
            plt.colorbar(self._img_carni_axis, ax=self._heat_carnivore_ax,
                         orientation='vertical')

    def _update_mean_graph(self, step, mean):
        # [nan, nan, nan, nan]
        y_data = self._count_line.get_ydata()
        # if step = 0, the list becomes [1, nan, nan, nan]

        y_data[step] = mean
        self._count_line.set_ydata(y_data)

    def histo_fitness_update(self, herbivores, carnivores):
        # Here we create the histogram for the fitness update.
        # This will be a histogram at the bottom left of the plot window.
        if self._count_fitness_ax is None:
            self._img_herb_figure.hist(herbivores["fitness"], color="blue", histtype="step")
            self._img_carni_figure.hist(carnivores["fitness"], color="red", histtype="step")

    def histo_age_update(self, herbivores, carnivores):
        # Here we create the histogram for the age update.
        # This will be a histogram at the bottom center of the plot window.
        if self._count_age_ax is None:
            self._img_herb_figure.hist(herbivores["age"], color="blue", histtype="step")
            self._img_carni_figure.hist(carnivores["age"], color="red", histtype="step")
        else:
            self._count_age_ax.clear()

    def histo_weight_update(self, herbivores, carnivores):
        # Here we create the histogram for the weight update.
        # This will be a histogram at the bottom right of the plot window.

        if self._count_weight_ax is None:
            self._img_herb_figure.hist(herbivores["weight"], color="blue", histtype="step")
            self._img_carni_figure.hist(carnivores["weight"], color="red", histtype="step")

    def _save_graphics(self, step):
        """Saves graphics to file if file name given."""

        if self._img_base is None or step % self._img_step != 0:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self._img_base,
                                                     num=self._img_ctr,
                                                     type=self._img_fmt))
        self._img_ctr += 1

    def map_graphics_update(self, island_map):
        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in island_map.splitlines()]

        fig = plt.figure()

        ax_im = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h

        ax_im.imshow(map_rgb)

        ax_im.set_xticks(range(len(map_rgb[0])))
        ax_im.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        ax_im.set_yticks(range(len(map_rgb)))
        ax_im.set_yticklabels(range(1, 1 + len(map_rgb)))

        ax_lg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        ax_lg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                          edgecolor='none',
                                          facecolor=rgb_value[name[0]]))
            ax_lg.text(0.35, ix * 0.2, name, transform=ax_lg.transAxes)

    def year_update(self, year_on_island):
        """
        This is a counter lapsed years on the island.
        """
        self._yearly_count_disp.set_text(f"Year: {year_on_island}")
