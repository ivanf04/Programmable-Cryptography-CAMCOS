import numpy as np
from fhelib import Ciphertext
from fhelib.lowlevel.realify import realify

"""
Test file for the realify function
"""

a = Ciphertext(16)

for i in range(a.size):
    a[i] = i + 1j

print(a)
b =realify(a)
print(b)
