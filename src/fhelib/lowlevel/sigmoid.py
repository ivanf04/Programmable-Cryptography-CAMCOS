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
from fhelib.lowlevel.power import raise_to_power
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
        ct[:] = scalar  # broadcast scalar into every slot
        coefficients.append(ct)
    return coefficients


def exp_x(x: Ciphertext, n: int) -> list[Ciphertext]:
    """
    Compute the encrypted powers of x up to degree n for use in the e^{-x} Taylor expansion.

    Returns a list of n+1 Ciphertexts where the k-th element is x^k:
      [x^0, x^1, x^2, ..., x^n]  =  [1, x, x^2, ..., x^n]

    x^0 is the constant Ciphertext with every slot set to 1.
    x^1 is a copy of the input x.
    x^k for k >= 2 is computed via repeated multiplication using raise_to_power.

    :param x: Encrypted input values.
    :param n: Highest power to compute (inclusive); produces n+1 terms.
    :return:  List of n+1 Ciphertexts [x^0, x^1, ..., x^n].
    """
    length = x.size
    powers: list[Ciphertext] = []

    ct_0 = Ciphertext(length)
    ct_0[:] = 1
    powers.append(ct_0)  # x^0 = 1

    powers.append(x.copy())  # append x^{1} to the list (no multiplication needed)

    for k in range(2, n + 1):
        powers.append(raise_to_power(x, k))  # append x^{k} to the list
    return powers


def exp_expansion(x: Ciphertext, n: int) -> Ciphertext:
    """
    Approximate e^{-x} using a degree-n Taylor expansion evaluated over encrypted values.

    Combines the outputs of exp_neg_coefficients and exp_x by multiplying each
    coefficient c_k by its corresponding power x^k, then summing all n+1 terms:

      e^{-x} ≈ c_0*x^0 + c_1*x^1 + ... + c_n*x^n
             =  1  -  x  +  x^2/2!  -  x^3/3!  + ...

    :param x: Encrypted input values.
    :param n: Degree of the Taylor expansion (inclusive); uses n+1 terms.
    :return:  Single Ciphertext approximating e^{-x} slot-wise.
    """
    coefficients = exp_neg_coefficients(n, x.size)
    x_k = exp_x(x, n)

    ct_temps: list[Ciphertext] = []
    for i in range(n + 1):
        ct = multiply(coefficients[i], x_k[i])
        ct_temps.append(ct)

    result = ct_temps[0]
    for j in range(1, n + 1):
        result = add(result, ct_temps[j])
    return result


# Step 1: create the constant coefficients of the u expansion in plaintext then encrypt
#   → done by exp_neg_coefficients above
# Step 2: calculate x^k where k goes up to n (the degree of the e^{-x} expansion)
#   -> done by exp_x
# Step 3: multiply each x^k by its coefficient and accumulate the sum → gives u = e^{-x} approx
#   -> done by exp_expansion above
# Step 4: use the geometric series  1/(1-u) = 1 + u + u^2 + … + u^m  to approximate sigmoid


def sigmoid(x: Ciphertext, n: int = 5, m: int = 5) -> Ciphertext:
    """
    Approximate sigmoid(x) = 1 / (1 + e^{-x}) over encrypted values using two
    nested polynomial approximations.

    Step 1 — approximate e^{-x} via degree-n Taylor expansion (exp_expansion):
      u ≈ 1 - x + x^2/2! - x^3/3! + ...  (u is close to e^{-x})

    Step 2 — rewrite sigmoid using the geometric series identity:
      1 / (1 + e^{-x}) = 1 / (1 - (-u))
                       ≈ 1 + (-u) + (-u)^2 + ... + (-u)^m

    The result is the degree-m partial sum of that geometric series evaluated
    at -u, giving a fully FHE-legal polynomial approximation of sigmoid(x).

    :param x: Encrypted input values.
    :param n: Number of terms in the e^{-x} Taylor expansion (degree of u).
    :param m: Number of terms in the geometric series expansion of 1/(1+e^{-x}).
    :return:  Ciphertext approximating sigmoid(x) slot-wise.
    """
    # approximate e^{-x} via Taylor expansion: u ≈ e^{-x}
    u = exp_expansion(x, n)

    # negate u to get r = -u = -e^{-x}, the ratio of the geometric series
    neg_1 = Ciphertext(x.size)
    neg_1[:] = -1
    neg_u = multiply(u, neg_1)

    # build the m powers of r: [r^0, r^1, ..., r^m]
    u_powers: list[Ciphertext] = []

    u_0 = Ciphertext(x.size)
    u_0[:] = 1
    u_powers.append(u_0)  # r^0 = 1

    u_powers.append(neg_u)  # r^1 = -u

    for i in range(2, m + 1):  # r^2 through r^m
        u_powers.append(raise_to_power(neg_u, i))

    # sum the geometric series: 1 + r + r^2 + ... + r^m ≈ 1/(1-r) = sigmoid(x)
    u_sum = u_powers[0]
    for j in range(1, m + 1):
        u_sum = add(u_sum, u_powers[j])

    return u_sum


def 