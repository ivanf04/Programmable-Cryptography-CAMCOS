import numpy as np

#Cypher text class 
class Cypher_Text:

    # default ciphertext size n = N/2 (as noted in PiFHE hackmd)
    r = 15          # 16-1
    n = 2 ** r      # 2^(16-1)
    
    def __init__(self, length=n):
        """
        This initializes the ct to have a default length of N / 2 and elements equal to 0 (???)
        TODO: find out how to intitialize all elements to zero 
        """
        self.ct = np.zeros(length, dtype=complex) 
    
    #only use this for testing 
    def set_element(self, index, value):
        self.ct[index] = value
    
    def get_element(self, index):
        return self.ct[index]
    
    def __str__(self):
        return str(self.ct)