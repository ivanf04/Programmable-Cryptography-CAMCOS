import numpy as np
from fhelib.lowlevel import realify, sigmoid
from fhelib import Ciphertext
from fhelib.primitives import add, multiply
from fhelib.auxiliary.reciprocal_univ_guess import (
    reciprocal_newton_universal_guess,
    reciprocal_partial_sums_geometric,
)

from fhelib.lowlevel.tanh import tanh

"""
Returns 0 if x_i is <= 0 or 1 if x_i > 0
"""

"""
sigmoid based approximation for the sign function 
@param 
    x: Ciphertext
        Input Ciphertext
    k: float
        Sigmoid steepness (larger = sharper transition toward 0).
    power: int or float
        Raise sigmoid to this power to sharpen the curve
    tol: float
        Values <= tol become 0, else become 1
@return
    out: Ciphertext
        Output with 1's and 0's 
"""


def sign(x: Ciphertext, k=10.0, power=8, tol=1e-6) -> Ciphertext:
    x = realify(x)
    s = reciprocal_newton_universal_guess(sigmoid(x), assumed_range=(0, 1000))
    result = s
    for _ in range(power - 1):
        result = multiply(result, s)
    return result


"""
Sign function as described in the "Spring 2026" hackmd
"""


def sign_half_equality(x: Ciphertext, k=10.0, tol=0.25) -> Ciphertext:
    # print(f"intial CT:\n{x}")
    # s = (1.0 + np.exp(-k * x))
    s = sigmoid(x)
    return reciprocal_newton_universal_guess(s, assumed_range=(0, 1000))


"""
Use the original sign method to create a heaviside-type function
see "CAMCOS 2026 Spring" hackmd for details 
TODO: Make FHE legal so we can count primitive operations
"""


def sign_heaviside(x: Ciphertext, a, b, c, power=10) -> Ciphertext:
    b_a = add(b, multiply(-1, a))
    half_equality = sign_half_equality(add(x, multiply(-1, c)), k=power)
    b_a_half_eqaul = multiply(b_a, half_equality)
    return add(a, b_a_half_eqaul)


def sign_tanh(x: Ciphertext, k: float = 10.0, n_terms: int = 9) -> Ciphertext:
    """
    Approximates sign(x) using tanh(kx).

    tanh(kx) → +1 for x > 0, -1 for x < 0 as k → ∞.
    Returns values in (-1, 1) rather than {0, 1} — use sign_heaviside
    to remap to {0, 1} if needed.

    :param x:       Encrypted input values.
    :param k:       Steepness — larger k = sharper transition at 0.
    :param n_terms: Terms in the tanh Taylor expansion (max 9).
    :return:        Ciphertext approximating sign(x) slot-wise.
    """
    x = realify(x)

    # scale input by k (int multiply costs no level)
    kx = multiply(int(k), x) if float(k).is_integer() else multiply(k, x)

    return tanh(kx, n_terms=n_terms)
