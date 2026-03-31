import numpy as np 
from fhelib.lowlevel.realify import realify
from fhelib import Ciphertext
"""
Returns 0 if x_i is <= 0 or 1 if x_i > 0
TODO: use a sigmoid approximation for the output  
TODO: refactor with 'good_if'
"""

# def sign(a: Ciphertext) -> Ciphertext:
#     s = Ciphertext(a.size)
#     for i in range(a.size):
#         if(a[i] <= 0):
#             s[i] = 0
#         else:
#             s[i] = 1
#     return s


"""
sigmoid based approximation for the sign function 
@param 
    x: Ciphertext
        Input Ciphertext
    k: float
        Sigmoid steepness (larger = sharper transition toward 0).
    power: int or float
        Raise sigmoid to this power to sharpen the curve
    tol: float
        Values <= tol become 0, else become 1
@return
    out: Ciphertext
        Output with 1's and 0's 
"""
def sign(x: Ciphertext, k=10.0, power=8, tol=1e-6) -> Ciphertext:
    x = realify(x)
    s = 1.0 / (1.0 + np.exp(-k * x))
    y = s ** power
    y[y <= tol] = 0.0
    y[y >= 1.0 - tol] = 1.0

    out = np.zeros_like(y)
    out[y > 0.5] = 1.0
    return out

