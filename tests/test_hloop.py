from hloopy import HLoop
from nose.tools import assert_equal, raises
import os
import matplotlib.pyplot as plt

SHOW_PLOTS = False

testpath = os.path.realpath(os.path.dirname(__file__))

class TestHLoopPupPdn:
    @classmethod
    def setup(cls):
        fpath = os.path.join(testpath, 'data', 'poleup_poledown', 
                             '0deg_400G_down_0')
        cls.hl = HLoop(fpath, sep='\t', skiprows=5)
        cls.fig, cls.ax = plt.subplots()

    @classmethod
    def teardown(cls):
        plt.close()

    def test_num_cols(self):
        assert_equal(self.hl.num_cols(), 3)

    def test_xy_plot_unset(self):
        self.hl.plot(self.ax)
        if SHOW_PLOTS: plt.show()

    def test_setas_dict(self):
        self.hl.setas(x=0, y=1)
        self.hl.plot(self.ax)
        if SHOW_PLOTS: plt.show()

    def test_setas_dict_twoy(self):
        self.hl.setas(x=0, y=(1, 2))
        self.hl.plot(self.ax)
        if SHOW_PLOTS: plt.show()

    def test_setas_dict_str(self):
        self.hl.setas('x.y')
        self.hl.plot(self.ax)
        if SHOW_PLOTS: plt.show()
