import numpy as np
from fhelib.auxiliary.difference_matrix import difference_matrix
from fhelib import Ciphertext

"""
Testing of difference_matrix.py
"""

print("Test of difference_matrix method")
print("=" * 50)
evens = Ciphertext(4)

for i in range(evens.size):
    evens.set_element(i, i * 2)

# print(evens)
print(f"Input Ciphertext of even numbers:\n{evens}")
print("=" * 50)
expected_output = [[0, 2, 4, 6],
                   [-2, 0, 2, 4],
                   [-4, -2, 0, 2],
                   [-6, -4, -2, 0]]
print(f"Expected output for difference matrix:\n{expected_output}")
print("=" * 50)
d = difference_matrix(evens)

print(f"Result:\n{d}")
