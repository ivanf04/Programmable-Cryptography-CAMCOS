"""
FHE legal approximation of the exponential function 
"""
import numpy as np
from fhelib import Ciphertext
from fhelib.primitives import add, multiply
from fhelib.lowlevel import factorial, rasie_to_power
from fhelib.auxiliary.reciprocal_univ_guess import reciprocal_partial_sums_geometric

def exponential(x: Ciphertext, n: int) -> Ciphertext:
    """
    Approximant e^x using taylor series expansion, 
    using geometric series approximation for the reciprocal of n!

    :param n: the number of summation terms in the taylor expansion
    """
    # factorials = factorial(n)
    # reciprocal_factorial = reciprocal_partial_sums_geometric(factorials)
    b = np.ones_like(x)
    b = add(b, x)
    for i in range(2, n + 1):
        x_raised = rasie_to_power(x, i)
        reciprocal_factorial_term = reciprocal_partial_sums_geometric(factorial(i))
        b = add(b, multiply(x_raised, reciprocal_factorial_term))
    return b
