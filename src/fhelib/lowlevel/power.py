"""
FHe legal power function  
"""

from fhelib import Ciphertext
from fhelib.primitives import multiply

def rasie_to_power(x: Ciphertext, a: int) -> Ciphertext:
    """
    Rasies every element of a ciphetext to the power a, x^a

    :param x: Ciphertext to be raised to power a
    :param a: integer to raise x to power a 
    """
    result = x.copy()
    for _ in range(a - 1):
        result = multiply(result, x)
    return result