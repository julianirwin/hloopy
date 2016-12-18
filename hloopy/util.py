def rightpad(x, c, w):
    """Rightpad string `x` with `c` using width `w`.
    """
    return x + c * (w - len(x))

def find_all(a_str, sub):
    """Find all non-overlapping instances of `sub` in `a_str`.

    Returns:
        locs (generator): indices of all locations of `sub`.
    """
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches
