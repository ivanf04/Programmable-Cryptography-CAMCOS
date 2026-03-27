from fhelib.ciphertext import Ciphertext
from fhelib.primitives.conjugate import conjugate

a = Ciphertext(8)

a.set_element(0, 1)

a = conjugate(a)

print(a)