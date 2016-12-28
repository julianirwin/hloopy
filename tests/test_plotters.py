from hloopy import HLoop
from hloopy.plotters import *
from hloopy.extract import Coercivity, Remanence, Saturation
from nose.tools import assert_equal, raises
from os.path import join, realpath, dirname


SHOW_PLOTS = False
TESTPATH = realpath(dirname(__file__))


class TestGridPlot:
    @classmethod
    def setup(cls):
        datapath = join(TESTPATH, 'data', 'poleup_poledown')
        datanames = ('0deg_400G_down_0', 
                     '0deg_400G_up_0', 
                     '0deg_400G_down_1', 
                     '0deg_400G_up_1')
        cls.datanames = [join(datapath, name) for name in datanames]
        cls.hls = [HLoop(f, sep='\t', skiprows=5) for f in cls.datanames]

    @classmethod
    def teardown(cls):  
        plt.close()

    def test_grid_xy(self):
        n = (1, 3, 4, 5, 8, 9, 10, 15, 16, 17)
        x = (1, 2, 2, 3, 3, 3, 4, 4, 4, 5)
        for ni, xi in zip(n, x):
            yield self.check_grid_xy, ni, xi

    def check_grid_xy(self, ni, xi):
        res = GridPlot.get_grid_xy(range(ni))[0]
        assert_equal(res, xi)

    def test_title_from(self):
        gp = GridPlot(self.hls[:1])
        title = gp._title_from('/dir/1_y=142um_I=5mA_Vpp=3.0V', level=0,
                               maxchars=20, ellipsis=True)
        correct = r'1_y=142um_I=5mA_Vpp=$\ldots$'
        assert_equal(title, correct)
        
    @raises(ValueError)
    def test_plot_zero(self):
        GridPlot([])

    def test_plot(self):
        self.run_plot(self.hls[:1])
        self.run_plot(self.hls[:1], hideaxes=True)
        self.run_plot(self.hls[:2])
        self.run_plot(self.hls[:4])
        self.run_plot(self.hls[:4], hideaxes=True)
    
    def run_plot(self, hls, **kwargs):
        gp = GridPlot(hls, **kwargs)
        gp.plot()
        if SHOW_PLOTS: plt.show()
    
    def test_plot_with_extracts(self):
        gp = GridPlot(self.hls[:1], hideaxes=True, legend={'fontsize': 10})
        gp.extract(Coercivity, Remanence, Saturation)
        gp.plot()
        if SHOW_PLOTS: plt.show()

    def test_plot_four_with_extracts(self):
        gp = GridPlot(self.hls, hideaxes=True, legend=True)
        gp.extract(Coercivity, Remanence, Saturation)
        gp.plot()
        if SHOW_PLOTS: plt.show()

    def test_plot_titles(self):
        self.run_plot(self.hls[:1], lablevel=None)
        self.run_plot(self.hls[:1], lablevel=0)
        self.run_plot(self.hls[:1], lablevel=1)
        self.run_plot(self.hls, lablevel=0)
