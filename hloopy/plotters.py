import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np
from numpy import rot90
from os.path import split


class GridPlotBase: 

    def extract(self, *args):
        self.extracts += args 

    def _parse_legend_param(self, legend):
        legend_defaults = {'loc': 'best', 'fontsize': 8, 'frameon': True}
        if legend:
            try:
                legend_defaults.update(legend)
            except TypeError:
                pass
            finally:
                legend = legend_defaults
        return legend
        
    @staticmethod
    def get_grid_xy(paths):
        """Get size of grid required to plot data by choosing the
        smallest square grid that will fit all of the data.
        """
        x = np.ceil(np.sqrt(len(paths)))
        return int(x), int(x)

    @staticmethod
    def hideaxes(axarr):
        for ax in axarr:
            for curr in ax:
                curr.spines["left"].set_visible(False)
                curr.spines["right"].set_visible(False)
                curr.spines["top"].set_visible(False)
                curr.spines["bottom"].set_visible(False)
                curr.xaxis.set_visible(False)
                curr.yaxis.set_visible(False)

    def _title_from(self, fpath, level, maxchars=None, ellipsis=False):
        dir, base = split(fpath)
        if level == 0:
            title = base
        else:
            title = self._title_from(dir, level - 1) 
        if maxchars is not None and len(title) > maxchars:
            title = title[:maxchars] 
            if ellipsis:
                title += r'$\ldots$' 
        return title
    
    def _empty_2darr(self, m, n=None):
        if n is None:
            n = m
        return [[None for x in range(n)] for y in range(m)]

    def rotated_indices(self, row, col, nrows, ncols, ostring):
        '''Function that takes (iy, ix) coordinate in original matrix and returns
        the (iyy, ixx) coordinate where that element should go in a new matrix
        that has been rotated by 'angle'°
        '''
        smat = self.rotated_serial_matrix(ostring, nrows, ncols)
        scoord = self.row_col_to_serial(row, col, nrows, ncols)
        return np.argwhere(smat == scoord)[0]

    def rotated_serial_matrix(self, ostring, nrows, ncols):
        ostring = ostring.lower()
        mat = np.arange(nrows * ncols).reshape(nrows, ncols)
        trans_dict ={
         'nwes': (0, False), 
         'nwse': (0, True), 
         'nesw': (270, False), 
         'news': (270, True),
         'sewn': (180, False), 
         'senw': (180, True), 
         'swne': (90, False), 
         'swen': (90, True)}
        angle, transp = trans_dict[ostring]
        if transp:
            mat = mat.T
        if angle == 90:
            mat = rot90(mat)
        elif angle == 180:
            mat = rot90(rot90(mat))
        elif angle == 270:
            mat = rot90(rot90(rot90(mat)))
        return mat

    def rotated_shape(self, ostring, nrows, ncols):
        return self.rotated_serial_matrix(ostring, nrows, ncols).shape

    def row_col_to_serial(self, row_y, col_x, nrows, ncols):
        return col_x + ncols * row_y


class GridPlot(GridPlotBase):
    """Plot a 2d grid of HLoops that lack ordering. Plotting on a 
    grid is just a convenient way of visualizing many HLoops.

    Args:
        hloops (sequence): hloopy.HLoops to include in the grid plot.
        legend: If `None` or `False` then no legend. If `True` then 
                a legend is put in one axes. If a dict is passed, the
                legend is shown and the dict is passed to `ax.legend()`
                as its kwargs.
        lablevel (int): Determines how each axis is labeled. Default
                        is no label. Value of 0 means label with the
                        datafile basename, 1 means datafile dirname,
                        2 means grandparent and so on.
        titleparams (dict): Optional kwargs for :code:`ax.set_title()`
    """
    def __init__(self, hloops, hideaxes=True, legend=True, lablevel=None,
                 titleparams={}):
        if hloops is None or len(hloops) == 0:
            raise ValueError("Must have at least 1 hloop to make a GridPlot.")
        self.hloops = hloops
        self.mx, self.my = self.get_grid_xy(self.hloops)
        self.fig, self.axarr = plt.subplots(self.mx, self.my, squeeze=False)
        self.legend = self._parse_legend_param(legend)
        if hideaxes:
            self.hideaxes(self.axarr)
        self.extracts = []
        self.lablevel = lablevel
        self.titleparams = titleparams

    def plot(self, **kwargs):
        """Plot all of `self.hloops` onto a 2d array of `matploblib.axes`.

        Args:
            The `kwargs` are passed to ax.plot().

        Returns:
            
        """
        self.lines_plotted = self._empty_2darr(self.mx)
        self.extract_instances = []
        for q, hl in enumerate(self.hloops):
            x, y = q // self.mx, q % self.mx
            ax = self.axarr[x][y]
            if self.lablevel is not None:
                title_style = {'fontsize': 12}
                title_style.update(self.titleparams)
                title = self._title_from(hl.fpath, level=self.lablevel,
                                         maxchars=20, ellipsis=True)
                ax.set_title(title, **title_style)
            ln = hl.plot(ax)
            self.lines_plotted[x][y] = ln
            for e in self.extracts:
                e_instance = e(hl)
                e_instance.plot(ax, **kwargs)
                self.extract_instances.append(e_instance)
            if q == 0 and self.legend:
                try:
                    ax.legend(**self.legend)
                except TypeError:
                    ax.legend()
        return self.lines_plotted



