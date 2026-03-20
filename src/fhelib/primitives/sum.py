import numpy as np
""""
Implemetation of basic component wise sum    
"""

# sum ct naive O(n)
def sum_naive(ct):
    result_ct = np.empty(ct.size , dtype=complex)
    roller_ct = np.empty(ct.size , dtype=complex)
    np.copyto(result_ct, ct)
    np.copyto(roller_ct, ct)
    for i in range(ct.size - 1):
        roller_ct = np.roll(roller_ct, 1)
        result_ct = result_ct + roller_ct
    return result_ct

# sum ct O(lg(n))
def sum(ct):
    #TODO I hard coded r = 15, we need to dynamically implement r
    r = 15
    ctcp = np.empty(ct.size, dtype=complex)
    np.copyto(ctcp, ct)
    i = 0
    while i < (r-1): # TODO make sure this range is actually correct
        ctcp = ctcp + np.roll(ct, 2 ** i)
        i *= 2
    return ctcp