"""
Tests for sign_tanh — checks output range, steepness, and level consumption.
"""

import math
import numpy as np
from fhelib.ciphertext import Ciphertext
from fhelib.lowlevel.sign import sign_tanh


# ── helpers ───────────────────────────────────────────────────────────────────


def make_ct(values: list, level: int = 15) -> Ciphertext:
    length = len(values)
    ct = Ciphertext(length)
    ct[:] = [complex(v) for v in values]
    ct.set_level(level)
    return ct


def header(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


def show(label, result_ct, expected_signs=None):
    real_vals = np.real(result_ct)
    lvl = result_ct.get_level()
    print(f"  {label}")
    print(f"    output:  {np.round(real_vals, 4)}")
    print(f"    level:   {lvl}")
    if expected_signs is not None:
        checks = []
        for v, e in zip(real_vals, expected_signs):
            if e == 1:
                checks.append("✓" if v > 0 else "✗")
            elif e == -1:
                checks.append("✓" if v < 0 else "✗")
            else:
                checks.append("~")  # near-zero, don't check
        print(f"    signs:   {checks}")


# ── 1. basic sign correctness ─────────────────────────────────────────────────

# ── 1. basic sign correctness — inputs in convergence range ──────────────────

header("1. Basic sign correctness — inputs where |kx| < 1.5  (k=10, |x| < 0.15)")

pos = make_ct([0.05, 0.10, 0.12, 0.15])
neg = make_ct([-0.05, -0.10, -0.12, -0.15])

show(
    "positive inputs [0.05, 0.10, 0.12, 0.15]",
    sign_tanh(pos, k=10),
    expected_signs=[1, 1, 1, 1],
)
show(
    "negative inputs [-0.05,-0.10,-0.12,-0.15]",
    sign_tanh(neg, k=10),
    expected_signs=[-1, -1, -1, -1],
)


# ── 2. mixed inputs in convergence range ─────────────────────────────────────

header("2. Mixed positive and negative  (k=10, |x| < 0.15)")

mixed = make_ct([-0.12, -0.05, 0.05, 0.12])
show(
    "[-0.12, -0.05, 0.05, 0.12]", sign_tanh(mixed, k=10), expected_signs=[-1, -1, 1, 1]
)


# ── 3. near-zero transition region ───────────────────────────────────────────

header("3. Near-zero — transition sharpness (k=1, |kx| well within range)")

near_zero = make_ct([-0.1, -0.01, 0.01, 0.1])
show("k=1  (kx in [-0.1, 0.1])", sign_tanh(near_zero, k=1))
show("k=5  (kx in [-0.5, 0.5])", sign_tanh(near_zero, k=5))
show("k=10 (kx in [-1.0, 1.0])", sign_tanh(near_zero, k=10))
print("  k=10 is near the edge of convergence for |x|=0.1")


# ── 4. steepness sweep — only within convergence range ───────────────────────

header("4. Steepness sweep on x=0.1 — |kx| must stay < ~1.5")

x_small = make_ct([0.1, 0.1, 0.1, 0.1])
for k in [1, 5, 10]:
    result = sign_tanh(x_small, k=k)
    val = round(float(np.real(result)[0]), 5)
    kx = k * 0.1
    ok = "✓ converges" if kx < 1.5 else "✗ diverges"
    print(f"  k={k:<4}  kx={kx:.2f}  sign_tanh(0.1) = {val:<12}  {ok}")


# ── 5. output range ───────────────────────────────────────────────────────────

header("5. Output range — values in convergence zone should be in (-1, 1)")

wide = make_ct([-0.15, -0.10, -0.05, 0.0, 0.05, 0.10, 0.15, 0.0])
result = sign_tanh(wide, k=10)
real_vals = np.real(result)
in_range = all(-1.0 < v < 1.0 for v in real_vals)
print(f"  outputs: {np.round(real_vals, 4)}")
print(f"  all in (-1, 1): {'✓' if in_range else '✗'}")


# ── 6. divergence callout — intentionally outside convergence ─────────────────

header("6. ⚠ Divergence callout — inputs outside safe range (informational only)")

print("  tanh Taylor (9 terms) diverges for |kx| > ~1.5")
print("  these results are EXPECTED to be wrong:\n")

bad_inputs = make_ct([1.0, 2.0, 4.0, 8.0])
for k in [5, 10]:
    result = sign_tanh(bad_inputs, k=k)
    real_vals = np.round(np.real(result), 2)
    print(f"  k={k}  inputs=[1,2,4,8]  kx up to {k*8}  →  {real_vals}")
    print(f"  (values >> 1 confirm divergence — not a bug, Taylor limitation)\n")


# ── 7. level consumption ──────────────────────────────────────────────────────

header("7. Level consumption across n_terms")

print("  max degree = 2*n_terms - 1,  cost = ceil(log2(degree)) levels")
print("  int k costs 0 levels, float k costs 1 level\n")

for n in [1, 3, 5, 7, 9]:
    ct = make_ct([0.1, 0.1, 0.1, 0.1], level=15)
    max_degree = 2 * n - 1
    r_int = sign_tanh(ct, k=10, n_terms=n)
    r_float = sign_tanh(ct, k=10.5, n_terms=n)
    expected_cost = math.ceil(math.log2(max_degree)) if max_degree > 1 else 0
    print(
        f"  n_terms={n}  degree=x^{max_degree:<2}  expected cost={expected_cost}  "
        f"int k → level {r_int.get_level()}   float k → level {r_float.get_level()}"
    )
