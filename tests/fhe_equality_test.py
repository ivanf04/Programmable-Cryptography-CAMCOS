"""
Diagnostic test for fhe_equality — convergence analysis.

fhe_equality(ct, a, epsilon) computes (x == a) componentwise by checking
  lower = sign_tanh(x - (a - epsilon), k=k)   # x >= a - epsilon
  upper = sign_tanh((a + epsilon) - x, k=k)   # x <= a + epsilon
where k = 100 / epsilon.

sign_tanh uses a 9-term Taylor tanh, which converges only for |kx| < ~1.5.
The shifted inputs passed to sign_tanh are of order epsilon at the target,
so k * epsilon = 100 — well outside the convergence radius. This test
locates where the function actually converges and what k range is safe.

Graphs produced:
  1. fhe_equality output vs x for several epsilon values (FHE vs numpy ref)
  2. k * epsilon product vs epsilon — shows why divergence happens
  3. Max |kx| at the boundary vs epsilon — convergence threshold line at 1.5
  4. Safe k values that keep |kx| < 1.5 across the shifted input range
"""

import numpy as np
import matplotlib.pyplot as plt
from fhelib import Ciphertext
from fhelib.auxiliary.equality import fhe_equality

TANH_CONVERGENCE_RADIUS = 1.5   # Taylor series reliable below this

# ── numpy reference: ideal fhe_equality (no Taylor approximation error) ───────

def ref_equality(x: np.ndarray, a: float, epsilon: float, k: float) -> np.ndarray:
    """Exact tanh-based equality using numpy — the ideal the FHE code targets."""
    lower = (np.tanh(k * (x - (a - epsilon))) + 1) / 2
    upper = (np.tanh(k * ((a + epsilon) - x)) + 1) / 2
    return lower * upper


# ── helper: run fhe_equality and extract real parts ───────────────────────────

def run_fhe_equality(x_vals: np.ndarray, a: float, epsilon: float) -> np.ndarray:
    n = len(x_vals)
    ct = Ciphertext(n)
    for i, v in enumerate(x_vals):
        ct[i] = v
    result = fhe_equality(ct, a, epsilon=epsilon)
    return np.real(np.array(result))


# ── Section 1: convergence table ──────────────────────────────────────────────

print("=" * 65)
print("fhe_equality convergence analysis")
print("=" * 65)
print()
print("The root issue: k = 100/epsilon, so k*epsilon = 100 always.")
print(f"Taylor tanh converges for |kx| < {TANH_CONVERGENCE_RADIUS}.")
print("At the target (x=a), the shifted input fed to sign_tanh is epsilon,")
print("so |k * epsilon| = 100 >> 1.5.  The series diverges for all epsilon.")
print()

print(f"{'epsilon':>10}  {'k=100/eps':>12}  {'k*eps (kx at target)':>22}  {'converges?':>12}")
print("-" * 65)
epsilons = [1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001]
for eps in epsilons:
    k = 100.0 / eps
    kx_at_target = k * eps          # = 100 always
    converges = kx_at_target < TANH_CONVERGENCE_RADIUS
    print(f"  {eps:>8}  {k:>12.1f}  {kx_at_target:>22.1f}  {'YES' if converges else 'NO (diverges)':>12}")

print()
print("Conclusion: no epsilon value makes fhe_equality converge with k=100/eps.")
print()

# ── Section 2: what k WOULD make it converge ──────────────────────────────────

print("=" * 65)
print("Safe k values: k < 1.5 / epsilon")
print("=" * 65)
print()
print(f"{'epsilon':>10}  {'k_max (safe)':>14}  {'current k':>12}  {'ratio current/safe':>20}")
print("-" * 62)
for eps in epsilons:
    k_current = 100.0 / eps
    k_safe = TANH_CONVERGENCE_RADIUS / eps
    ratio = k_current / k_safe
    print(f"  {eps:>8}  {k_safe:>14.3f}  {k_current:>12.1f}  {ratio:>20.1f}x too large")

print()

# ── Section 3: sweep x vs fhe_equality for several epsilon values ─────────────

TARGET_A = 0.0
N_SLOTS  = 16   # must be power of 2

print("=" * 65)
print(f"FHE output vs numpy ref — target a={TARGET_A}")
print("=" * 65)

results = {}

for eps in [0.1, 0.01, 0.001]:
    k = 100.0 / eps
    # x range: [-3*eps, 3*eps] centred on target, so shifted values are O(eps)
    x_vals = np.linspace(TARGET_A - 3 * eps, TARGET_A + 3 * eps, N_SLOTS)
    ref = ref_equality(x_vals, TARGET_A, eps, k)
    fhe = run_fhe_equality(x_vals, TARGET_A, eps)
    max_err = np.max(np.abs(fhe - ref))
    print(f"\n  epsilon={eps}  k={k:.1f}  k*eps={k*eps:.1f}")
    print(f"  x range: [{x_vals[0]:.4f}, {x_vals[-1]:.4f}]")
    print(f"  numpy ref: {np.round(ref, 3)}")
    print(f"  FHE output: {np.round(fhe, 3)}")
    print(f"  max |err vs ref|: {max_err:.4f}")
    results[eps] = (x_vals, ref, fhe)

print()

# ── Section 4: find k values that actually converge ───────────────────────────

print("=" * 65)
print("Sweep k directly — find convergence threshold")
print("=" * 65)
print()
print("Fix epsilon=0.1, vary k from safe to unsafe.")
print()

