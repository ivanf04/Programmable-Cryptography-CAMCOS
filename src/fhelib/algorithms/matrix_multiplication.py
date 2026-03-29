from fhelib import Ciphertext
from fhelib.algorithms.product import dot_product
from fhelib.primitives.cycle import cycle
from fhelib.algorithms.sum import intravector_partsum
import numpy as np


def nxn_matrix_multiply_n_vectors(A_rows: list, B_cols: list, n: int):
    """
    A_rows: list of n Ciphertexts, each encoding a row of A
    B_cols: list of n Ciphertexts, each encoding a column of B
    returns: n x n list of complex scalars representing C = A*B
    """
    C = []
    for i in range(n):
        row = []
        for j in range(n):
            c_ij = dot_product(A_rows[i], B_cols[j])
            row.append(c_ij)
        C.append(row)
    return C


def make_mask(n: int) -> Ciphertext:
    """Creates a mask with 1s at positions 0 and n²-1"""
    X = Ciphertext(n * n)
    X.set_element(0, 1)
    X.set_element(n * n - 1, 1)
    return X


def matrix_multiply_n2_vector_2x2(A_prime: Ciphertext, B_prime: Ciphertext, n: int = 2) -> Ciphertext:
    """
    n² vector approach to matrix multiplication for 2x2 matrices.
    A_prime: flattened rows of A as a single Ciphertext
    B_prime: flattened columns of B as a single Ciphertext
    returns: flattened result matrix C = A*B as a Ciphertext
    """
    B_double_prime = cycle(B_prime.copy(), -n)  # ct first, k second
    X = make_mask(n)

    C_x = intravector_partsum(np.multiply(A_prime, B_prime), n)
    C_y = intravector_partsum(np.multiply(A_prime, B_double_prime), n)

    return np.multiply(C_x, X) + np.multiply(C_y, 1 - X)