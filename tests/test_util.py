from hloopy.util import *
from nose.tools import assert_equal


def test_rightpad():
    assert_equal(rightpad('xy', '.', 3), 'xy.')


def test_find_all():
    assert_equal(list(find_all('x.yy', 'y')), [2, 3])
