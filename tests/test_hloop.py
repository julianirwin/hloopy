from hloopy import HLoop
from nose.tools import assert_equal
import os

testpath = os.path.realpath(__file__)

class TestHLoopPupPdn:
    @classmethod
    def setup(cls):
        fpath = os.path.join(testpath, 'data', '0deg_400G_down_0')
        hl = Hloop(fpath)
