from hloopy import HLoop
from hloopy.extract import (coercivity, Coercivity, Remanence, Saturation,
                            ExtractWriter)
from nose.tools import assert_equal, assert_less
import os
import matplotlib.pyplot as plt
import numpy as np
from shutil import rmtree

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

    def test_coercivity_function_plot(self):
        self.hl.plot(self.ax, ls='-')
        hc_extract = coercivity(self.hl)
        hc_extract.plot(self.ax, ls='none', marker='o')
        if SHOW_PLOTS: plt.show()

    def test_coercivity_class_plot(self):
        self.hl.plot(self.ax, ls='-')
        hc_extract = Coercivity(self.hl)
        hc_extract.plot(self.ax, ls='none', marker='o')
        if SHOW_PLOTS: plt.show()

    def test_remanence_class_plot(self):
        self.hl.plot(self.ax, ls='-')
        mr_extract = Remanence(self.hl)
        mr_extract.plot(self.ax, ls='none', marker='o')
        if SHOW_PLOTS: plt.show()

    def test_saturation_class_plot(self):
        self.hl.plot(self.ax, ls='-')
        sat_extract = Saturation(self.hl)
        sat_extract.plot(self.ax, alpha=0.7, zorder=10)
        if SHOW_PLOTS: plt.show()


class TestExtractWriter:
    @classmethod
    def setup(cls):
        fname = '0deg_400G_down_0'
        fpath = os.path.join(testpath, 'data', 'poleup_poledown', fname)
        cls.hl = HLoop(fpath, sep='\t', skiprows=5)
        cls.writer = ExtractWriter()
        cls.hl.setas('x.y')
        try:
            os.mkdir(os.path.join(testpath, 'save'))
        except FileExistsError:
            pass
        cls.savepath = os.path.join(testpath, 'save', fname + '.txt')

    @classmethod
    def teardown(cls):
        rmtree(os.path.join(testpath, 'save'))
        

    def test_write_single_hl(self):
        mr_extract = Remanence(self.hl)
        sat_extract = Saturation(self.hl)
        writer = ExtractWriter()
        writer.add(mr_extract)
        writer.add(sat_extract)
        writer.to_csv(self.savepath)

