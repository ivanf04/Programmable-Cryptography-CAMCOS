import numpy as np
from fhelib.ciphertext import Ciphertext
from fhelib.primitives import _counts

"""
Basic component wise addition of two cypher texts
using np.add
"""


def add(a, b):
    _counts["add"] += 1

    # ensure a is always Ciphertext
    if not isinstance(a, Ciphertext) and isinstance(b, Ciphertext):
        a, b = b, a

    if isinstance(b, Ciphertext):
        level = min(a.get_level(), b.get_level())  # no level cost, but must match
    elif isinstance(b, (int, float, np.ndarray)):
        level = a.get_level()  # adding scalar/plaintext costs nothing

    result = np.add(a, b)
    result.set_level(level)
    return result
