import numpy as np
from fhelib.auxiliary.difference import difference
from fhelib import Ciphertext

"""
Testing of difference.py
"""

n = 2 ** 15
odds = Ciphertext(n)
evens = Ciphertext(n)

for i in range(n):
    odds.set_element(i, i * 2 + 1)
    evens.set_element(i, i * 2)

print(odds, "\n", evens)

d = difference(odds,evens)

print(d)
