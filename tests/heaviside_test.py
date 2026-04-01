from fhelib import Ciphertext
from fhelib.lowlevel.sign import sign_heaviside
""""
testing the heaviside implementaionof sign
input:
    a = [5,2,6,5]
expected output: 
    sign(a,0,1,5) = [0.5,0,1,0.5]
"""
print('=' * 50)
print('Test of heaviside-type function using sign')
print('=' * 50)
a = Ciphertext(4)
a.set_element(0,5)
a.set_element(1,2)
a.set_element(2,6)
a.set_element(3,5)
expected_value = [0.5, 0, 1, 0.5]
print(f"Input CT:\n{a}")
print("Method call: sign_heaviside(a, 0, 1, 5)")
print(f"Expected value (approximate):\n{expected_value}")
print('=' * 50)
s = sign_heaviside(a, 0, 1, 5)
print(f"Output:\n{s}")