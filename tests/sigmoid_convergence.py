"""
Tests for the sigmoid FHE approximation.

sigmoid(x) = 1/(1+e^{-x}) is approximated in two nested steps:
  1. e^{-x} via degree-n Taylor expansion
  2. 1/(1+u) via degree-m geometric series

We sweep n=m together (labeled "terms") so the x-axis is directly
comparable to tanh_test.py's n_terms axis.

Graphs produced (scales matched to tanh_test.py for slideshow comparison):
  1. Convergence  — approximation curves vs exact sigmoid for each (n=m)
  2. Accuracy     — max |error| vs terms on a shared log scale
  3. Move counts  — add and multiply primitives per sigmoid() call
"""

import numpy as np
import matplotlib.pyplot as plt
from fhelib import Ciphertext
from fhelib.lowlevel.sigmoid import sigmoid
from fhelib.primitives import reset, get_counts

# ── shared constants — match tanh_test.py exactly ────────────────────────────

N_SLOTS      = 16
X_MIN, X_MAX = -1.4, 1.4
COLORS       = plt.cm.plasma(np.linspace(0.1, 0.9, 5))
FIGSIZE_1    = (9, 5)

# ── input ciphertext ──────────────────────────────────────────────────────────

x_vals = np.linspace(X_MIN, X_MAX, N_SLOTS)
exact  = 1 / (1 + np.exp(-x_vals))

ct = Ciphertext(N_SLOTS)
for i, v in enumerate(x_vals):
    ct[i] = v

# ── collect data: n = m swept 1 → 5 ─────────────────────────────────────────

TERMS  = list(range(1, 6))
labels = [f"n=m={p}" for p in TERMS]

print("=" * 55)
print("sigmoid convergence  (|x| ≤ 1.4,  n = m swept 1–5)")
print("=" * 55)
print(f"{'terms':>6}  {'max |err|':>10}  {'mean |err|':>11}")
print("-" * 35)

approx_by_p = {}
max_errors  = []

for p in TERMS:
    approx = np.real(np.array(sigmoid(ct, n=p, m=p)))
    err    = np.abs(approx - exact)
    approx_by_p[p] = approx
    max_errors.append(err.max())
    print(f"  ({p},{p})  {err.max():>10.6f}  {err.mean():>11.6f}")

print()
print("=" * 55)
print("Primitive operation counts per sigmoid() call")
print("=" * 55)
print(f"{'terms':>6}  {'adds':>6}  {'multiplies':>10}  {'total':>7}")
print("-" * 38)

counts_by_p = {}
for p in TERMS:
    reset()
    sigmoid(ct, n=p, m=p)
    c = get_counts()
    counts_by_p[p] = (c["add"], c["multiply"])
    print(f"  ({p},{p})  {c['add']:>6}  {c['multiply']:>10}  {c['add']+c['multiply']:>7}")

# ── Figure 1: convergence (curves vs exact) ───────────────────────────────────

fig, ax = plt.subplots(figsize=FIGSIZE_1)
fig.suptitle("sigmoid approximation — convergence", fontsize=13)

ax.plot(x_vals, exact, "k-", lw=2.5, label="exact sigmoid(x)", zorder=10)
for i, p in enumerate(TERMS):
    ax.plot(x_vals, approx_by_p[p], color=COLORS[i], lw=1.3,
            alpha=0.85, label=f"n=m={p}")

ax.set_xlabel("x")
ax.set_ylabel("sigmoid(x)")
ax.set_title("Approximation vs exact  (n = m)")
ax.set_ylim(-0.3, 1.3)
ax.legend(fontsize=8, ncol=2)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("sigmoid_convergence.png", dpi=150)
plt.show()
print("Saved: sigmoid_convergence.png")

# ── Figure 2: accuracy (max |error| log scale) ────────────────────────────────

fig, ax = plt.subplots(figsize=FIGSIZE_1)
fig.suptitle("sigmoid approximation — accuracy", fontsize=13)

ax.semilogy(TERMS, max_errors, "o-", color="steelblue", lw=2, ms=7)
for p, e in zip(TERMS, max_errors):
    ax.annotate(f"{e:.1e}", (p, e), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=7)

ax.set_xticks(TERMS)
ax.set_xticklabels(labels, fontsize=8)
ax.set_xlabel("(n, m)  [n = m]")
ax.set_ylabel("max |error|  (log scale)")
ax.set_title("Max absolute error vs (n, m)")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("sigmoid_accuracy.png", dpi=150)
plt.show()
print("Saved: sigmoid_accuracy.png")

# ── Figure 3: move counts ─────────────────────────────────────────────────────

adds   = [counts_by_p[p][0] for p in TERMS]
mults  = [counts_by_p[p][1] for p in TERMS]
totals = [a + m for a, m in zip(adds, mults)]

fig, ax = plt.subplots(figsize=FIGSIZE_1)
fig.suptitle("Primitive operations per sigmoid() call", fontsize=13)

x_pos = np.arange(len(TERMS))
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
ax.set_xticklabels(labels)
ax.set_xlabel("(n, m)  [n = m]")
ax.set_ylabel("operation count")
ax.legend()
ax.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("sigmoid_ops.png", dpi=150)
plt.show()
print("Saved: sigmoid_ops.png")
