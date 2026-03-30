import numpy as np

#Cypher text class 
class Ciphertext(np.ndarray):

    def __new__(cls, length):        # __new__ instead of __init__ (ndarray requires this)
        obj = np.zeros(length, dtype=complex).view(cls)  # create array, cast to Ciphertext type
        return obj                   # return it directly

    # default ciphertext size n = N/2 (as noted in PiFHE hackmd)
    def __init__(self): 
        r = 15          # 16-1
        n = 2 ** r      # 2^(16-1)
        self.ct = np.zeros(n, dtype=complex)

    #TODO make the constructor return itself, right now we need to use Ciphertext.ct to acces np funcitons 
    def __init__(self, length):
        """
        This initializes the ct to have a default length of N / 2 and elements equal to 0 (???)
        TODO: find out how to intitialize all elements to zero 
        """
        if not self._is_power_of_2(length):
            raise ValueError(f"Length must be a power of two, got {length}")
             
        self.ct = np.zeros(length, dtype=complex) 
    
    # check if a number is a power of two
    def _is_power_of_2(self, length):
        return length > 0 and (length & (length - 1)) == 0

    
    #only use this for testing 
    def set_element(self, index, value):
        self[index] = value
    
    def get_element(self, index):
        return self[index]
    
    def __str__(self):
        return super().__str__()