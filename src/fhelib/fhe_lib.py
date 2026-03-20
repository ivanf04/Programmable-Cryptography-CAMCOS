import numpy as np

"""
This file is being depricated, TODO: move  and implement the remainig methods 
in thier corresponding directories 
"""


""" # 4 moves
        a+b                   # addition
        a*b                   # component | element-wise multiplication 
        np.roll(a,k)          # cycle | shift | roll ct elements by k indeces
        np.conjugate(a)       # complex conjugation

    # implied moves
        np.copyto(a,b)                          # copy a to b (both contain a copy of what was in b)
        ct0 = np.zeroes(n, dtype=np.complex)    # ct containing zeroes
        ct1 = np.ones(n, dtype=np.complex)      # ct containing ones
"""

# region concrete implementations


# dot product
def dotpr(cta, ctb):
    dpct = cta * ctb
    return sum(dpct)

# complex inner product
def complex_ip(ct):
    # TODO implement comp ip
    return

# endregion

# region functions we assume work    
""" but have not been implemented 
    as a sequence of the four moves

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
    n = ct.size()
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

def mean_asmpt(ct):
    #TODO validate how mean is returned
    #TODO implement mean
    return

# endregion