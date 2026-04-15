from fhelib import Ciphertext
from fhelib.basic.add       import add
from fhelib.basic.multpily  import multiply

""" return difference of two ciphertexts 
"""

def sub(a:Ciphertext, b:Ciphertext):
    ctneg = Ciphertext(len(a), -1) # TODO modify ct constr. 
    b = multiply(b, ctneg)
    return add(a, b)