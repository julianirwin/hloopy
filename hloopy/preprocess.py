import numpy as np

def crop(arr, numcycles, precrop=0, postcrop=0):
    """Crop out some initial and final cycles in data that contains
    several cycles.

    Args:
        arr (numpy.ndarray): Sequence to operate on.
        numcycles (int): number of cycles in the total array. 
        precrop (int): number of cycles to remove from the beginning of the 
                       array
        postcrop (int): number of cycles to remove from the end of the array
    
    Returns:
        The cropped sequence, as an ndarray.
    """
    N = len(arr)
    cyclen = N/numcycles
    arr = arr[int(precrop * cyclen):]
    if postcrop * cyclen > 0:
        arr = arr[:int(-postcrop * cyclen)]
    return arr


def average_cycles(arr, numcycles):
    """For cyclical data, split into cyles and then average the cycles 
    together. This is for data where signal averaging is desired.

    Args:
        arr (ndarray): Array to be operated on.
        numcycles: Number of cycles in the total array. The array must divide
                   evenly by this number, otherwise a call to reshape() will
                   raise.
    
    Returns:
        The signal averaged ndarray.
    """
    N = len(arr)
    cyclen = N/numcycles
    return arr.reshape(numcycles, cyclen).mean(axis=0)


def average_points(arr, d):
    """Average every `d` points together. This creates a new array so
    be careful if using on a large dataset.

    Args:
        arr (ndarray-like): Array to be operated on.
        d (int): Number of points to average together. Must divide array 
                 evenly otherwise unexpected results could occur, or a raise
                 depending on the type of array passed.
    """
    return np.array(list(arr[i:i+d].mean() for i in range(0, len(arr), d)))
