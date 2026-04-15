from fhelib.ciphertext import Ciphertext
from fhelib.basic.conjugate import conjugate

a = Ciphertext(8)

a.set_element(0, 1)

a = conjugate(a)

print(a)