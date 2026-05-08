from fhelib import Ciphertext
from fhelib.stats.mode import mode
"""
Test file for mode.py
"""
values = [-1, 0.5, -1, 1]
a = Ciphertext(len(values))
for idx, val in enumerate(values):
    a.set_element(idx, val)

print("=" * 50)
print(f"Mode test on {values}")
print("Expected output: -1")
print("=" * 50)

result = mode(a)
print(f"Result: {result}")
