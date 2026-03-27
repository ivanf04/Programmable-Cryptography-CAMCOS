import numpy as np
from fhelib.ciphertext import Ciphertext
"""
Basic component wise multiplication of two cypher texts
using np.multiply
"""

def multiply(a: Ciphertext, b: Ciphertext):
    return np.multiply(a,b); 
    
