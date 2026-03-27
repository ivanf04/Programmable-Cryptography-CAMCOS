from fhelib.ciphertext import Ciphertext
"""
Creates a copy of the given cyphertext and takes the complex
conjugate of each element. 
Returns the conjugated copy
"""
def conjugate(a: Ciphertext):
    b = a.copy()
    for i, element in enumerate(b):
      b[i] = element.conjugate()
    return b
     