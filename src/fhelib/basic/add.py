import numpy as np
from fhelib.ciphertext import Ciphertext
"""
Basic component wise addition of two cypher texts
using np.add
"""

def add(a: Ciphertext, b: Ciphertext):
    return np.add(a,b)