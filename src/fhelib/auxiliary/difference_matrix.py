from fhelib import Ciphertext
from fhelib.auxiliary.difference import difference
import numpy as np


def difference_matrix(a: Ciphertext) -> np.matrix:
    """
    Method to output a difference matrix given one vector

    Returns: difference matrix D where D_ij = A_i - A_j for all i, j
    """

    d = np.empty(shape=(0, a.size), dtype=complex)

    for i in range(a.size): 
        a_copy = np.full(a.shape, a[i])
        temp_row = difference(a, a_copy)
        d = np.vstack((d, temp_row))
        
    return d