EPS_FIXED = 0.1
x_vals_fixed = np.linspace(TARGET_A - 3 * EPS_FIXED, TARGET_A + 3 * EPS_FIXED, N_SLOTS)
ref_fixed = ref_equality(x_vals_fixed, TARGET_A, EPS_FIXED, k=100.0 / EPS_FIXED)

print(f"{'k':>10}  {'k*eps':>8}  {'converged?':>12}  {'max|err vs ref|':>18}")
print("-" * 55)

k_sweep_results = {}
for k_val in [0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 30.0, 100.0, 1000.0]:
    eps_val = EPS_FIXED
    kx_product = k_val * eps_val
    converged = kx_product < TANH_CONVERGENCE_RADIUS

    # build ciphertext and manually call sign_tanh with this k
    from fhelib.lowlevel.sign import sign_tanh
    from fhelib.primitives.multiply import multiply

    ct = Ciphertext(N_SLOTS)
    for i, v in enumerate(x_vals_fixed):
        ct[i] = v

    lower = sign_tanh(ct - (TARGET_A - eps_val), k=k_val)
    upper = sign_tanh((TARGET_A + eps_val) - ct, k=k_val)
    fhe_out = np.real(np.array(multiply(lower, upper)))

    ref_k = ref_equality(x_vals_fixed, TARGET_A, eps_val, k_val)
    max_err = np.max(np.abs(fhe_out - ref_k))
    print(f"  {k_val:>8}  {kx_product:>8.3f}  {'YES' if converged else 'NO':>12}  {max_err:>18.4f}")
    k_sweep_results[k_val] = (fhe_out, ref_k, kx_product)

print()


# ── Plots ──────────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("fhe_equality convergence analysis", fontsize=14)

# Plot 1: FHE vs ref for 3 epsilon values
ax = axes[0, 0]
colors = ["steelblue", "coral", "seagreen"]
for i, eps in enumerate([0.1, 0.01, 0.001]):
    x_vals, ref, fhe = results[eps]
    ax.plot(x_vals, ref, "--", color=colors[i], lw=1.5, label=f"ref  eps={eps}")
    ax.plot(x_vals, fhe, "-",  color=colors[i], lw=2.0, label=f"FHE  eps={eps}", alpha=0.8)
ax.axhline(0, color="black", lw=0.5, ls=":")
ax.axhline(1, color="black", lw=0.5, ls=":")
ax.set_xlabel("x")
ax.set_ylabel("fhe_equality(x, 0)")
ax.set_title("FHE output vs numpy ref (k=100/eps)")
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

# Plot 2: k * epsilon product — always 100
ax = axes[0, 1]
eps_arr = np.array(epsilons)
k_arr   = 100.0 / eps_arr
kx_arr  = k_arr * eps_arr
ax.axhline(TANH_CONVERGENCE_RADIUS, color="red", lw=2, ls="--",
           label=f"convergence radius = {TANH_CONVERGENCE_RADIUS}")
ax.plot(eps_arr, kx_arr, "o-", color="steelblue", lw=2, ms=8, label="k * epsilon (= 100)")
ax.set_xlabel("epsilon")
ax.set_ylabel("k * epsilon  (|kx| at target)")
ax.set_xscale("log")
ax.set_title("k·ε product vs epsilon\n(constant 100 — always diverges)")
ax.legend()
ax.grid(True, alpha=0.3)

# Plot 3: k sweep — output for safe vs unsafe k values
ax = axes[1, 0]
safe_ks   = [k for k, (_, _, kx) in k_sweep_results.items() if kx < TANH_CONVERGENCE_RADIUS]
unsafe_ks = [k for k, (_, _, kx) in k_sweep_results.items() if kx >= TANH_CONVERGENCE_RADIUS]

for k_val in list(k_sweep_results.keys())[:6]:
    out, ref_k, kx = k_sweep_results[k_val]
    style = "-" if kx < TANH_CONVERGENCE_RADIUS else "--"
    label = f"k={k_val} (kε={kx:.2f}, {'OK' if kx < TANH_CONVERGENCE_RADIUS else 'DIVERGES'})"
    ax.plot(x_vals_fixed, out, style, lw=1.5, label=label)
ax.axhline(0, color="black", lw=0.5, ls=":")
ax.axhline(1, color="black", lw=0.5, ls=":")
ax.set_xlabel("x")
ax.set_ylabel("fhe_equality(x, 0)")
ax.set_title(f"k sweep  (eps={EPS_FIXED}) — solid=converges, dashed=diverges")
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

# Plot 4: max error vs k
ax = axes[1, 1]
k_vals_plot = sorted(k_sweep_results.keys())
max_errs = [np.max(np.abs(k_sweep_results[k][0] - k_sweep_results[k][1])) for k in k_vals_plot]
kx_prods = [k_sweep_results[k][2] for k in k_vals_plot]
colors_bar = ["seagreen" if kx < TANH_CONVERGENCE_RADIUS else "coral" for kx in kx_prods]
ax.bar([str(k) for k in k_vals_plot], max_errs, color=colors_bar)
ax.axhline(0.05, color="red", lw=1.5, ls="--", label="5% error threshold")
ax.set_xlabel("k value")
ax.set_ylabel("max |FHE - ref|")
ax.set_title(f"Max error vs k  (eps={EPS_FIXED})\ngreen=k·ε<1.5 (converges), red=diverges")
ax.legend()
ax.grid(True, axis="y", alpha=0.3)
ax.set_yscale("symlog", linthresh=0.01)

plt.tight_layout()
plt.savefig("fhe_equality_convergence.png", dpi=150)
plt.show()
print("Saved: fhe_equality_convergence.png")
