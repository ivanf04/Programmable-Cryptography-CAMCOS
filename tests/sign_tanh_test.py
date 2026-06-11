"""
Tests the binary sign approximation using tanh:

  sign_(0,1,a)(x) = (tanh(k * (x - a)) + 1) / 2

Maps x > a → close to 1, x < a → close to 0.

Sweeps threshold a from -1.5 to 1.5 with x fixed at 0.
Shows FHE output vs numpy reference and distance from the ideal binary target.
"""

import numpy as np
from fhelib import Ciphertext
from fhelib.primitives import add, multiply
from fhelib.lowlevel.tanh import tanh

CT_SIZE = 4
X_VAL = 0.0
K = 1
N_TERMS = 9  # default

x_ct = Ciphertext(CT_SIZE, X_VAL)

thresholds = np.arange(-1.5, 1.6, 0.5)  # -1.5, -1.0, ..., 1.5

print("=" * 75)
print(f"sign_(0,1,a)(x) = (tanh(k*(x-a)) + 1) / 2   k={K}, n_terms={N_TERMS}")
print(f"Input x = {X_VAL}  |  threshold a sweeps -1.5 → 1.5")
print("=" * 75)
print(f"{'a':>6}  {'target':>7}  {'FHE':>10}  {'np ref':>10}  {'|FHE - target|':>15}  {'|ref - target|':>15}")
print("-" * 75)

for a in thresholds:
    # (tanh(k*(x - a)) + 1) / 2  in FHE
    x_minus_a = add(x_ct, -float(a))
    tanh_out = tanh(x_minus_a, n_terms=N_TERMS, k=K)
    heaviside = multiply(add(tanh_out, 1.0), 0.5)

    fhe_val = float(np.real(heaviside[0]))
    ref_val = float((np.tanh(K * (X_VAL - a)) + 1) / 2)
    target = 1.0 if X_VAL > a else 0.0

    fhe_err = abs(fhe_val - target)
    ref_err = abs(ref_val - target)

    label = "x > a → 1" if target == 1.0 else "x ≤ a → 0"
    print(f"{a:>6.2f}  {target:>7.1f}  {fhe_val:>10.5f}  {ref_val:>10.5f}  {fhe_err:>15.2e}  {ref_err:>15.2e}  ({label})")

print()
print("FHE error: distance from ideal binary output (0 or 1)")
print("ref error: how far numpy tanh is from binary — sets the ceiling on FHE accuracy")
