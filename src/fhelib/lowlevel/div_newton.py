"""
FHE legal division using Newton's Method
"""
from fhelib.primitives.multiply import multiply
from fhelib.primitives.add import add
from fhelib.ciphertext import Ciphertext

"""
Tolerance check is temporary, 
we need to test and find a number of sufficeint interations to hardcode into the program 
"""
def div_newton(a: Ciphertext, x_0,  tol= 10e-10):
    count = 0
    ct_negative1 = Ciphertext(a.size)
    ct_negative1.negative_ones()
    x_n = add(multiply(2, a), multiply((multiply(multiply(x_0, x_0), a)), ct_negative1))
    
    # TODO: create a nested loop to take the approximation of elements individually
    while(abs(x_n - x_0) < tol):
            x_0 = x_n
            x_n = add(multiply(2, x_0), multiply((multiply(multiply(x_0, x_0), a)), ct_negative1))
            count += 1
    return x_n, count



    