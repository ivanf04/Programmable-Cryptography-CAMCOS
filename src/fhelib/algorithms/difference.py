from fhelib import Ciphertext
"""
Difference method, given to ciphertexts A and B,
 return ciphertext D with elements D_i = (A_i - B_i)
 prerequiste: gif (good if)? 
"""
"""
Precondtion: A and B must be same length 
Postcondition: D will conation difference of elements in A and B 
"""
def difference(a: Ciphertext, b: Ciphertext) -> Ciphertext:
    # TODO raise a length mismatch if A and B are of different lengths
    len = b.size
    d = Ciphertext(len)
    for i in range(len): 
      d[i] = a[i] - b[i]
    return d