from fhelib.lowlevel.dot_product import *
from fhelib.ciphertext import Ciphertext


a = Ciphertext(8)
b = Ciphertext(8)

a.set_element(0, 3)
a.set_element(1, 4)
b.set_element(0, 2)
b.set_element(1, 3)


print(f"a: {a}")
print(f"b: {b}")

c = dot_product(a, b)
print(f"dot product (expect 18): {c}")

# complex inner product: same as dot product here since all values are real
d = complex_inner_product(a, b)
print(f"complex inner product (expect 18): {d}")