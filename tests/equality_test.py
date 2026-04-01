from fhelib.ciphertext import Ciphertext
from fhelib.auxiliary.equality import fhe_equality
from fhelib.lowlevel.sign import sign
import numpy as np

"""
Note: exact boundary values (x = a +/- epsilon) are unreliable
per hackmd: "it is advised to avoid being dependent on the true equality case"
test values are chosen to be clearly inside or outside the epsilon range
"""

v = Ciphertext(8)
values = [0, 0.005, 0.02, 1.0, -0.008, 0.5, 0.015, 0.0]
for idx, val in enumerate(values):
    v.set_element(idx, val)

print("=" * 50)
print("Equality Test: (x == 0) with epsilon=0.01")
print("Note: boundary values (exactly +/- epsilon) avoided")
print("=" * 50)
print(f"Input v:  {values}")
result = fhe_equality(v, 0, epsilon=0.01)
print(f"Result:   {result}")
print(f"Expected: [1, 1, 0, 0, 1, 0, 0, 1]")

print()
print("=" * 50)
print("Equality Test: (x == 1) with epsilon=0.1")
print("Note: boundary values (exactly +/- epsilon) avoided")
print("=" * 50)
values2 = [1.0, 1.05, 0.95, 1.15, 0.85, 0.0, 2.0, 1.0]
v2 = Ciphertext(8)
for idx, val in enumerate(values2):
    v2.set_element(idx, val)

print(f"Input v:  {values2}")
result2 = fhe_equality(v2, 1.0, epsilon=0.1)
print(f"Result:   {result2}")
print(f"Expected: [1, 1, 1, 0, 0, 0, 0, 1]")