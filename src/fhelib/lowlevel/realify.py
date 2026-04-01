from fhelib import Ciphertext
import numpy as np


""" convert ct to reals only from complex 
    adding a complex number and its conjugate returns 2*(real),
    so divide that by half
    concrete FHE equivalent to np.real(ct)
"""
def realify(ct:Ciphertext):
    return (ct + np.conjugate(ct)) * 0.5

# TODO by Dwyer: validate how we intend to call function using wrapper