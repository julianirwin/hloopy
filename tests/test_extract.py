from hloopy import HLoop
from hloopy.extract import ExtractPlot, coercivity, remanence, saturation
from nose.tools import assert_equal, assert_less
import os
import matplotlib.pyplot as plt
import numpy as np

SHOW_PLOTS = False

testpath = os.path.realpath(os.path.dirname(__file__))

class TestExtractPdn0:
    @classmethod
    def setup(cls):
        fpath = os.path.join(testpath, 'data', 'poleup_poledown', 
                             '0deg_400G_down_0')
        cls.hl = HLoop(fpath, sep='\t', skiprows=5)
        cls.hl.setas('x.y')
        cls.xtol =  0.02 * np.max(cls.hl.x())
        cls.ytol =  0.02 * np.max(cls.hl.y())
        cls.fig, cls.ax = plt.subplots()

    @classmethod
    def teardown(cls):
        plt.close()

    def test_coercivity(self):
        res = coercivity(self.hl)

    def test_coercivity_plot(self):
        self.hl.plot(self.ax, ls='-')
        ep = ExtractPlot(self.hl)
        ep.extract(coercivity)
        ep.plot(self.ax)
        if SHOW_PLOTS: plt.show()

    def test_remanence(self):
        res = remanence(self.hl)

    def test_remanence_plot(self):
        self.hl.plot(self.ax, ls='-')
        ep = ExtractPlot(self.hl)
        ep.extract(remanence)
        ep.plot(self.ax)
        if SHOW_PLOTS: plt.show()

    def test_(self):
        res = saturation(self.hl)

    def test_remanence_plot(self):
        self.hl.plot(self.ax, ls='-')
        ep = ExtractPlot(self.hl)
        ep.extract(saturation)
        ep.plot(self.ax)
        if SHOW_PLOTS: plt.show()
