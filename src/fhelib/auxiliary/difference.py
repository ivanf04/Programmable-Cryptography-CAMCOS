from fhelib import Ciphertext
from fhelib.primitives.add import add

def difference(a: Ciphertext, b: Ciphertext) -> Ciphertext:
    """
    Difference method, for ciphertexts A and B

    Raises: ValueError if a and b have different sizes
    
    Returns: Ciphertext where D_i = A_i - B_i for all i 
    """
    
    if a.size != b.size:
        raise ValueError(f"Length mismatch: a has {a.size} elements, b has {b.size} elements")
    
    d = add(a, -b)

    return d