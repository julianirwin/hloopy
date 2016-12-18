import pandas as pd
import numpy as np
from hloopy.util import rightpad, find_all


class HLoop:
    """An hloopy.HLoop represents a single hysteresis loop. It has
    both x and y datasets.
    """
    def __init__(self, fpath, read_func=pd.read_csv, **kwargs):
        self.fpath = fpath
        self._read_data(f=read_func, **kwargs)

    def _read_data(self, f, **kwargs):
        self.df = pd.read_csv(self.fpath, **kwargs)

    def num_cols(self):
        """Number of columns in the linked data file.

        Returns:
            n (int): Number of columns.
        """
        return len(self.df.columns)

    def x(self):
        try:
            xcol = self.xcol[0]
            return self.df.ix[:, xcol]
        except (AttributeError, ValueError):
            return self.df.ix[:, 0]

    def y(self):
        try:
            ycol = self.ycol
            ycol = ycol if len(ycol) > 1 else ycol[0]
            return self.df.ix[:, ycol]
        except (AttributeError, ValueError):
            return self.df.ix[:, 1]

    def setas(self, *args, **kwargs):
        # Do nothing if no args are passed.
        if len(args) == 0:
            return
        # If first arg is a string, treat that as the column specifier
        elif len(args) == 1 and isinstance(args[0], str):
            s = args[0]
            if len(s) > self.num_cols():
                msg = '`len(x)` cannot be greater than `num_cols()`'
                raise ValueError(msg)
            else:
                s = rightpad(s, '.', self.num_cols())
                self.xcol = np.array([s.find('x')])
                self.ycol = np.array(list(find_all(s, 'y')))
        # Otherwise treat kwargs as the column specifier
        else:
            self.xcol = np.array(kwargs.get('x', None))
            self.ycol = np.array(kwargs.get('y', None))

    def plot(self, ax, plotf='plot', **kwargs):
        """Plot hloop onto a `matploblib.axes`. The columns that are
        used are determined according to the values given to
        `setas()`, or automatically if `setas()` wasn't used.

        Args:
            ax (axes):  Object to be plotted on.
            plotf (string):  Plotting function. Must be a function that
                             is provided by the `axes` object.
            kwargs:  These are provided to the axes.plotf function.

        Returns:
            Whatever the `axes.plotf` function returns.

        """
        f = getattr(ax, plotf)
        try:
            x = self.df.ix[:, self.xcol]
            y = self.df.ix[:, self.ycol]
            res = f(x, y, **kwargs)
        except (AttributeError, ValueError):
            x = self.df.ix[:, 0]
            if self.num_cols() == 1:
                res = f(x, **kwargs)
            else:
                y = self.df.ix[:, 1]
                res = f(x, y, **kwargs)
        return res
