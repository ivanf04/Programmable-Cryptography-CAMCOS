from fhelib import Ciphertext
from fhelib.lowlevel.sum import intravector_sum
from fhelib.auxiliary.exponentiate import exponentiate
from fhelib.auxiliary.division import division
import numpy as np

def softmax(ct: Ciphertext) -> Ciphertext:
    """
    Approximates softmax using plaintext exp and division.
    asmpt: assumes exp and division are available (both WIP in FHE)
    """
    # exponentiate each element
    x_prime = exponentiate(ct)

    # sum all
    s = intravector_sum(x_prime)

    # needs to be replaced with FHE division
    return np.divide(x_prime, s)