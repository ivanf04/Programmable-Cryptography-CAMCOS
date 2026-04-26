import numpy as np


# TODO: can we make a contructor with a list of data points as a parameter
# Cypher text class
class Ciphertext(np.ndarray):

    def __new__(cls, length):  # __new__ instead of __init__ (ndarray requires this)
        obj = np.zeros(length, dtype=complex).view(
            cls
        )  # create array, cast to Ciphertext type
        obj.level = 15
        return obj  # return it directly

    # default ciphertext size n = N/2 (as noted in PiFHE hackmd)
    def __init__(self):
        r = 15  # 16-1
        n = 2**r  # 2^(16-1)
        self.ct = np.zeros(n, dtype=complex)
        self.level = 15

    def __init__(self, length):
        """
        This initializes the ct to have a default length of N / 2 and elements equal to 0 (???)
        TODO: find out how to intitialize all elements to zero
        """
        if not self._is_power_of_2(length):
            raise ValueError(f"Length must be a power of two, got {length}")

        self.ct = np.zeros(length, dtype=complex)
        self.level = 15

    def __array_finalize__(self, obj):
        """Called whenever numpy creates a new view of this array."""
        if obj is None:
            return
        # inherit level from parent array if it has one, else default
        self.level = getattr(obj, "level", 15)

    # check if a number is a power of two
    def _is_power_of_2(self, length):
        return length > 0 and (length & (length - 1)) == 0

    # only use this for testing
    def set_element(self, index, value):
        self[index] = value

    def get_element(self, index):
        return self[index]

    def set_level(self, value):
        self.level = value

    def get_level(self):
        return self.level

    def __str__(self):
        return super().__str__()

    def negative_ones(self):
        for i in range(self.size):
            self.set_element(i, -1)
