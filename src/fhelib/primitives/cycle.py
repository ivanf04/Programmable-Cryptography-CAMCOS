""""
Implemetation of cycle using np.roll

if(k>0) elements move right
if(k<0) elements move left

See documentation for examples:
https://numpy.org/doc/stable/reference/generated/numpy.roll.html
"""
from fhelib import Ciphertext
import numpy as np

def cycle(ct: Ciphertext, k: int):
    return np.roll(ct, k)