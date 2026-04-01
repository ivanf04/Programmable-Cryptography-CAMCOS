import numpy as np 
from fhelib.lowlevel.realify import realify
from fhelib import Ciphertext
"""
Returns 0 if x_i is <= 0 or 1 if x_i > 0
TODO: refactor with 'good_if'
TODO: refactor to output {0,1/2,1}
"""

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

    # normalize values to 1 and zero based on tolerance
    y[y <= tol] = 0.0   
    y[y >= 1.0 - tol] = 1.0

    # clean up the data, set equal length CT to all 0 and 1 in corresponding elements of y 
    out = np.zeros_like(y)
    out[y > 0.5] = 1.0
    return out

"""
Sign function as described in the "Spring 2026" hackmd
"""
def sign_half_equality(x: Ciphertext, k=10.0, tol=0.25) -> Ciphertext:
    # x = realify(x)  
    print(f"intial CT:\n{x}")
    s = 1.0 / (1.0 + np.exp(-k * x))

    # normalize values to 1, 1.5 and zero based on tolerance
    s[s <= tol] = 0.0   
    s[(s > tol) & (s < 1 - tol)] = 0.5
    s[s >= 1.0 - tol] = 1.0

    return s


"""
Use the original sign method to create a heaviside-type function
see "CAMCOS 2026 Spring" hackmd for details 
"""
def sign_heaviside(x: Ciphertext, a, b, c) -> Ciphertext:
    return a + ((b - a) * sign(x - c))