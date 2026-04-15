from fhelib.ciphertext import Ciphertext
import numpy as np
"""
Implementation of complex conjugation

for each element in ct x+yj, 
returned ciphertext contains x-yj
"""

def conjugate(a: Ciphertext):
    return np.conjugate(a)