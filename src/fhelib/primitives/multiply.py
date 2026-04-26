import numpy as np
from fhelib.ciphertext import Ciphertext
from fhelib.primitives import _counts


"""
Multiplication Levels:
ct a * ct b , level = min(a-1,b-1)
ct a * ar b , level = a-1
ct a * int b , level = a
ct a * float b , level = a - 1
ct a * ct b * ct c * ct d ... , level = min(level) - ceil ( log2 ( n terms ) )
 """


def multiply(a: Ciphertext, b: Ciphertext):
    """
    Basic component wise multiplication of two cypher texts
    using np.multiply
    """
    _counts["multiply"] += 1

    # ensure a is always Ciphertext
    if not isinstance(a, Ciphertext) and isinstance(b, Ciphertext):
        a, b = b, a

    if isinstance(b, Ciphertext):
        level = min(a.get_level() - 1, b.get_level() - 1)
    elif isinstance(b, int):
        level = a.get_level()
    elif isinstance(b, (float, np.ndarray)):
        level = a.get_level() - 1

    result = np.multiply(a, b)
    result.set_level(level)
    return result


def chain_multiply(terms) -> Ciphertext:
    """
    Handle levels of chained multiplication
    """
    _counts["multiply"] += len(terms) - 1  # n-1 multiplications

    if not any(isinstance(t, Ciphertext) for t in terms):
        raise TypeError("At least one term must be a Ciphertext")

    ct_terms = [t for t in terms if isinstance(t, Ciphertext)]
    min_level = min(t.get_level() for t in ct_terms)
    n_ct = len(ct_terms)

    while len(terms) > 1:
        pairs = list(zip(terms[::2], terms[1::2]))
        next_terms = [multiply(a, b) for a, b in pairs]
        if len(terms) % 2 == 1:
            next_terms.append(terms[-1])
        terms = next_terms

    result = terms[0]
    result.set_level(min_level - math.ceil(math.log2(n_ct)) if n_ct > 1 else min_level)
    return result
