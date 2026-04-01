from fhelib import Ciphertext
from fhelib.auxiliary.difference_matrix import difference_matrix
"""
TODO implement Mode in FHE 
Required methods: distance, gif, max, eqaulity
"""

def mode(x: Ciphertext) -> complex:
    # create differnce matrix
    d = difference_matrix(x)
