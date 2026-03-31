import numpy as np
from fhelib import Ciphertext
from fhelib.lowlevel.sign import sign
"""
test file for the sign function
"""

a = Ciphertext(2 ** 15)

for i in range(a.size):
    a[i] = i - 4

print(f"intial CT:\n{a}")
print(f"CT passed though sign:\n{sign(a)}")

