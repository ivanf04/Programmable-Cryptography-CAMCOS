import numpy as np
from fhelib import Ciphertext
from fhelib.lowlevel.sigmoid import sigmoid
from fhelib.primitives import reset, get_counts

CT_LENGTH = 4   # small power-of-2 ciphertext for testing

# set up a ciphertext with a spread of values to exercise the approximation
x = Ciphertext(CT_LENGTH)
for i in range(CT_LENGTH):
    x[i] = (i - CT_LENGTH / 2)   # e.g. [-2, -1, 0, 1]

# expected sigmoid values for reference (plaintext)
expected = 1 / (1 + np.exp(-np.array([i - CT_LENGTH / 2 for i in range(CT_LENGTH)])))

print("=" * 60)
print("Sigmoid approximation test")
print("=" * 60)
print(f"Input x:          {np.real(np.array(x))}")
print(f"Expected sigmoid: {np.round(expected, 6)}")
print("=" * 60)

header = f"{'n':>4}  {'m':>4}  {'adds':>6}  {'mults':>6}  {'total':>6}  result (real part)"
print(header)
print("-" * len(header))

for n in range(1, 6):
    for m in range(1, 6):
        reset()
        result = sigmoid(x, n=n, m=m)
        counts = get_counts()
        total = counts["add"] + counts["multiply"]
        real_result = np.round(np.real(np.array(result)), 4)
        print(f"  n={n}  m={m}  adds={counts['add']:>4}  mults={counts['multiply']:>4}  total={total:>4}  {real_result}")
    print()
