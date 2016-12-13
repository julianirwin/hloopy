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
