import numpy as np
from fhelib.ciphertext import Ciphertext

"""
Out-of-spec implementation of division 

using numpy division as a placeholder for higher complexity functions
returns a ciphetext containing ai/bi in each corresponding index

TODO: discuss how to implement polynomial estimation with math theory team.
"""

def il_division(a:Ciphertext, b:Ciphertext):
    return np.divide(a,b)