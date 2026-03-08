# libraries
import numpy as np

# default ciphertext size n = N/2 (as noted in PiFHE hackmd)
r = 15          # 16-1
n = 2 ** r      # 2^(r)
k = int()       # roll key 

# representation of cipertexts ct=Enc(z*)
ptct = np.empty(n, dtype=complex) # prototype ciphertext 
a = np.array(ptct)
b = np.array(ptct)
ct2n = np.full(2/n) # ct containing multiplicative inverse of size (allows division by number of elements)

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
    

""" # 4 moves
        a+b                   # addition
        a*b                   # component | element-wise multiplication 
        np.roll(a,k)          # cycle | shift | roll ct elements by k indeces
        np.conjugate(a)       # complex conjugation

    # implied moves
        q = np.array(ptct)                      # create a new empty ct named q 
        b = np.array(a)                         # creates a new ct b as a copy of a
        b = np.copy(a)                          # copy a into b, assumes b has been declared
        ct0 = np.zeroes(n, dtype=np.complex)    # ct containing zeroes
        ct1 = np.ones(n, dtype=np.complex)      # ct containing ones
        ct2n = np.full(2/n)                     # ct containing mutliplicative inverse of size
"""

# region concrete implementations

''' intra-sum naive O(n)
    returns ct with every element containing sum 
'''
def sum_naive(ct):
    ct_sum = np.array(ct)
    for i in range(n-1):
        ct_sum += np.roll(ct, 1)
    return ct_sum

''' intra-sum O(lg(n))
    returns ct with every element containing sum 
'''
def sum(ct):
    ct_sum = np.copy(ct)
    i = 0
    while i < (r): # TODO make sure this range is actually correct
        ct_sum += np.roll(ct, i)
        i *= 2
    return ct_sum

''' dot product
    returns ct with every element containing 
    the dot product of a and b
'''
def dotpr(cta, ctb):
    return sum(cta * ctb) 

# complex inner product
def complex_ip(ct):
    # TODO implement comp ip
    return

# mean
def mean(ct):
    return sum(ct) * ct2n   # returns ct with every element containing mean

# endregion

# region functions we assume work 
""" but have not been implemented 
    as a sequence of the four moves
    (technically illegal)

    np.real(ct)             # return array containing only real component of each z in ct
    np.imag(ct)             # "                            imaginary "
    np.emath.sqrt(ct)       # take square root of each complex element
    np.sign(ct)             # lreturn x / abs(x) | 0 if x==0

                            # approximate with polynomials | taylor series
"""

# sign only reals
def sign_asmpt(ct):
    return np.sign(np.real(ct))

# sign as described in hackmd
def sign_asmpt_hmd(ct):
    real = np.real(ct)
    sign = np.zeroes(n, dtype=np.complex)
    for i in range(n):
        if (ct[i] > 0):
            sign[i] = 1
    return sign

# compare
def cmp_asmpt(ct):
    #TODO implement compare
    return

def mod_asmpt(ct):
    #TODO implement mod
    return
    
# endregion