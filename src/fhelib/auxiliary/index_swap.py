from fhelib import Ciphertext
from fhelib.primitives.cycle import cycle
from fhelib.primitives.multiply import multiply
import numpy as np

def index_swap(v: Ciphertext, i: int, j: int) -> Ciphertext:
    """
    Swaps elements at indices i and j in ciphertext vector v.
    i should be the lesser index.
    """
    k = len(v)

    # c1: 1s everywhere except positions i and j
    c1 = np.ones(k, dtype=complex)
    c1[i] = 0
    c1[j] = 0

    # c2: 1 only at position i
    c2 = np.zeros(k, dtype=complex)
    c2[i] = 1

    # c3: 1 only at position j
    c3 = np.zeros(k, dtype=complex)
    c3[j] = 1

    p1 = multiply(v, c1)  # original with i,j zeroed out
    p2 = multiply(v, c2)  # only a_i
    p3 = multiply(v, c3)  # only b_j

    # cycle p2 forward to position j, p3 back to position i
    p2_prime = cycle(p2, j - i)
    p3_prime = cycle(p3, -(j - i))

    return p1 + p2_prime + p3_prime