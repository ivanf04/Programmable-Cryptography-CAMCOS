from fhelib import Ciphertext
import numpy as np 


# rough adult U.S. bosy weight distibution 
weights = np.random.normal(loc=185, scale=48, size=(2 ** 15))

ct = Ciphertext(weights)

print(ct.size)