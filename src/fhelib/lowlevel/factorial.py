"""
A simple factorial implementation in FHE
Goal: create a ciphertext with elemets of x! for every element x. 
This will be used to approxiate the exponential function. With testing we will know how long the ct will need to be 
"""
import numpy as np 
import math
from fhelib.primitives import multiply
from fhelib import Ciphertext

def factorial(n:int):
    """
    Generate a ciphertext of length n, with each element as n!
    Since we can create constants we know, we can calculate n! non-fhe and encrypt it 

    :param n: the length of the output ciphertext with n! in as the nth element

    :return ct: Ciphertext with length n containing n!
    """
    ct = Ciphertext(n)
    n_factorial = math.factorial(n)
    for i in range(n):
        # num = multiply(num, i)
        ct.set_element(i, n_factorial)
    return ct