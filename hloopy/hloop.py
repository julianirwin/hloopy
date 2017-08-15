import pandas as pd
import numpy as np
from hloopy.util import rightpad


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

    def _x(self):
        """Get this HLoop's x-axis data. In a custom subclass of
        hloopy.HLoop this can be overridden to allow custom 
        transformation/manipulation of the x data. The only
        requirement is that it returns an numpy.ndarray like object
        that will have the same length as the one HLoop.y() returns.
        """
        try:
            xcol = self.xcol[0]
            return self.df.ix[:, xcol]
        except (AttributeError, ValueError):
            return self.df.ix[:, 0]
    x = _x

    def _y(self):
        """Get this HLoop's y-axis data. In a custom subclass of
        hloopy.HLoop this can be overridden to allow custom 
        transformation/manipulation of the y data. The only
        requirement is that it returns an numpy.ndarray like object
        that will have the same length as the one HLoop.x() returns.
        """
        try:
            ycol = self.ycol[0]
            return self.df.ix[:, ycol]
        except (AttributeError, ValueError):
            return self.df.ix[:, 1]
    y = _y

    def setas(self, *args, **kwargs):
        """Mark which columns should be respectively set as the 
        x-axis and y-axis data. There are ways to call this function:

          - Pass a single string which has a length equal to the number of
            columns in this HLoop's datafile. A '.' represents an unused
            column, 'x' and 'y' represent the columns to mark as x and y.
            For example if there are five columns: 

                `setas('..x.y')`

          - Use the kwargs 'x' and 'y' whose values are the int 
            indices of the x and y columns within the datafile:

                `setas(x=2, y=3)`

        """
        # Do nothing if no args are passed.
        if len(args) == 0 or args[0] is None:
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
                self.ycol = np.array([s.find('y')])
        # Otherwise treat kwargs as the column specifier
        else:
            self.xcol = int(np.array(kwargs.get('x', None)))
            self.ycol = int(np.array(kwargs.get('y', None)))


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
        styles = {'color': 'darkslategrey'}
        styles.update(kwargs)
        try:
            res = f(self.x(), self.y(), **kwargs)
        except (AttributeError, ValueError):
            x = self.df.ix[:, 0]
            if self.num_cols() == 1:
                res = f(x, **styles)
            else:
                y = self.df.ix[:, 1]
                res = f(x, y, **styles)
        return res


class HLoopGrid:
    """A 2d grid of HLoops.

    Args:
        hloops (sequence): A sequence of hloopy.HLoop object
        mapping_func (callable): A function that maps an HLoop object
            to a (row, column). If left as `None` the default behavior
            is to create a square or nearly square grid and to assign
            hloops to locations on the grid sequentially.
    """
    def __init__(self, hloops, mapping_func=None):
        self._verify_hloops(hloops)
        self.hloops = hloops
        self.nloops = len(hloops)
        if mapping_func is None:
            self.shape = self._pick_shape(self.nloops)
            self.nrows = self.shape[0]
            self.ncols = self.shape[1]
            # mapping[ith hloop of sequence] = (row, col) in grid to be placed
            self.mapping = [divmod(i, self.ncols) for i in range(self.nloops)]
        else:
            self._assert_mapping_func_valid(mapping_func, hloops[0])
            self.mapping = [mapping_func(hl) for hl in hloops]
            self.nrows = max([x[0] for x in mapping])
            self.ncols = max([x[1] for x in mapping])
            self.shape = (self.nrows, self.ncols)

    def _pick_shape(self, N):
        """Pick a good grid shape for N HLoops."""
        ncols = int(np.ceil(np.sqrt(N)))
        nrows = int(np.ceil(N / ncols))
        return nrows, ncols
    
    def _verify_hloops(self, hloops):
        if hloops is None:
            raise ValueError("Parameter 'hloops' cannot be None")
        if len(hloops) == 0:
            msg = "Parameter 'hloops' must be a sequence of len > 0"
            raise ValueError(msg)
        for hl in hloops:
            if not isinstance(hl, HLoop):
                msg = "'hloops' arg has 1 or more elements that are not hloops"
                raise(ValueError(msg))

    def _assert_mapping_func_valid(self, func, hloop):
        """Assert that mapping_func takes an hloop and returns a (row, col)
        sequence.
        """
        output = func(hloop)
        if not len(output) == 2:
            raise ValueError("'mapping_func' not outputting length 2 sequence")
        if not isinstance(output[0], int) and isinstance(output[1], int):
            msg = "'mapping_func' sequence output contains non ints"
            raise ValueError(msg)


