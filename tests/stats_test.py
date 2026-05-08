from fhelib import Ciphertext
from fhelib.stats import vector_mean
from fhelib.primitives import reset, get_counts
import numpy as np 


# rough adult U.S. bosy weight distibution 
weights = np.random.normal(loc=185, scale=48, size=(2 ** 15))

ct = Ciphertext(weights)

true_mean = np.mean(ct)
reset()
mean = vector_mean(ct)

print(f'True mean:{true_mean}\nFHE mean:{mean}')
print(get_counts())