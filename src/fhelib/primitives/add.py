import numpy as np
from fhelib.ciphertext import Ciphertext
from fhelib.primitives import _counts
"""
Basic component wise addition of two cypher texts
using np.add
"""

def add(a: Ciphertext, b: Ciphertext):
    _counts["add"] += 1
    return np.add(a,b)