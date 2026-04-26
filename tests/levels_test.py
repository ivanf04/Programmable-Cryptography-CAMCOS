import math
import numpy as np
from fhelib.ciphertext import Ciphertext
from fhelib.primitives.multiply import multiply, chain_multiply
from fhelib.lowlevel.power import raise_to_power


# ── helpers ───────────────────────────────────────────────────────────────────


def make_ct(length=4, level=15, fill=1.0):
    ct = Ciphertext(length)
    ct[:] = fill
    ct.set_level(level)
    return ct


def header(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print(f"{'='*55}")


def show(label, ct, expected=None):
    lvl = ct.get_level()
    ok = (
        ""
        if expected is None
        else ("  ✓" if lvl == expected else f"  ✗ (expected {expected})")
    )
    print(f"  {label:<40} level = {lvl}{ok}")


# ── 1. basic single multiply cases ────────────────────────────────────────────

header("1. Single multiply — all type combos")

a = make_ct(level=15)
b = make_ct(level=12)

r_ct_ct = multiply(a, b)
show("ct(15) * ct(12)", r_ct_ct, expected=11)  # min(14,11)

r_ct_int = multiply(a, 3)
show("ct(15) * int", r_ct_int, expected=15)  # no drop

r_ct_flt = multiply(a, 3.0)
show("ct(15) * float", r_ct_flt, expected=14)  # -1

r_ct_arr = multiply(a, np.ones(4))
show("ct(15) * np.ndarray", r_ct_arr, expected=14)  # -1

# swapped order: scalar first
r_int_ct = multiply(3, a)
show("int * ct(15)  [swapped]", r_int_ct, expected=15)

r_flt_ct = multiply(3.0, a)
show("float * ct(15) [swapped]", r_flt_ct, expected=14)


# ── 2. sequential ct*ct multiplications ───────────────────────────────────────

header("2. Sequential ct*ct  (naive, costs 1 level each)")

x = make_ct(level=15)
print(f"  start level = {x.get_level()}")
for i in range(1, 6):
    x = multiply(x, make_ct(level=x.get_level()))
    show(f"  after multiply #{i}", x)


# ── 3. chain_multiply — log2 level cost ───────────────────────────────────────

header("3. chain_multiply  —  ceil(log2(n)) levels consumed")

for n in [2, 4, 8, 16]:
    terms = [make_ct(level=15) for _ in range(n)]
    result = chain_multiply(terms)
    expected = 15 - math.ceil(math.log2(n))
    show(f"chain_multiply {n:>2} cts", result, expected=expected)

print()
print("  compare naive vs tree for n=8:")
naive = make_ct(level=15)
for _ in range(7):  # 7 sequential multiplies
    naive = multiply(naive, make_ct(level=naive.get_level()))
show("  naive  (7 sequential)", naive)  # level = 15 - 7 = 8

tree = chain_multiply([make_ct(level=15) for _ in range(8)])
show("  tree   (log2 depth)  ", tree)  # level = 15 - 3 = 12


# ── 4. raise_to_power — repeated squaring ────────────────────────────────────

header("4. raise_to_power  —  ceil(log2(a)) levels consumed")

base_level = 15
for exp in [2, 4, 6, 8, 16]:
    ct = make_ct(level=base_level)
    result = raise_to_power(ct, exp)
    depth = math.ceil(math.log2(exp))
    show(f"x^{exp:<2}  (depth=ceil(log2({exp}))={depth})", result)

print()
print("  x^8 step-by-step (repeated squaring):")
ct = make_ct(level=15)
ct2 = multiply(ct, ct)
show("    x^2  = x*x", ct2)  # -1 → 14
ct4 = multiply(ct2, ct2)
show("    x^4  = x^2 * x^2", ct4)  # -1 → 13
ct8 = multiply(ct4, ct4)
show("    x^8  = x^4 * x^4", ct8)  # -1 → 12


# ── 5. mixed levels in chain_multiply ────────────────────────────────────────

header("5. chain_multiply with mixed input levels")

terms = [
    make_ct(level=15),
    make_ct(level=12),  # lowest ct
    make_ct(level=14),
    3,  # int  — no level
    2.0,  # float — no level
]
result = chain_multiply(terms)
# 3 cts → depth = ceil(log2(3)) = 2,  min_ct_level = 12  → 12-2 = 10
show("ct(15)*ct(12)*ct(14)*int*float", result, expected=10)


# ── 6. level-awareness: catching level exhaustion ─────────────────────────────

header("6. Level exhaustion warning")

low = make_ct(level=2)
print(f"  starting level = {low.get_level()}")
for i in range(1, 4):
    low = multiply(low, make_ct(level=low.get_level()))
    flag = "  ⚠ level exhausted!" if low.get_level() <= 0 else ""
    show(f"  multiply #{i}", low)
    if low.get_level() <= 0:
        print(f"         {flag}")
        break
