import numpy as np

class Extract:
    """Container for parameters extracted from a hysteresis loop.
    A noun not a verb (vanilla extract, not extract the minerals).

    Attributes:
        xcoords (numpy.ndarray): List of extracted x-coordinates
        ycoords (numpy.ndarray): List of extracted y-coordinates
        indices (numpy.ndarray): Indices of the x and y coords in the HLoop
                                 from where they came.
        
    """
    def __init__(self, label, label_short, avg_val, xcoords, ycoords, indices):
        self.label = label
        self.label_short = label_short
        self.avg_val = avg_val
        self.xcoords = self.xs = xcoords
        self.ycoords = self.ys = ycoords
        self.indices = self.ixs = indices

    def __str__(self):
        return str({'avg_val': self.avg_val, 'xcoords': self.xcoords,
                    'ycoords': self.ycoords, 'indices': self.indices})


class ExtractPlot:
    def __init__(self, hloop):
        self.hl = hloop
        self._fs = []

    def setas(self, *args, **kwargs):
        return self.hl.setas(*args, **kwargs)

    def extract(self, f):
        self._fs.append(f)

    def plot(self, ax):
        self._assert_one_ycol()
        self.hl.plot(ax)
        for f in self._fs:
            e = f(self.hl)
            ax.plot(e.xs, e.ys, 'o', label=e.label_short)
    
    # Private methods

    def _assert_one_ycol(self):
        try:
            ny = len(self.hl._ycol)
            if ny > 1: 
                msg = 'ExtractPlot only supports HLoops that use one ycol'
                raise ValueError(msg)
        except AttributeError:
            pass


def coercivity(hloop, avg_width=10):
    """Find the coercivity of an hloop, determined as the x-intercepts of
    each (centered with `y -= y.mean()`) branch.

    Args:
        hloop (hloopy.hloop): Hloop to be operated on

    Returns:
        extracted_params (hloop.Extract)
    """
    x, y = np.array(hloop.x()), np.array(hloop.y())
    N = len(y)
    yc = y - y.mean()  # y-centered
    ych0, ych1 = yc[:N//2], yc[N//2:]  # y-centered-half0/1
    hc_indices = list(np.argmin(np.abs(y)) for y in (ych0, ych1))
    hc_indices[1] += N//2
    Hc_avgs = tuple(x[i - avg_width:i + avg_width].mean() for i in hc_indices)
    Hc = abs(Hc_avgs[1] - Hc_avgs[0])
    hc_indices = np.array(hc_indices)
    return Extract(label='coercivity',
                   label_short='Hc',
                   avg_val=Hc,
                   xcoords=x[hc_indices],
                   ycoords=y[hc_indices],
                   indices=hc_indices)


def remanence(hloop):
    """Find the remanence of an hloop, determined as the y-intercepts of each
    branch.

    Args:
        hloop (hloopy.hloop): Hloop to be operated on.
        center (bool): If true, center the curve in the x-direction before
                       computing the remanence.

    Returns:
        extracted_params (hloop.Extract)
    """
    
    pass


