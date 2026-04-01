from fhelib.ciphertext import Ciphertext
from fhelib.auxiliary.softmax import softmax

"""
Softmax test file
Note: current implementation uses plaintext exp and division
Both will be replaced with FHE-safe versions once implemented by theory team
Note: Ciphertext size is N=8 for 4 data values (CKKS convention: N/2 usable slots)
      padding slots 4-7 will contain small residual values, only first 4 slots are valid
"""

print("=" * 50)
print("Softmax Test 1: z = (4, 2, 24, 6, 0, 0, 0, 0)")
print("Expected: approx (0, 0, 1, 0, -, -, -, -)")
print("=" * 50)

v = Ciphertext(8)
for idx, val in enumerate([4, 2, 24, 6]):
    v.set_element(idx, val)

print(f"Input:    [4, 2, 24, 6, 0, 0, 0, 0]")
result = softmax(v)
print(f"Result:   {result}")
print(f"Expected: approx [0, 0, 1, 0, -, -, -, -] (first 4 slots valid)")

print()
print("=" * 50)
print("Softmax Test 2: z = (1, 1, 1, 1, 0, 0, 0, 0)")
print("Expected: (0.25, 0.25, 0.25, 0.25, -, -, -, -)")
print("=" * 50)

v2 = Ciphertext(8)
for idx, val in enumerate([1, 1, 1, 1]):
    v2.set_element(idx, val)

print(f"Input:    [1, 1, 1, 1, 0, 0, 0, 0]")
result2 = softmax(v2)
print(f"Result:   {result2}")
print(f"Expected: approx [0.25, 0.25, 0.25, 0.25, -, -, -, -] (first 4 slots valid)")