from fhelib import Ciphertext
from fhelib.lowlevel.sign import sign_tanh
from fhelib.primitives.multiply import multiply
import numpy as np

def fhe_equality(ct: Ciphertext, a: float, epsilon: float = 0.01) -> Ciphertext:
    """
    Approximates (x == a) componentwise up to error epsilon.
    Uses tanh-based sign approximation.

    Returns: a 0-1 vector where 1 means the element is within epsilon of a
    """

    k = 100.0 / epsilon  # scale k to epsilon size
    lower = sign_tanh(ct - (a - epsilon), k=k)   # x >= a - epsilon
    upper = sign_tanh((a + epsilon) - ct, k=k)   # x <= a + epsilon
    
    return multiply(lower, upper)