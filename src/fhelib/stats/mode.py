import numpy as np
from fhelib import Ciphertext
from fhelib.auxiliary.difference_matrix import difference_matrix
from fhelib.auxiliary.equality import fhe_equality
from fhelib.lowlevel.sum import intravector_sum_naive, intravector_sum
from fhelib.auxiliary.max import fhe_max
"""
TODO implement Mode in FHE 
Required methods: distance, gif, max, eqaulity
"""

def mode(x: Ciphertext):
    # create differnce matrix
    d = difference_matrix(x)
    print(f"difference matrix:\n{d}")
    equailt_matrix = np.empty(shape=d.shape)
    for i in range(d.shape[0]):
        equailt_matrix[i] = fhe_equality(d[i], 0.0)
    print(f"equality matrix:\n{equailt_matrix}")
    sums = np.zeros(d.shape[1])
    for i in range(d.shape[0]):
        row = equailt_matrix[i]
        print(f"row_{i}: {row}")
        sums[i] = intravector_sum(row)
    print(f"sums:\n{sums}")
    return fhe_max(sums)

    
