from fhelib import Ciphertext
import numpy as np

def fhe_max(a: Ciphertext):
    return np.max(a) # not yet legal in code
                     # have legal moves in writeup