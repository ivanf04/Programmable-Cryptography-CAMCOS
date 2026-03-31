import numpy as np
from fhelib import Ciphertext
from fhelib.lowlevel.sign import sign, sign_heaviside

"""
test file for the sign function
"""

a = Ciphertext(4)

for i in range(a.size):
    a[i] = i - (a.size / 2)

print(f"CT passed though sign:\n{sign(a)}")
print(f"CT passed though sign_heaviside:\n{sign_heaviside(a, 0, 1, 0)}")

