from fhelib.ciphertext import Ciphertext
from fhelib.auxiliary.division import reciprocal_newton_universal_guess, adaptive_guess
import numpy as np

"""
Newton's method reciprocal test
Using hackmd example: approximate 1/48 starting from x0 = 1/64

TODO: test false convergence case - starting x0 too close to 0
TODO: test poorly chosen x0 requiring 30+ iterations
TODO: compare iteration count vs geometric series for same accuracy
"""

print("=" * 50)
print("Test 1: 1/48 with explicit x0 = 1/64 (hackmd example)")
print("=" * 50)

v = Ciphertext(4)
v.set_element(0, 48.0)

true_val = 1 / 48
print(f"True 1/48: {true_val:.10f}")
print(f"x0 = 1/64 = {1/64:.10f}")
print()

for n_iters in [1, 2, 3, 4, 5]:
    result = reciprocal_newton_universal_guess(v, n=n_iters, x0=1 / 64)
    got = float(np.real(result[0]))
    error = abs(got - true_val)
    print(f"n={n_iters}: {got:.10f}  error: {error:.2e}")

print()
print("=" * 50)
print("Test 2: multiple values with assumed_range")
print("assumed_range = (32, 64), x0 = 1/sqrt(32*64) = 1/45.25")
print("=" * 50)

v2 = Ciphertext(4)
vals = [48.0, 50.0, 33.0, 60.0]
for idx, val in enumerate(vals):
    v2.set_element(idx, val)

print(
    f"z_max = {max(vals)}, convergence requires x0 < 2/{max(vals)} = {2/max(vals):.4f}"
)
print()
result2 = reciprocal_newton_universal_guess(v2, n=5, assumed_range=(32, 64))
for i, val in enumerate(vals):
    got = float(np.real(result2[i]))
    print(f"1/{val}: got {got:.7f}  expected {1/val:.7f}  error {abs(got - 1/val):.2e}")

print()
print("=" * 50)
print("Test 3: adaptive guess for values in [1, 2^16]")
print("=" * 50)

v3 = Ciphertext(8)
test_vals = [1.5, 3.0, 5.0, 48.0, 100.0, 1000.0, 32768.0, 0.0]
for idx, val in enumerate(test_vals):
    v3.set_element(idx, val)

print(f"Input: {test_vals}")
x0s = adaptive_guess(v3, b=16)
for i, val in enumerate(test_vals[:7]):
    print(f"x={val}: adaptive x0={float(np.real(x0s[i])):.6f}  true 1/x={1/val:.6f}")


print()
print("=" * 50)
print("Test 3b: adaptive guess with Newton's method (per element x0)")
print("=" * 50)

x0_vec = np.real(x0s)
z = np.real(v3)
x = x0_vec.copy()

for _ in range(5):
    x = 2 * x - (x**2) * z

for i, val in enumerate(test_vals[:7]):
    got = float(np.real(x[i]))
    print(f"1/{val}: got {got:.7f}  expected {1/val:.7f}  error {abs(got - 1/val):.2e}")

print()
print("=" * 50)
print("Test 3c: EXPECTED FAIL - using averaged x0 across wide range")
print("Using mean of adaptive guesses as single x0 for all elements")
print("Fails x0 isn't in convergence basin (0, 2/z_max)")
print("for all elements when range is wide e.g. [1.5, 32768]")
print("=" * 50)

bad_x0 = float(np.real(x0s).mean())
print(f"averaged x0: {bad_x0:.6f}")
print(f"convergence requires x0 < 2/32768 = {2/32768:.6f}")
print(f"bad_x0 > 2/z_max so large values will diverge")
result_bad = reciprocal_newton_universal_guess(v3, n=5, x0=bad_x0)
for i, val in enumerate(test_vals[:7]):
    got = float(np.real(result_bad[i]))
    print(f"1/{val}: got {got:.7f}  expected {1/val:.7f}")