class HLoopGridPlot(GridPlotBase):
    def __init__(self, hloop_grid, legend=None, extracts=None, lablevel=None,
                 titleparams={}, hideaxes=True):
        """Plot an HLoopGrid object
        """
        self.hloop_grid = hloop_grid
        self.hloops = hloop_grid.hloops
        self.nrows = self.hloop_grid.nrows
        self.ncols = self.hloop_grid.ncols
        self.nloops = self.hloop_grid.nloops
        self.hg = hloop_grid
        self.extracts = extracts
        self.legend = self._parse_legend_param(legend)
        self.lablevel = lablevel
        self.titleparams = titleparams
        self.extracts = []
        self.hideaxes_switch = hideaxes

    def plot(self, simple_label=False, extract_plot_kwargs={}, 
             ostring='nwes', **kwargs):
        """Plot the HLoops on a grid.

        Args:
            - ostring (string): A four character string that determines the
                orientation transformation applied. Letters correspond to
                cardinal directions n, e, s, w. The first two characters
                are the location of (0, 0), the third character is the +x
                direction and the fourth character is the +y direction. The
                x and y reffered to are that of typical computer image 
                coordinates. Top left is (0, 0), +x is to the right and +y is
                down. The default orientation is 'nwes'.
            - extract_plot_kwargs (dict): kwargs for pyplot.plot when used to
                plot any extracts that may have been added.
            - kwargs: passed to pyplot.plot call that plots the HLoop data.
        """
        ostring = ostring.lower()
        final_nrows, final_ncols = self.rotated_shape(ostring, self.nrows, 
                                                      self.ncols)
        self.fig, self.axarr = plt.subplots(nrows=final_nrows, 
                                            ncols=final_ncols)
        if self.hideaxes_switch:
            self.hideaxes(self.axarr)
        self.extract_instances = []
        self.plotted_lines = []
        for i, hl in enumerate(self.hloops):
            # Plot hloop
            row_init, col_init = self.hg.mapping[i]
            row, col = self.rotated_indices(row_init, col_init, self.nrows, 
                                            self.ncols, ostring)
            ax = self.axarr[row][col]
            self.plotted_lines.append(hl.plot(ax, **kwargs))
            # Maybe add a title
            title_style = {'fontsize': 12}
            title_style.update(self.titleparams)
            if self.lablevel is not None:
                title = self._title_from(hl.fpath, level=self.lablevel,
                                         maxchars=20, ellipsis=True)
                ax.set_title(title, **title_style)
            if simple_label:
                ax.set_title('(x={}, y={})'.format(col_init, row_init), 
                             **title_style)
            # Plot extracts
            for e in self.extracts:
                e_instance = e(hl)
                e_instance.plot(ax, **extract_plot_kwargs)
                self.extract_instances.append(e_instance)
            # Maybe add a legend
            if i == 0 and self.legend:
                try:
                    ax.legend(**self.legend)
                except TypeError:
                    ax.legend()
        return self.plotted_lines



class ExtractGridPlot(GridPlotBase):
    def __init__(self, hloop_grid, extract):
        """Plot an HLoopGrid object
        """
        self.hloop_grid = hloop_grid
        self.hloops = hloop_grid.hloops
        self.nrows = self.hloop_grid.nrows
        self.ncols = self.hloop_grid.ncols
        self.nloops = self.hloop_grid.nloops
        self.hg = hloop_grid
        self.extract = extract

    def plot(self, ostring='nwes', colorbar={}, clim=None, hideaxes=False, 
             **kwargs):
        """Plot the HLoops on a grid.

        Also adds extract_instances 2d array to this ExtractGridPlot instance
        if the instances are needed for something morecomplicated than just an
        imshow of the avg_vals.


        Args:
            - ostring (string): A four character string that determines the
                orientation transformation applied. Letters correspond to
                cardinal directions n, e, s, w. The first two characters
                are the location of (0, 0), the third character is the +x
                direction and the fourth character is the +y direction. The
                x and y reffered to are that of typical computer image 
                coordinates. Top left is (0, 0), +x is to the right and +y is
                down. The default orientation is 'nwes'.
            - colorbar (dict): To add a colorbar pass True or a dict of params
                to be passed to fig.colorbar().
            - clim (tuple): vmin and vmax to be used for colorbar. Overrides
                the norm parameter if it is also passed in kwargs below.
            - hideaxes (bool): Hides the axes.
            - kwargs: passed to pyplot.imshow call. FOr example:
                    im = plt.imshow(Hcs, norm=norm, aspect='equal')
        """
        ostring = ostring.lower()
        final_nrows, final_ncols = self.rotated_shape(ostring, self.nrows, 
                                                      self.ncols)
        self.extract_avg_vals = self._empty_2darr(final_nrows, final_ncols)
        self.extract_instances = self._empty_2darr(final_nrows, final_ncols)
        for i, hl in enumerate(self.hloops):
            # Plot hloop
            row_init, col_init = self.hg.mapping[i]
            row, col = self.rotated_indices(row_init, col_init, self.nrows, 
                                            self.ncols, ostring)
            ext = self.extract(hl)
            self.extract_instances[row][col] = ext
            self.extract_avg_vals[row][col] = ext.avg_val
        self.fig, self.ax = plt.subplots()
        if clim is not None:
            norm = Normalize(*clim)
            kwargs.update(norm=norm)
        res = self.ax.imshow(self.extract_avg_vals, **kwargs)
        if colorbar:
            colorbar = {} if colorbar is True else colorbar
            self.fig.colorbar(res, **colorbar)
        return res

    def hideaxes(self, ax):
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
