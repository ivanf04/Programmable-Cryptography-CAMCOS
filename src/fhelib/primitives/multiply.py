import numpy as np
from fhelib.ciphertext import Ciphertext
from fhelib.primitives import _counts
"""
Basic component wise multiplication of two cypher texts
using np.multiply
"""

def multiply(a: Ciphertext, b: Ciphertext):
    _counts["multiply"] += 1
    return np.multiply(a,b)