from fhelib import Ciphertext
from fhelib.stats.mode import mode
"""
Test file for mode.py
"""
values = [2, 2, 1, -2]
a = Ciphertext(len(values))
for idx, val in enumerate(values):
    a.set_element(idx, val)

print("=" * 50)
print(f"Mode test on {values}")
print("Expected output: 2+0j")
print("=" * 50)

result = mode(a)
print(f"Result: {result}")
