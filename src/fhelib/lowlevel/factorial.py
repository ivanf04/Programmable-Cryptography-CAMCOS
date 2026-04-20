"""
A simple factorial implementation in FHE
Goal: create a ciphertext with elemets of x! for every element x. 
This will be used to approxiate the exponential function. With testing we will know how long the ct will need to be 
"""
import numpy as np 
from fhelib.primitives import multiply
from fhelib import Ciphertext
"""
Generate a ciphertext of length n, with each element as n_i! with n_i going from 0 to n

:param n: the length of the output ciphertext with n! in as the nth element

:return ct: Ciphertext with length n containing 0! up to n!
"""
def factorial(n:int):
    ct = Ciphertext(n)
    ct.set_element(0, 1)
    for i in range(1, n):
        # num = multiply(num, i)
        ct.set_element(i, multiply(ct.get_element(i - 1), i))
    return ct