from fhelib.lowlevel.sign import sign_heaviside
from fhelib.auxiliary.reciprocal_univ_guess import reciprocal_newton_universal_guess
from fhelib import Ciphertext
import numpy as np
from fhelib.primitives import add, multiply, _counts

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
        # result = result - (1 / 2**n) * np.real(indicator)
        reciprocal_partial_sums = reciprocal_newton_universal_guess(2**n, assumed_range=(1, 2 ** 16))
        result = add(result, multiply(-1, multiply(reciprocal_partial_sums, np.real(indicator))))
        print(_counts)

    return result