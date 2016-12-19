from hloopy.util import *
from nose.tools import assert_equal


def test_rightpad():
    assert_equal(rightpad('xy', '.', 3), 'xy.')

