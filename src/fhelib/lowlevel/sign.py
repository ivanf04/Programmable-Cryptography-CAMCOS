import numpy as np
from fhelib.lowlevel.realify import realify
from fhelib.lowlevel.sigmoid import sigmoid
from fhelib.lowlevel.tanh import tanh
from fhelib import Ciphertext
from fhelib.primitives import add, multiply
from fhelib.auxiliary.reciprocal_univ_guess import (
    reciprocal_newton_universal_guess,
    reciprocal_partial_sums_geometric,
)


def sign(x: Ciphertext, k=10.0, power=1, tol=1e-6) -> Ciphertext:
    """
    sigmoid based approximation for the sign function
    Returns ciphertext of 0 if x_i is <= 0 or 1 if x_i > 0

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
            0 if x_i is <= 0 or 1 if x_i > 0
    """
    x = realify(x)
    # s = reciprocal_newton_universal_guess(sigmoid(x), assumed_range=(0, 1000))
    result = sigmoid(x)
    for _ in range(power - 1):
        result = multiply(result, s)
    return result


def sign_sigmoid_geo_recip(x: Ciphertext, k=10.0, power=1, tol=1e-6) -> Ciphertext:
    """
    Assumes values within for geometric series convergence

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
    x = realify(x)
    sig_x = sigmoid(x)
    s = reciprocal_partial_sums_geometric(sig_x)
    result = sigmoid(x)
    for _ in range(power - 1):
        result = multiply(result, s)
    return result


"""
Sign function as described in the "Spring 2026" hackmd
"""


# def sign_half_equality(x: Ciphertext, k=10.0, tol=0.25) -> Ciphertext:
#     # print(f"intial CT:\n{x}")
#     # s = (1.0 + np.exp(-k * x))
#     s = sigmoid(x)
#     return reciprocal_newton_universal_guess(s, assumed_range=(0, 1000))


def sign_heaviside(x: Ciphertext, a, b, c, power=10) -> Ciphertext:
    """
    Approximates the piecewise function: a if x <= c, b if x > c.

    Computes a + (b - a) * H(x - c), where H is approximated by `sign`
    (sigmoid-based). As power increases the transition at x = c sharpens.

    :param x:     Encrypted input values.
    :param a:     Output value (or ciphertext) when x <= c.
    :param b:     Output value (or ciphertext) when x > c.
    :param c:     Threshold — transition point between a and b.
    :param power: Steepness of the sigmoid used in `sign`; higher = sharper.
    :return:      Ciphertext approximating the step from a to b at x = c.

    TODO: Make FHE-legal so primitive operation counts are accurate.
    """
    # b - a
    neg_a = -1 * a
    b_a = b + neg_a

    # add(x , -c)
    neg_c = -1 * c
    x_c = add(x, neg_c)

    # half equality of ( x - c ) 0
    half_equality = sign_half_equality(x_c, k=power)
    b_a_half_eqaul = multiply(b_a, half_equality)
    # a + (b - a) * H(x - c)
    return add(a, b_a_half_eqaul)


def sign_tanh(x: Ciphertext, k: float = 1, n_terms: int = 9) -> Ciphertext:
    """
    Approximates sign(x) using tanh(kx).
    Convergence requires |x| < π/(2k),
    k=1:  |x| < π/2    ≈ 1.571
    k=10: |x| < π/20   ≈ 0.157

    tanh(kx) → +1 for x > 0, -1 for x < 0 as k → ∞.

    :param x:       Encrypted input values.
    :param k:       Steepness — larger k = sharper transition at 0.
    :param n_terms: Terms in the tanh Taylor expansion (max 9).
    :return:        Ciphertext approximating sign(x) slot-wise.
    """
    x = realify(x)

    # scale input by k (int multiply costs no level)
    kx = (int(k) * x) if float(k).is_integer() else multiply(x, k)
    tanh_kx = tanh(kx, n_terms=n_terms)

    return tanh_kx


def sign_heaviside_tanh(x: Ciphertext, k: float = 1, n_terms: int = 9) -> Ciphertext:
    """
    Approximates sign(x) using tanh(kx).

    tanh(kx) → +1 for x > 0, 0 for x < 0 as k → ∞.
    Sign_heaviside, values remapped to {0, 1}.

    :param x:       Encrypted input values.
    :param k:       Steepness — larger k = sharper transition at 0.
    :param n_terms: Terms in the tanh Taylor expansion (max 9).
    :return:        Ciphertext approximating sign(x) slot-wise.
    """
    x = realify(x)

    # scale input by k (int multiply costs no level)
    kx = (int(k) * x) if float(k).is_integer() else multiply(x, k)
    tanh_kx = tanh(kx, n_terms=n_terms)
    tanh_kx_plus_one = add(tanh_kx, 1)

    # (tanh(kx) + 1) / 2
    sign_approx = multiply(tanh_kx_plus_one, 0.5)

    return sign_approx
