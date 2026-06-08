import numpy as np
from fhelib.ciphertext import Ciphertext
from fhelib.lowlevel.sign import sign_heaviside
from fhelib.lowlevel.sum import intravector_sum
from fhelib.primitives.multiply import multiply
from fhelib.auxiliary.equality import fhe_equality

"""
Median implementation using Method 1 from hackmd.
Assumes N/2 is odd and all values are distinct.

Steps:
1. Build D where D[i,j] = Sign_{-1,1,0}(z_i - z_j) applied rowwise
2. Sum each row using intravector_sum
3. Find where row sum == 0 using fhe_equality
4. Multiply mask by z and sum to get median value
"""

def median_position(z: Ciphertext, n: int, epsilon: float = 0.5):
    z_real = np.real(z[:n])
    D = np.zeros((n, n))

    # Step 1: build D rowwise using sign_heaviside
    for i in range(n):
        row_ct = Ciphertext(8)
        for j in range(n):
            row_ct.set_element(j, z_real[i] - z_real[j])
        signed_row = sign_heaviside(row_ct, a=-1, b=1, c=0)
        D[i] = np.real(signed_row)[:n]
        D[i][i] = 0  # diagonal = 0

    # # Step 2: row sums using intravector_sum
    # row_sums = np.zeros(n)
    # for i in range(n):
    #     row_ct = Ciphertext(8)
    #     for j in range(n):
    #         row_ct.set_element(j, D[i][j])
    #     row_sums[i] = np.real(intravector_sum(row_ct))

    row_sums = D.sum(axis=1)

    print(f"row_sums: {row_sums}")
    print(f"z_vals:   {z_real}")

    # Step 3: find where row sum == 0
    row_sums_ct = Ciphertext(8)
    for i in range(n):
        row_sums_ct.set_element(i, row_sums[i])
    return fhe_equality(row_sums_ct, 0, epsilon=epsilon)

def median_value(z: Ciphertext, n: int, epsilon: float = 0.5):
    """Returns median value via Sum(m * z)"""
    m = median_position(z, n=n, epsilon=epsilon)
    return intravector_sum(multiply(m, z))