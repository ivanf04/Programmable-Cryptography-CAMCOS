from src.fhelib.primitives.sum import sum_naive
import numpy as np 
import openfhe

a = np.empty(4, dtype= int)
# b = np.empty(4, dtype= int)

# print(a, b)

for i in range (4):
    a[i] = i + 1
print(a)

c = sum_naive(a)
print(c)