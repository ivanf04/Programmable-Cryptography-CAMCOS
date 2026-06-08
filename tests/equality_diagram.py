"""
Visual diagram for fhe_equality: shows point a with ±ε tails and point x
side by side. Color codes x green (inside window) or red (outside).
Also shows the fhe_equality output value using the sech² approach.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



def draw_equality_diagram(ax, a: float, x_val: float, epsilon: float, title: str = ""):
    """
    Draw a single equality diagram on ax.

    Left column:  a  with vertical tails at a±ε
    Right column: x  as a colored dot
    """
    A_COL = 0.3   # horizontal position of a
    X_COL = 0.7   # horizontal position of x

    in_range = abs(x_val - a) <= epsilon
    dot_color = "#2e9e5b" if in_range else "#d94f3b"   # green / red

    # ── shaded tolerance window around a ─────────────────────────────────────
    window = mpatches.FancyBboxPatch(
        (A_COL - 0.08, a - epsilon),
        width=0.16,
        height=2 * epsilon,
        boxstyle="square,pad=0",
        facecolor="#aecde8",
        edgecolor="none",
        alpha=0.45,
        zorder=1,
        transform=ax.transData,
    )
    ax.add_patch(window)

    # ── vertical spine (the "tails") ─────────────────────────────────────────
    ax.plot([A_COL, A_COL], [a - epsilon, a + epsilon],
            color="#2171b5", lw=2.2, zorder=2, solid_capstyle="butt")

    # top cap
    ax.plot([A_COL - 0.07, A_COL + 0.07], [a + epsilon, a + epsilon],
            color="#2171b5", lw=3, zorder=2, solid_capstyle="butt")

    # bottom cap
    ax.plot([A_COL - 0.07, A_COL + 0.07], [a - epsilon, a - epsilon],
            color="#2171b5", lw=3, zorder=2, solid_capstyle="butt")

    # dot at a
    ax.plot(A_COL, a, "o", color="#2171b5", ms=9, zorder=3)

    # ── dot at x ─────────────────────────────────────────────────────────────
    ax.plot(X_COL, x_val, "o", color=dot_color, ms=9, zorder=3)

    # dashed horizontal reference line from x to the a column
    ax.plot([A_COL + 0.08, X_COL - 0.02], [x_val, x_val],
            "--", color=dot_color, lw=1.2, alpha=0.55, zorder=1)

    # ── value labels ─────────────────────────────────────────────────────────
    y_pad = epsilon * 0.18

    # a+ε label (above top cap)
    ax.text(A_COL, a + epsilon + y_pad, f"a+ε = {a + epsilon:.3g}",
            ha="center", va="bottom", fontsize=8.5, color="#2171b5")

    # a-ε label (below bottom cap)
    ax.text(A_COL, a - epsilon - y_pad, f"a−ε = {a - epsilon:.3g}",
            ha="center", va="top", fontsize=8.5, color="#2171b5")

    # a label (centred on the dot, offset right)
    ax.text(A_COL + 0.09, a, f"a = {a:.3g}",
            ha="left", va="center", fontsize=8.5, color="#2171b5", fontweight="bold")

    # x label
    ax.text(X_COL + 0.04, x_val, f"x = {x_val:.3g}",
            ha="left", va="center", fontsize=8.5, color=dot_color, fontweight="bold")

    # ── verdict footer ───────────────────────────────────────────────────────
    verdict = "EQUAL  ✓" if in_range else "NOT EQUAL  ✗"
    ax.text(0.5, 0.04, verdict, transform=ax.transAxes,
            ha="center", va="bottom", fontsize=8.5, color=dot_color,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor=dot_color, lw=1.2, alpha=0.9))

    # ── axes formatting ───────────────────────────────────────────────────────
    view_half = max(abs(x_val - a), epsilon) * 1.6 + epsilon * 0.5
    ax.set_ylim(a - view_half, a + view_half)
    ax.set_xlim(0.0, 1.1)
    ax.set_xticks([A_COL, X_COL])
    ax.set_xticklabels(["a", "x"], fontsize=11)
    ax.yaxis.set_tick_params(labelsize=8)
    ax.set_ylabel("value", fontsize=9)
    ax.axhline(a, color="#2171b5", lw=0.6, ls=":", alpha=0.35, zorder=0)
    ax.grid(True, axis="y", alpha=0.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if title:
        ax.set_title(title, fontsize=10, pad=8)


# ── figure: two cases for a = 0.5, ε = 0.1 ──────────────────────────────────

A   = 0.5
EPS = 0.1

cases = [
    (A, 0.55, EPS, "x inside window\nx = 0.55"),
    (A, 0.72, EPS, "x outside window\nx = 0.72"),
]

fig, axes = plt.subplots(1, 2, figsize=(9, 6.5))
fig.suptitle(
    f"fhe_equality(x, a)   |   a = {A},  ε = {EPS}",
    fontsize=13,
    y=1.01,
)

for ax, (a, x, eps, title) in zip(axes, cases):
    draw_equality_diagram(ax, a, x, eps, title=title)

plt.tight_layout()
plt.savefig("equality_diagram.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved: equality_diagram.png")
