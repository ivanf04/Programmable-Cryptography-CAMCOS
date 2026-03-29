import numpy as np
from fhelib.algorithms.difference import difference
from fhelib import Ciphertext

"""
Testing of difference.py
"""

n = 2 ** 15
a = Ciphertext(n)
b = Ciphertext(n)

for i in range(n):
    a.set_element(i, i * 2 + 1)
    b.set_element(i, i * 2)

print(a, "\n", b)

d = difference(a,b)

print(d)
