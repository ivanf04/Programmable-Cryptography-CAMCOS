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

    alevel = a.get_level() if isinstance(a, Ciphertext) else 15
    blevel = b.get_level() if isinstance(b, Ciphertext) else 15
    level = min((alevel - 1), (blevel - 1))

    result = np.multiply(a, b)
    result.set_level(level)

    return result
