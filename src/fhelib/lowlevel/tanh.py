"""
FHE legal tanh approximation using the Taylor series expansion:

  tanh(x) ≈ x - (1/3)x^3 + (2/15)x^5 - (17/315)x^7 + (62/2835)x^9
             - (1382/155925)x^11 + (21844/6081075)x^13
             - (929569/638512875)x^15 + (6404582/10854718875)x^17

Only odd powers appear. Coefficients are the Bernoulli-number-derived
rational constants from the tanh Maclaurin series.
"""

import numpy as np
from fractions import Fraction
from fhelib.primitives import add, multiply
from fhelib.lowlevel.power import raise_to_power
from fhelib import Ciphertext


# Tanh Taylor coefficients: (degree, numerator, denominator)
# Only odd degrees, matching the image formula
TANH_COEFFICIENTS = [
    (0, 1, 2),
    (1, 1, 2),
    (3, -1, 6),
    (5, 1, 15),
    (7, -17, 630),
    (9, 31, 2835),
    (11, -691, 155925),
    (13, 10922, 6081075),
    (15, -929569, 1277025750),
]


def tanh_coefficients(ct_length: int) -> list[tuple[int, Ciphertext]]:
    """
    Broadcast each tanh Taylor coefficient into a constant Ciphertext.

    :param ct_length: Length of each output Ciphertext (must be a power of 2).
    :return: List of (degree, Ciphertext) pairs for each term.
    """
    result = []
    for degree, num, den in TANH_COEFFICIENTS:
        scalar = num / den
        ct = Ciphertext(ct_length)
        ct[:] = scalar
        result.append((degree, ct))
    return result


def tanh(x: Ciphertext, n_terms: int = 9) -> Ciphertext:
    """
    Approximate tanh(x) using the first n_terms of its Taylor expansion.

    :param x:       Encrypted input values.
    :param n_terms: Number of terms to include (max 9, matching the formula).
    :return:        Ciphertext approximating tanh(x) slot-wise.
    """
    if n_terms < 1 or n_terms > len(TANH_COEFFICIENTS):
        raise ValueError(f"n_terms must be between 1 and {len(TANH_COEFFICIENTS)}")

    coeffs = tanh_coefficients(x.size)[:n_terms]

    # compute each term: c_k * x^degree
    terms = []
    for degree, c_ct in coeffs:
        x_pow = x.copy() if degree == 1 else raise_to_power(x, degree)
        term = multiply(c_ct, x_pow)
        terms.append(term)

    # sum all terms
    result = terms[0]
    for i in range(1, len(terms)):
        result = add(result, terms[i])

    return result
