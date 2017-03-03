import matplotlib.pyplot as plt
import numpy as np
from os.path import split


class GridPlot:
    """Plot a 2d grid of HLoops.

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
#        elabs = [e.label for e in self.extracts]
#        self.extract_vals = {k: [] for k in elabs}
        self.extract_instances = []
        for q, hl in enumerate(self.hloops):
            x, y = q // self.mx, q % self.mx
            # i_ax, j_ax = self.get_axarr_coords(origin, xplus, yplus, 
            #                                    self.mx, x, y)
            # ax = axarr[i_ax, j_ax]
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
#                self.extracts_plotted[e.label].append(e.avg_value)
            if q == 0 and self.legend:
                try:
                    ax.legend(**self.legend)
                except TypeError:
                    ax.legend()
        return self.lines_plotted

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
    
    # def _truncate_title(self, title, maxchars=None, ellipsis=False):
    #     if maxchars is not None and len(title) > maxchars:
    #         title = title[:maxchars] 
    #         if ellipsis:
    #             title += r'$\ldots$' 


    # @staticmethod
    # def get_axarr_coords(origin, xplus, yplus, N, i, j):
    #     origin, xplus, yplus = (x.upper() for x in (origin, xplus, yplus))
    #     verify_directions(origin, xplus, yplus)
    #     xh, yh, zh = np.array((1, 0, 0)), np.array((0, 1, 0)), np.array((0, 0, 1))
    #     unit_vs = {'N': yh, 'E': xh,
    #                'S': -yh, 'W': -xh}
    #     deg_ccw = {'NW': 0, 'NE': -90, 'SE': 180, 'SW': 90}
    #     need_trans = (-zh == np.cross(unit_vs[xplus], unit_vs[yplus])).all()
    #     if need_trans:
    #         i, j = j, i
    #     return matrix_rotate_indices(N, i, j, deg_ccw[origin])

    # @staticmethod
    # def verify_directions(origin, xplus, yplus):
    #     if (origin[0] not in ('N', 'S')) or (origin[1] not in ('E', 'W')):
    #         raise ValueError('Parameter "origin" must be "(N|S)(E|W)" w/o parens.')
    #     total = origin + xplus + yplus
    #     for c in 'NESW':
    #         if total.count(c) != 1:
    #             emsg = 'xplus and yplus must use the two directions not in origin'
    #             raise ValueError(emsg)

    # @staticmethod
    # def matrix_rotate_indices(N, i, j, deg_ccw):
    #     N -= 1
    #     d = {0: (i, j), 90: (N - j, i), -90: (j, N - i), 180: (N - i, N - j)}
    #     try:
    #         return d[deg_ccw]
    #     except KeyError:
    #         raise ValueError('Parameter deg_ccw must be one of (0, 90, -90, 180).')
