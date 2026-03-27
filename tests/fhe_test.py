from fhelib.ciphertext import Ciphertext
from fhelib.algorithms.sum import *
import numpy as np 

a = Ciphertext(16)
b = Ciphertext(16)
a.set_element(0, 1)
b.set_element(0, 1)

c = intravector_sum_naive(a)
d = intravector_sum(a)

print(c)
print(d)
e = a + b
print(e)