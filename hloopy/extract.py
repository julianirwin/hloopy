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


def remanence(hloop, avg_width=10):
    """Find the remanence of an hloop, determined as the y-intercepts of each
    branch.

    Args:
        hloop (hloopy.hloop): Hloop to be operated on.
        center (bool): If true, center the curve in the x-direction before
                       computing the remanence.

    Returns:
        extracted_params (hloop.Extract)
    """
    x, y = np.array(hloop.x()), np.array(hloop.y())
    N = len(x)
    # Divide into 4 quarters
    #    import pdb; pdb.set_trace()
    inds = np.arange(N).reshape(4, N//4) - 1
    yq03 = y[inds[[0, 3]]].reshape(N//2)  # yq03 = y quarters 0 and 3
    xq03 = x[inds[[0, 3]]].reshape(N//2)
    yq12 = y[inds[[1, 2]]].reshape(N//2)
    xq12 = x[inds[[1, 2]]].reshape(N//2)
    # get indices of B=0 in the half-arrays
    xmq03i = np.argmin(np.abs(xq03))  # xmq03i = indsof x min quarters 0 and 3
    xmq12i = np.argmin(np.abs(xq12))
    # convert to indices in the full arrays
    rem_ind_03 = inds[[0, 3]].reshape(N//2)[xmq03i]
    rem_ind_12 = inds[[1, 2]].reshape(N//2)[xmq12i]
    # Average over the kernel size
    yq03avg = abs(np.mean(yq03[xmq03i - avg_width:xmq03i + avg_width]))
    yq12avg = abs(np.mean(yq12[xmq12i - avg_width:xmq12i + avg_width]))
    mrem = (yq03avg + yq12avg)/2.
    mrem_indices = np.array([rem_ind_03, rem_ind_12])
    # return mrem, np.array((rem_ind_03, rem_ind_12))
    return Extract(label='remanence',
                   label_short='Mrem',
                   avg_val=mrem,
                   xcoords=x[mrem_indices],
                   ycoords=y[mrem_indices],
                   indices=mrem_indices)


def get_threshold_y(heights, bins, thresh=0.25):
    lbins = bins[:-1]
    binw = bins[1] - bins[0]
    igt0, ilt0 = lbins > 0, lbins < 0
    xthresh = []
    for half, dx, ax in zip((igt0, ilt0), (0.0, binw), (1.0, -1.0)):
        hthresh = thresh * heights[half].max()
        saturated = np.where(half & (heights > hthresh))
        # dx is 0 for the gt0 side and binwidth for the lt0 side
        xthresh.append(ax * min(abs(lbins[saturated])) + dx)
    return xthresh


def saturation(hloop, bins=50, thresh=0.25):
    x, y = np.array(hloop.x()), np.array(hloop.y())
    heights, bins = np.histogram(y, bins=bins)
    thresh_y = get_threshold_y(heights, bins, thresh=thresh)
    y_saturations = (y[y > thresh_y[0]].mean(), y[y < thresh_y[1]].mean())
    return Extract(label='saturation',
                   label_short='sat',
                   avg_val=np.abs(y_saturations).mean(),
                   xcoords=np.array([np.min(x), np.max(x)]),
                   ycoords=np.array(y_saturations),
                   indices=None)
