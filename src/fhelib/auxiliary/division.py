import numpy as np
from fhelib.ciphertext import Ciphertext
from fhelib.lowlevel.sign import sign_heaviside

"""
Out-of-spec implementation of division 

using numpy division as a placeholder for higher complexity functions
returns a ciphetext containing ai/bi in each corresponding index

TODO: discuss how to implement polynomial estimation with math theory team.
"""


def division(a: Ciphertext, b: Ciphertext):
    return np.divide(a, b)


def reciprocal_partial_sums_geometric(
    a: Ciphertext, n: int = 10, assumed_range: tuple = None
) -> Ciphertext:
    """
    Approximate 1/z using geometric series Taylor expansion
    1/z = 1 + (z-1) + (z-1)^2 + ... + (z-1)^n
    Only converges if |z-1|<1

    :param a: Ciphertext containing values to take reciprocal of
    :param n: number of terms in Taylor expansion (higher n = more accurate but more multiplications)
    :param assumed_range: optional tuple (lo, hi) of expected value range

    Raises: ValueError if assumed_range is provided and outside interval |z - 1| < 1
    """
    if assumed_range:
        if abs(lo - 1) >= 1 or abs(hi - 1) >= 1:
            raise ValueError(
                f"Assumed range {assumed_range} outside interval |z - 1| <1. Scaling required."
            )
    # each element as u=z-1 for 1 + u + u^2 + ...
    x = np.real(a) - 1

    # initial 1 term for each element
    res = np.ones_like(x)

    # power tracks (z-1)^k, multiplied by x each iteration
    # avoids recomputing from scratch: (z-1)^k = (z-1)^(k-1) * (z-1)
    power = np.ones_like(x)

    for _ in range(1, n + 1):
        power = power * x  # (z-1)^k
        res = res + power  # accumulate sum

    return res


def reciprocal_newton_universal_guess(
    a: Ciphertext, n: int = 10, assumed_range: tuple = None, x0: float = None
) -> Ciphertext:
    """
    Approximates 1/z using Newton's method
    Converges quadratically — digits of accuracy double each step.
    Converges for all elements if the initial guess x0 is within (0, 2/z),
    where z is the maximum underlying plaintext value in the input ciphertext a.
    If assumed range (a,b) is provided then x0 can be 1/sqrt(a*b)

    Interative guess update formula:
        x_{n+1} = 2*x_n - x_n^2 * z

    Initial guess options (from hackmd):
    1. any x0 initial guess that's within (0, 2/z)
    2. if assumed_range (a,b) provided then the geometric mean: 1/sqrt(a*b)

    Args:
        a: input Ciphertext (z values we want 1/z of)
        n: number of iterations (digits of accuracy double each step)
        assumed_range: (min, max) of input values → computes x0 = 1/sqrt(min*max)
        x0: explicit initial guess

    Raises:
        ValueError: if neither x0 nor assumed_range provided
    """
    if x0 is None and assumed_range is None:
        raise ValueError("Either x0  or assumed_range required. ")

    if x0 is None:
        lo, hi = assumed_range
        # geometric mean initial guess
        x0 = 1.0 / np.sqrt(lo * hi)

    z = np.real(a)

    # initialize guess for every element
    x = np.full_like(z, x0)

    # Newton iterations: x_{n+1} = 2*x_n - x_n^2 * z
    for _ in range(n):
        x = 2 * x - (x**2) * z

    return x


def adaptive_guess(ct: Ciphertext, b: int = 16) -> Ciphertext:
    """
    Returns the largest power of 2 smaller than x
    Used for Newton's method for reciprocal
    Returns 1/2^n where 2^n < z < 2^(n+1) for each element.

    Uses sign indicators to simulate branching without branching:
        result = 1 - (1/2)(x>2) - (1/4)(x>4) - ... - (1/2^b)(x>2^b)

    Assumes all plaintext values are within [1, 2^b]
    May need tweaks for values < 1

    Args:
        ct: input Ciphertext
        b: bound, assumes all values in [1, 2^b]
    """
    # Each element starts with 1
    result = np.ones_like(ct)

    for n in range(1, b):
        # (x > 2^n) using sign_heaviside with a=0, b=1, c=2^n
        indicator = sign_heaviside(ct, a=0, b=1, c=2**n)

        # Subtracts 1/2^n from 1 for every power of 2 x exceeds
        result = result - (1 / 2**n) * np.real(indicator)

    return result
