""""
Implemetation of cycle    
"""

def cycle(step: int, ct: list):
    copy = ct
    last_index = len(ct) - 1
    for j in range(step):
        temp = copy[last_index]
        for i in range(len(ct)):
            copy[last_index - i] = copy[last_index  - i - 1]
        copy[0] = temp
    return copy