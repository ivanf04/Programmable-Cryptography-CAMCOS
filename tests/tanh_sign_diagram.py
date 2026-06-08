"""
Shows tanh(k·x) as an approximation of the sign function for increasing k.
"""

import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-3, 3, 2000)

ks = [1, 3, 8, 20]
colors = ["#a8c8e8", "#5aabcf", "#2171b5", "#08306b"]

fig, ax = plt.subplots(figsize=(9, 5.5))

# tanh(k·x) curves
for k, color in zip(ks, colors):
    ax.plot(x, np.tanh(k * x), color=color, lw=2, label=f"tanh({k}x)")


ax.axhline(0, color="black", lw=0.6, alpha=0.4)
ax.axvline(0, color="black", lw=0.6, alpha=0.4)

ax.set_xlim(-3, 3)
ax.set_ylim(-1.35, 1.35)
ax.set_xlabel("x", fontsize=12)
ax.set_ylabel("f(x)", fontsize=12)
ax.set_title("tanh(kx) → sign(x)  as  k → ∞", fontsize=14, pad=12)

ax.legend(loc="upper left", fontsize=10, framealpha=0.9)

ax.annotate(
    "larger k ⟹ sharper step",
    xy=(0.72, 0.65),
    xycoords="axes fraction",
    fontsize=9.5,
    color="#2171b5",
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#2171b5", alpha=0.85),
)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig("tests/tanh_sign_diagram.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved: tests/tanh_sign_diagram.png")
