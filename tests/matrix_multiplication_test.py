from fhelib.ciphertext import Ciphertext
from fhelib.algorithms.matrix_multiplication import nxn_matrix_multiply_n_vectors, matrix_multiply_n2_vector_2x2

# Test matrices:
# A = [[1,2],[3,4]]
# B = [[5,6],[7,8]]
# A*B = [[19,22],[43,50]]

print("=" * 50)
print("Approach 1: n vectors of length n")
print("=" * 50)

a1 = Ciphertext(4); a1.set_element(0, 1); a1.set_element(1, 2)  # row 1 of A
a2 = Ciphertext(4); a2.set_element(0, 3); a2.set_element(1, 4)  # row 2 of A
b1 = Ciphertext(4); b1.set_element(0, 5); b1.set_element(1, 7)  # col 1 of B
b2 = Ciphertext(4); b2.set_element(0, 6); b2.set_element(1, 8)  # col 2 of B

print(f"A = [[1,2],[3,4]]  encoded as rows: a1={a1}, a2={a2}")
print(f"B = [[5,6],[7,8]]  encoded as cols: b1={b1}, b2={b2}")

C = nxn_matrix_multiply_n_vectors([a1, a2], [b1, b2], 2)
print(f"\nResult C = A*B:")
for i, row in enumerate(C):
    print(f"  row {i}: {[complex(x) for x in row]}")
print(f"Expected:  [[19,22],[43,50]]")

print()
print("=" * 50)
print("Approach 2: length-n² vector")
print("=" * 50)

# A flattened by rows: (1,2,3,4)
# B flattened by cols: (5,7,6,8)
A_prime = Ciphertext(4)
A_prime.set_element(0, 1); A_prime.set_element(1, 2)
A_prime.set_element(2, 3); A_prime.set_element(3, 4)

B_prime = Ciphertext(4)
B_prime.set_element(0, 5); B_prime.set_element(1, 7)
B_prime.set_element(2, 6); B_prime.set_element(3, 8)

print(f"A' (rows of A flattened): {A_prime}")
print(f"B' (cols of B flattened): {B_prime}")

C2 = matrix_multiply_n2_vector_2x2(A_prime, B_prime)
print(f"\nResult C = A*B (flattened): {[complex(x) for x in C2]}")
print(f"Expected:                   [19, 22, 43, 50]")