import numpy as np
""""
Implemetation of basic component wise sum    
"""

def intravector_sum_naive(ct):
    result_ct = np.empty(ct.size, dtype=complex)
    roller_ct = np.empty(ct.size, dtype=complex)
    np.copyto(result_ct, ct)
    np.copyto(roller_ct, ct)
    
    for i in range(ct.size - 1):
        roller_ct = np.roll(roller_ct, 1)  # cycle by 1 each time
        result_ct = result_ct + roller_ct  # add to accumulator
    
    return result_ct[0]


def intravector_sum(ct: np.ndarray) -> np.ndarray:
    r = ct.size // 2  # N/2 slots, so log(N/2) steps
    ct_copy = np.empty(ct.size, dtype=complex)
    np.copyto(ct_copy, ct)
    
    i = 0
    while i < (r - 1):
        ct_copy = ct_copy + np.roll(ct_copy, -(2 ** i))
        i = 2 * i + 1
    
    return ct_copy[0]

def intravector_partsum(ct: np.ndarray, n: int) -> np.ndarray:
    ct_copy = np.empty(ct.size, dtype=complex)
    np.copyto(ct_copy, ct)
    
    num_blocks = ct.size // n
    for b in range(num_blocks):
        block = ct[b*n:(b+1)*n].copy()
        # sum within this block
        i = 0
        while i < (n - 1):
            block = block + np.roll(block, -(2**i))
            i = 2 * i + 1
        ct_copy[b*n:(b+1)*n] = block
    
    return ct_copy