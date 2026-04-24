import numpy as np
from fhelib.ciphertext import Ciphertext
from fhelib.primitives import add, multiply, _counts, reset

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
    1/z = 1 + (1-z) + (1-z)^2 + ... + (1-z)^n
    Only converges if |z-1|<1

    :param a: Ciphertext containing values to take reciprocal of
    :param n: number of terms in Taylor expansion (higher n = more accurate but more multiplications)
    :param assumed_range: optional tuple (lo, hi) of expected value range

    Raises: ValueError if assumed_range is provided and outside interval |z - 1| < 1
    """

    if assumed_range:
        lo, hi = assumed_range
        if abs(lo - 1) >= 1 or abs(hi - 1) >= 1:
            raise ValueError(
                f"Assumed range {assumed_range} outside interval |z - 1| <1. Scaling required."
            )
    # each element as u= 1-z for 1 + u + u^2 + ...
    x = 1 - np.real(a)
    # negative_1 = multiply(np.ones_like(x), -1)

    # initial 1 term for each element
    res = np.ones_like(x)

    # power tracks (1-z)^k, multiplied by x each iteration
    # avoids recomputing from scratch: (1-z)^k = (1-z)^(k-1) * (1-z)
    power = np.ones_like(x)

    for _ in range(1, n + 1):
        power = multiply(power, x)  # (1-z)^k
        res = add(res, power)  # accumulate sum
        # print(_counts)
        # reset()

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
        x_n = multiply(2, x)  # 2*x_n
        x_2 = multiply(x, x)  # x_n^2
        x_2_z = multiply(x_2, z)  # x_n^2 * z
        negative_x_2_z = multiply(-1, x_2_z)  # -(x_n^2 * z)
        x = add(x_n, negative_x_2_z)  # 2*x_n - x_n^2 * z
        # print(_counts)
        # reset()

    return x
