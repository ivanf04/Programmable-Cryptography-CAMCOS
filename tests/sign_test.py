import numpy as np
from fhelib import Ciphertext
from fhelib.lowlevel.sign import sign_half_equality, sign_heaviside

"""
test file for the sign function
"""

a = Ciphertext(4)

for i in range(a.size):
    a[i] = i - (a.size / 2)

print('=' * 50)
print('sign with sigmoid approximation test.')
print('=' * 50)
print(f"Input: {a}")
expected = [0, 0, 0.5, 1]
print(f'Expected output(approximate):\n{expected}')
print('=' * 50)
print(f"CT passed though sign:\n{sign_half_equality(a, k=5)}")
print(f"CT passed though sign_heaviside(0, 1, 0):\n{sign_heaviside(a, 0, 1, 0, 5)}")

