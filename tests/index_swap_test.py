from fhelib.ciphertext import Ciphertext
from fhelib.auxiliary.index_swap import index_swap

# swap indices 1 and 3 in [1,2,3,4,5,6,7,8]
# expect [1,4,3,2,5,6,7,8]

v = Ciphertext(8)
for idx, val in enumerate([1,2,3,4,5,6,7,8]):
    v.set_element(idx, val)

print(f"v before swap: {v}")
result = index_swap(v, 1, 3)
print(f"v after swap indices 1 and 3: {result}")
print(f"expected:                     [1,4,3,2,5,6,7,8,...]")