def rightpad(x, c, w):
    """Rightpad string `x` with `c` using width `w`.
    """
    return x + c * (w - len(x))
