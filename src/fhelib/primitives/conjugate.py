from fhelib.ciphertext import Ciphertext
import numpy as np
from fhelib.primitives import _counts
"""
Implementation of complex conjugation

for each element in ct x+yj, 
returned ciphertext contains x-yj
"""

def conjugate(a: Ciphertext):
    _counts["conjugate"] += 1
    return np.conjugate(a)