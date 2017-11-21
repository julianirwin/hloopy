import numpy as np
import pandas as pd
from os.path import split

class ExtractBase:
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

    def plot(self, ax, **kwargs):
        """Convert the data represented in this class into a graphical
        representation and then plot it on :code:`ax`, a mpl.axes object.

        Args:
            ax (matplotlib.axes): Axes to plot extract on.
            kwargs: Keyword parameters of :code:`matplotlib.axes.plot`

        Returns:
            Same as `matplotlib.axes.plot`
        """
        styles = {'linestyle': 'none', 
                  'marker': 'o', 
                  'label': self.label_short,
                  'alpha': 0.7,
                  'mew': 1,
                  'ms': 8}
        styles.update(kwargs)
        ax.plot(self.xs, self.ys, **styles)


def coercivity(hloop, avg_width=10):
    """Find the coercivity of an hloop, determined as the x-intercepts of
    each (centered with :code:`y -= y.mean()`) branch.

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
    Hc = abs(Hc_avgs[1] - Hc_avgs[0])/2.0
    hc_indices = np.array(hc_indices)
    return ExtractBase(label='coercivity',
                       label_short='Hc',
                       avg_val=Hc,
                       xcoords=x[hc_indices],
                       ycoords=y[hc_indices],
                       indices=hc_indices)


class Coercivity(ExtractBase):
    """Find the coercivity of an hloop, determined as the x-intercepts of
    each (centered with :code:`y -= y.mean()`) branch.
    """

    def __init__(self, hloop, avg_width=10):
        self.label = 'coercivity'
        self.label_short = 'Hc'
        self.hloop = hloop

        x, y = np.array(hloop.x()), np.array(hloop.y())
        N = len(y)
        yc = y - y.mean()  # y-centered
        ych0, ych1 = yc[:N//2], yc[N//2:]  # y-centered-half0/1
        hc_indices = list(np.argmin(np.abs(y)) for y in (ych0, ych1))
        hc_indices[1] += N//2
        Hc_avgs = [x[i - avg_width:i + avg_width].mean() for i in hc_indices]
        Hc = abs(Hc_avgs[1] - Hc_avgs[0])/2.0
        hc_indices = np.array(hc_indices)

        self.avg_val = Hc
        self.xcoords = self.xs = x[hc_indices]
        self.ycoords = self.ys = y[hc_indices]
        self.indices = self.ixs =hc_indices


class Remanence(ExtractBase):
    """Find the remanence of an hloop, determined as the y-intercepts of
    each branch.
    """

    def __init__(self, hloop, avg_width=10):
        self.label = 'remanence'
        self.label_short = 'Mrem'
        self.hloop = hloop

        x, y = np.array(self.hloop.x()), np.array(self.hloop.y())
        extract_dict = self.remanence(x, y, avg_width)

        self.avg_val = extract_dict['avg_val']
        self.xcoords = self.xs = extract_dict['xcoords']
        self.ycoords = self.ys = extract_dict['ycoords']
        self.indices = self.ixs = extract_dict['indices']

    @staticmethod
    def remanence(x, y, avg_width):
        N = len(x)
        # Force array len to be a multiple of 4. There are usually
        # thousands of points in a MOKE measurement, cutting the last 3 
        # (worst case) will not have a significant effect on the result.
        N -= (N % 4)
        x = x[:N]
        y = y[:N]
        # Divide into 4 quarters
        #    import pdb; pdb.set_trace()
        inds = np.arange(N).reshape(4, N//4)
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
        return dict(label='remanence',
                    label_short='Mrem',
                    avg_val=mrem,
                    xcoords=x[mrem_indices],
                    ycoords=y[mrem_indices],
                    indices=mrem_indices)


class Saturation(ExtractBase):
    """Find the positive and negative saturaiton values of the hysteresis loop
    using a counting method. For both the positive and negative halves of the
    loop (in the y direction) compute a histogram. At saturation there will be
    many more points per bin than in the switching region.  Find the bin with
    the most points pmax, and define threshold as :code:`pthresh = thresh *
    pmax`.  The saturation is the average value of all the points in the bins
    with height greater than :code`ptresh`. Pass :code`bins` or :code`thresh`
    when initializing this class if you wish.
    """

    def __init__(self, hloop, bins=50, thresh=0.25):
        self.label = 'Saturation'
        self.label_short = 'Sat'
        self.hloop = hloop

        x, y = np.array(self.hloop.x()), np.array(self.hloop.y())
        extract_dict = self.saturation(x, y, bins=bins, thresh=thresh)

        self.avg_val = extract_dict['avg_val']
        self.xcoords = self.xs = extract_dict['xcoords']
        self.ycoords = self.ys = extract_dict['ycoords']
        self.indices = self.ixs = extract_dict['indices']

    @staticmethod
    def saturation(x, y, bins=50, thresh=0.25):
        heights, bins = np.histogram(y, bins=bins)

        # thresh_y = self.get_threshold_y(heights, bins, thresh=thresh)
        # Compute the y thresholds
        lbins = bins[:-1]
        binw = bins[1] - bins[0]
        igt0, ilt0 = lbins > 0, lbins < 0
        thresh_y = []
        for half, dx, ax in zip((igt0, ilt0), (0.0, binw), (1.0, -1.0)):
            hthresh = thresh * heights[half].max()
            saturated = np.where(half & (heights > hthresh))
            # dx is 0 for the gt0 side and binwidth for the lt0 side
            thresh_y.append(ax * min(abs(lbins[saturated])) + dx)

        # Average over all points outside the thresholds to get the saturations
        y_saturations = (y[y > thresh_y[0]].mean(), y[y < thresh_y[1]].mean())

        return dict(avg_val=np.abs(y_saturations).mean(),
                    xcoords=np.array([np.min(x), np.max(x)]),
                    ycoords=np.array(y_saturations),
                    indices=None,
                    thresh_y=thresh_y)

    def plot(self, ax, **kwargs):
        defaults = dict(linestyles='dashed', label=self.label_short, zorder=3)
        defaults.update(kwargs)
        return ax.hlines(y=self.ys, xmin=self.xs[0], xmax=self.xs[1], 
                         **defaults)
        

class ReflectivityScMOKE(hlpy.extract.ExtractBase):
    def __init__(self, hloop):
        """Reflectivity is read from first line of data file by matching
        with a float regex. Works on Scanning MOKE labview program output.
        """
        self.label = 'reflectivity'
        self.label_short = 'Ref.(V)'
        self.hloop = hloop

        self.avg_val = self.reflectivity()
        self.xcoords = self.xs = None
        self.ycoords = self.ys = None
        self.indices = self.ixs = None
    
    def plot(self, ax, **kwargs):
        pass
    
    def reflectivity(self):
        with open(self.hloop.fpath) as f:
            line = f.readline()
            ref = re.search("([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)", line)
        return float(ref.groups()[0])



class ExtractWriter:
    """ The extracts given to the writer must have:
        - hloop attribute 
          - Also, extracts are grouped by the datafiles they came from not the
            actual HLoop instances.
        - label
        - avg_val
    And they may also optionally have:
        - std_val
    """
    def __init__(self, titlelevel=0):
        self.titlelevel = titlelevel
        self.d = {}

    def add(self, extract):
        key = extract.hloop.fpath 
        current = self.d.get(key, [])
        current.append(extract)
        self.d[key] = current

    def to_csv(self, savefile, row_index_label='File', **kwargs):
        """Wrapper of pandas.to_csv."""
        defaults = {'sep': '\t'}
        defaults.update(kwargs)
        df = self._parse_d_to_df(row_index_label)
        return df.to_csv(path_or_buf=savefile, **defaults)
    
    def to_string(self,row_index_label='File'):
        df = self._parse_d_to_df(row_index_label)
        return df.to_string()

    def to_df(self,row_index_label='File'):
        df = self._parse_d_to_df(row_index_label)
        return df

    def _parse_d_to_df(self, row_index_label='File'):
        # get a list of sorted unique extracts (using their label attributes)
        labels = sorted(set([e.label for es in self.d.values() for e in es]))
        titles, rows = [], []
        for path, extracts in self.d.items():
            titles.append(self._title_from(path, self.titlelevel))
            row = [float('nan') for i in labels]
            for e in extracts:
                i = labels.index(e.label)
                row[i] = e.avg_val
            rows.append(row)
        data = np.array(rows)
        df_d = {l: data[:,i] for i, l in enumerate(labels)}
        df_d[row_index_label] = titles
        df = pd.DataFrame(data=df_d)
        df.set_index(row_index_label, inplace=True)
        return df

    def _title_from(self, fpath, level):
        dir, base = split(fpath)
        if level == 0:
            return base
        else:
            return self._title_from(dir, level - 1)

    def __str__(self):
        return self.to_string()



