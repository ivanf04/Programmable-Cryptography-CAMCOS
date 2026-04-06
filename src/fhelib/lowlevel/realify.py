# surely there's a better way to do imports??
from fhelib import Ciphertext
from fhelib.basic.add       import add
from fhelib.basic.multiply  import multiply
from fhelib.basic.conjugate import conjugate

""" convert ct to reals only from complex 
    adding a complex number and its conjugate returns 2*(real),
    so divide that by half
    concrete FHE equivalent to np.real(ct)
"""
def realify(ct:Ciphertext):
    ct_halve = Ciphertext(len(ct), 0.5+0j)
    ct_result = add(ct, conjugate(ct))
    ct_result = multiply(ct_result, ct_halve)
    return ct_result