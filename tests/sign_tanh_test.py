"""
Test for tanh implementation of the sign function as described in Spring 26 CAMCOS Hackmd.

sign_tanh computes (tanh(kx) + 1) / 2, mapping:
  x << 0  →  ≈ 0
  x  = 0  →  = 0.5
  x >> 0  →  ≈ 1

NOTE: the 9-term Taylor tanh diverges for |kx| > ~1.5.
  inputs [-4, -2, 0, 1] with large k will diverge — use small k or small inputs.
"""

import numpy as np
from fhelib import Ciphertext
from fhelib.lowlevel.sign import sign_tanh

INPUT_VALUES = [-4, -2, 0, 1]
EXPECTED = [0, 0, 0.5, 1]

# ── build ciphertext ──────────────────────────────────────────────────────────

a = Ciphertext(len(INPUT_VALUES))
for i, v in enumerate(INPUT_VALUES):
    a[i] = v

# ── test 1: small k so kx stays in convergence range ─────────────────────────

print("=" * 55)
print("sign_tanh test — input: [-4, -2, 0, 1]")
print("=" * 55)
print(f"Input:    {INPUT_VALUES}")
print(f"Expected: {EXPECTED}")
print()

for k in [0.1, 0.3, 1.0]:
    result = sign_tanh(a, k=k)
    real_vals = np.round(np.real(np.array(result)), 4)
    kx_max = k * max(abs(v) for v in INPUT_VALUES)
    converges = "converges" if kx_max < 1.5 else "may diverge"
    print(f"  k={k:<4}  max|kx|={kx_max:.2f}  ({converges})")
    print(f"    output:   {real_vals}")
    print(f"    expected: {EXPECTED}")
    print()

# ── test 2: plaintext reference ───────────────────────────────────────────────

print("=" * 55)
print("Plaintext reference: (tanh(kx) + 1) / 2")
print("=" * 55)
x_arr = np.array(INPUT_VALUES, dtype=float)
for k in [0.1, 0.3, 1.0]:
    ref = (np.tanh(k * x_arr) + 1) / 2
    print(f"  k={k:<4}  ref: {np.round(ref, 4)}")
