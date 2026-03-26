from ciphertext import Ciphertext
"""
Creates a copy of the given cyphertext and takes the complex
conjugate of each element. 
Returns the conjugated copy
"""
def conjugate(a: Ciphertext):
    b = a.copy()
    for element in b:
       element.conjugate()
    return b
     