import numpy as np
from fhelib.ciphertext import Ciphertext

"""
equailty method
@param
    a: Ciphertext
    b: int or float
    tol: float
@return 
    x: Ciphertext
        1's where a[i] == b, 0 otherwise
"""

def equality(a: Ciphertext, b, tol: float) -> Ciphertext:
    # create CT with values of b in every index
    b_ct = np.ones_like(a) * b
    print(f"b_ct:\n{b_ct}")

    # create two CT's (a - b_ct) and (b_ct - a)
    # we can use this 
    for i in range(a.size):


