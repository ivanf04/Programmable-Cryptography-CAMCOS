from fhelib import Ciphertext
from fhelib.auxiliary.difference import difference
import numpy as np
"""
Method to output a distance matrix given one vector
"""

def difference_matrix(a: Ciphertext) -> np.matrix:
    d = np.empty(shape=(0, a.size), dtype=complex)
    for i in range(a.size): 
        a_copy = np.full(a.shape, a[i])
        temp_row = difference(a, a_copy)
        print(i, a_copy, temp_row)
        d = np.vstack((d, temp_row))
    return d
