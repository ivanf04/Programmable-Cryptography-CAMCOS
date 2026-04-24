"""
FHE legal sigmoid approximation, using the geometric series expansion:

  sigmoid(x) = 1 / (1 + e^{-x})
             = 1 / (1 - (-e^{-x}))

The inner approximation is the Taylor series for e^{-x}:

  e^{-x} ≈ sum_{k=0}^{n} (-1)^k / k!  *  x^k
          = 1 - x + x^2/2! - x^3/3! + ...

The plaintext coefficients c_k = (-1)^k / k! are constants — they are
computed in plaintext and broadcast into constant Ciphertexts so that
subsequent FHE operations can scale the encrypted x^k terms.
"""

import math
import numpy as np
from fhelib.primitives import add, multiply
from fhelib import Ciphertext


def exp_neg_coefficients(n: int, ct_length: int) -> list[Ciphertext]:
    """
    Compute the plaintext Taylor coefficients for e^{-x} up to degree n,
    then broadcast each scalar into a constant Ciphertext of length ct_length.

    Coefficient k:  c_k = (-1)^k / k!

    :param n:         Number of terms (inclusive), so degrees 0 … n are produced.
    :param ct_length: Length of each output Ciphertext (must be a power of 2).
    :return:          List of n+1 constant Ciphertexts [c_0, c_1, …, c_n].
    """
    coefficients: list[Ciphertext] = []
    for k in range(n + 1):
        scalar = ((-1) ** k) / math.factorial(k)
        ct = Ciphertext(ct_length)
        ct[:] = scalar          # broadcast scalar into every slot
        coefficients.append(ct)
    return coefficients


# Step 1: create the constant coefficients of the u expansion in plaintext then encrypt
#   → done by exp_neg_coefficients above
# Step 2: calculate x^k where k goes up to n (the degree of the e^{-x} expansion)
# Step 3: multiply each x^k by its coefficient and accumulate the sum → gives u = e^{-x} approx
# Step 4: use the geometric series  1/(1-u) = 1 + u + u^2 + … + u^m  to approximate sigmoid

def sigmoid(x: Ciphertext, n: int = 5, m: int = 5) -> Ciphertext:
    """
    :param x: Encrypted input values.
    :param n: Number of terms in the e^{-x} Taylor expansion.
    :param m: Number of terms in the geometric series for 1/(1+e^{-x}).
    """
