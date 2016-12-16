import numpy as np


def coercivity(hloop):
    """Find the coercivity of an hloop, determined as the x-intercepts of
    each (centered with `y -= y.mean()`) branch.

    Args:
        hloop (hloopy.hloop): Hloop to be operated on

    Returns:
        A dict with two elements:
            {'coercivity': (plus_side, minus_side),
             'indicies': (plus_side, minus_side)}
    """
    pass


def remanence(hloop):
    """Find the remanence of an hloop, determined as the y-intercepts of each
    branch.

    Args:
        hloop (hloopy.hloop): Hloop to be operated on.
        center (bool): If true, center the curve in the x-direction before
                       computing the remanence.

    Returns:
        A dict with two elements:
            {'remanence': (plus_side, minus_side),
             'indicies': (plus_side, minus_side)}
    """
    
    pass


