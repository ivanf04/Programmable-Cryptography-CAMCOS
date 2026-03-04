import fhe_lib
import numpy as np 

a = np.empty(4, dtype= int)
# b = np.empty(4, dtype= int)

# print(a, b)

for i in range (4):
    a[i] = i + 1
print(a)

c = fhe_lib.sum_naive(a)
print(c)