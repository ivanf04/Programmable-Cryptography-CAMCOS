"""
Tests for the tanh FHE approximation.

Graphs produced:
  1. Convergence  — approximation vs exact tanh, and max |error| vs n_terms
  2. Op counts    — add and multiply primitives consumed per tanh() call
"""

import numpy as np
import matplotlib.pyplot as plt
from fhelib import Ciphertext
from fhelib.lowlevel.tanh import tanh
from fhelib.primitives import reset, get_counts

# 16 x-values spread across the Taylor convergence range (|x| < π/2 ≈ 1.57)
N_SLOTS = 16
x_vals = np.linspace(-1.4, 1.4, N_SLOTS)
exact = np.tanh(x_vals)

ct = Ciphertext(N_SLOTS)
for i, v in enumerate(x_vals):
    ct[i] = v

# ── convergence ───────────────────────────────────────────────────────────────

print("=" * 55)
print("tanh convergence test  (|x| ≤ 1.4, within Taylor radius)")
print("=" * 55)
print(f"{'n_terms':>7}  {'max |err|':>10}  {'mean |err|':>11}")
print("-" * 35)

approx_by_n = {}
max_errors = []

for n in range(1, 10):
    approx = np.real(np.array(tanh(ct, n_terms=n)))
    err = np.abs(approx - exact)
    approx_by_n[n] = approx
    max_errors.append(err.max())
    print(f"  {n:>5}  {err.max():>10.6f}  {err.mean():>11.6f}")

# ── op counts ─────────────────────────────────────────────────────────────────

print()
print("=" * 55)
print("Primitive operation counts per tanh() call")
print("=" * 55)
print(f"{'n_terms':>7}  {'adds':>6}  {'multiplies':>10}  {'total':>7}")
print("-" * 38)

counts_by_n = {}
for n in range(1, 10):
    reset()
    tanh(ct, n_terms=n)
    c = get_counts()
    counts_by_n[n] = (c["add"], c["multiply"])
    print(f"  {n:>5}  {c['add']:>6}  {c['multiply']:>10}  {c['add']+c['multiply']:>7}")

ns = list(range(1, 10))

# ── Figure 1: convergence ─────────────────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("tanh Taylor approximation — convergence", fontsize=13)

colors = plt.cm.plasma(np.linspace(0.1, 0.9, 9))

ax1.plot(x_vals, exact, "k-", lw=2.5, label="exact tanh(x)", zorder=10)
for i, n in enumerate(ns):
    ax1.plot(x_vals, approx_by_n[n], color=colors[i], lw=1.3,
             alpha=0.85, label=f"n={n}")
ax1.set_xlabel("x")
ax1.set_ylabel("tanh(x)")
ax1.set_title("Approximation vs exact")
ax1.legend(fontsize=7, ncol=2)
ax1.grid(True, alpha=0.3)

ax2.semilogy(ns, max_errors, "o-", color="steelblue", lw=2, ms=7)
for n, e in zip(ns, max_errors):
    ax2.annotate(f"{e:.1e}", (n, e), textcoords="offset points",
                 xytext=(0, 8), ha="center", fontsize=7)
ax2.set_xticks(ns)
ax2.set_xlabel("n_terms")
ax2.set_ylabel("max |error|  (log scale)")
ax2.set_title("Max absolute error vs n_terms")
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("tanh_convergence.png", dpi=150)
plt.show()
print("Saved: tanh_convergence.png")

# ── Figure 2: op counts ───────────────────────────────────────────────────────

adds  = [counts_by_n[n][0] for n in ns]
mults = [counts_by_n[n][1] for n in ns]
totals = [a + m for a, m in zip(adds, mults)]

fig, ax = plt.subplots(figsize=(9, 5))
fig.suptitle("Primitive operations per tanh() call", fontsize=13)

x_pos = np.arange(len(ns))
width = 0.35
bars_add  = ax.bar(x_pos - width / 2, adds,  width, label="add",      color="steelblue")
bars_mult = ax.bar(x_pos + width / 2, mults, width, label="multiply",  color="coral")

for bar, val in zip(bars_add, adds):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            str(val), ha="center", va="bottom", fontsize=8)
for bar, val in zip(bars_mult, mults):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            str(val), ha="center", va="bottom", fontsize=8)

ax.plot(x_pos, totals, "k^--", lw=1.5, ms=7, label="total", zorder=5)

ax.set_xticks(x_pos)
ax.set_xticklabels([f"n={n}" for n in ns])
ax.set_xlabel("n_terms")
ax.set_ylabel("operation count")
ax.legend()
ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("tanh_ops.png", dpi=150)
plt.show()
print("Saved: tanh_ops.png")
