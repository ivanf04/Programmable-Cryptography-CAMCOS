import numpy as np
from fhelib.auxiliary.difference_matrix import difference_matrix
from fhelib import Ciphertext

"""
Testing of difference_matrix.py
"""

evens = Ciphertext(4)

for i in range(evens.size):
    evens.set_element(i, i * 2)

print(evens)

d = difference_matrix(evens)

print(d)
