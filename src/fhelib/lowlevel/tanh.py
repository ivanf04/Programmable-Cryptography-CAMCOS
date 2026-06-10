"""
FHE legal tanh approximation using the Taylor series expansion:

  (tanh(x) + 1) / 2

Only odd powers appear. Coefficients are the Bernoulli-number-derived
rational constants from the tanh Maclaurin series.
"""

import numpy as np
from fractions import Fraction
from fhelib.primitives import add, multiply
from fhelib.lowlevel.power import raise_to_power
from fhelib import Ciphertext


# Tanh Taylor coefficients: (degree, numerator, denominator)
# Note: missing the initial constant term of 0.5, it is added upon construction of the entire (degree, ct) list of tuples
TANH_COEFFICIENTS = [
    (1, 1, 2),
    (3, -1, 6),
    (5, 1, 15),
    (7, -17, 630),
    (9, 31, 2835),
    (11, -691, 155925),
    (13, 10922, 6081075),
    (15, -929569, 1277025750),
    (17, 3202291, 10854718875),
]


def tanh_coefficients(ct_length: int) -> list[tuple[int, Ciphertext]]:
    """
    Broadcast each tanh Taylor coefficient into a constant Ciphertext.

    :param ct_length: Length of each output Ciphertext (must be a power of 2).
    :return: List of (degree, Ciphertext) pairs for each term.
    """

    
    result = []
    result.append((0, Ciphertext(ct_length, 0.5))) #constant value ct with 0.5 for the first value of the expansion 
    print(f'Result: {result}')
    for degree, num, den in TANH_COEFFICIENTS:
        scalar = num / den
        ct = Ciphertext(ct_length)
        ct[:] = scalar
        result.append((degree, ct))
    return result


def tanh(x: Ciphertext, n_terms: int = 9, k: int=1) -> Ciphertext:
    """
    Approximate tanh(x) using the first n_terms of its Taylor expansion.

    :param x:       Encrypted input values.
    :param n_terms: Number of terms to include (max 9, matching the formula).
    :return:        Ciphertext approximating tanh(x) slot-wise.
    """
    if n_terms < 1 or n_terms > len(TANH_COEFFICIENTS):
        raise ValueError(f"n_terms must be between 1 and {len(TANH_COEFFICIENTS)}")

    coeffs = tanh_coefficients(x.size)[:n_terms]

    # create Ciphertext with value k to scale input 
    ck = Ciphertext(x.size)
    ck[:] = k
    x = multiply(x, ck)

    # compute each term: c_k * x^degree
    terms = []
    _, constant_ct = coeffs[0]
    terms.append(constant_ct)   #append the x^0 term
    for degree, c_ct in coeffs[1:]:     #skip the first element since you cannot raise to power 0
        x_pow = raise_to_power(x, degree)
        term = multiply(c_ct, x_pow)
        terms.append(term)

    # sum all terms
    result = terms[0]
    for i in range(1, len(terms)):
        result = add(result, terms[i])

    return result
