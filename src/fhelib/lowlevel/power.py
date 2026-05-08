"""
FHe legal power function
"""

from fhelib import Ciphertext
from fhelib.primitives import multiply


def raise_to_power(x: Ciphertext, a: int) -> Ciphertext:
    """
    Raises every element of a ciphertext to the power a, x^a
    Uses repeated squaring for optimal level consumption: ceil(log2(a)) levels

    :param x: Ciphertext to be raised to power a
    :param a: integer to raise x to power a
    """
    if a < 1:
        raise ValueError("Power must be a positive integer")
    if a == 1:
        return x.copy()

    result = None
    base = Ciphertext(x.copy())
    

    while a > 0:
        if a % 2 == 1:  # if current term is odd
            result = base if result is None else multiply(result, base)
        base = multiply(base, base)  # square the base
        a //= 2  # move to next term

    return result
