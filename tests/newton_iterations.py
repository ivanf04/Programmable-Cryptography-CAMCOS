"""
file to test the number of iterations needed to converge on a data set
"""

import random 
from fhelib.ciphertext import Ciphertext
from fhelib.lowlevel.div_newton import div_newton

# create ct of normally distibuted human weights, and the true inverse
weights = []
while len(weights) < 16: 
    w = random.gauss(170, 40) # mean=170, stddev=40
    if 50 <= w <= 500:
        weights.append(w)
ct_w = Ciphertext(16)
for i in range(ct_w.size):
    ct_w.set_element(i, weights[i])
print(f"Input list of normally distributed weights:\n{weights}")

inverse_w = [1/x for x in weights]
print(f"The true inverse of the data:\n{inverse_w}")

# create ct for inital guess 10e-10
# x_0 = Ciphertext(16)
# for i in range(16):
#     x_0.set_element(i, 10e-10)
x_0 = 10e-10

# use FHE newtons to find approximate 1/x
fhe_inverse = div_newton(ct_w, x_0)

error = (inverse_w - fhe_inverse)**2

print(f"FHE legal inverse using newton's method:\n{fhe_inverse}")
print(f"Mean squared error:\n{error}")