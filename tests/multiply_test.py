from fhelib.ciphertext import Ciphertext
from fhelib.primitives.multiply import multiply

a = Ciphertext(8)
b = Ciphertext(8)

a.set_element(0, 3)
a.set_element(1, 4)
b.set_element(0, 2)
b.set_element(1, 3)


c = multiply(a, b)
print(c)
