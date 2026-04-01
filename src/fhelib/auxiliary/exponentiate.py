from fhelib import Ciphertext
import numpy as np

def exponentiate(ct: Ciphertext, n: int = 10) -> Ciphertext:
    """
    Approximates e^x for each element in ciphertext.
    
    Intended implementation: Taylor series expansion
    
    Note from hackmd: 
    - Higher number n terms for more accuracy, multiplications
    - Input should lie in a restricted interval
    
    TODO: replace np.exp with Taylor series implementation
    """
    return np.exp(np.real(ct)) 