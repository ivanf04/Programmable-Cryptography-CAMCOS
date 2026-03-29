from fhelib import Ciphertext
from fhelib.algorithms.sum import intravector_sum
from fhelib.primitives.conjugate import conjugate
import numpy as np

def dot_product(ct1: Ciphertext, ct2: Ciphertext):
    return intravector_sum( np.multiply(ct1, ct2) )

def complex_inner_product(ct1: Ciphertext, ct2: Ciphertext):
    return intravector_sum( np.multiply(ct1, conjugate(ct2) ) )
