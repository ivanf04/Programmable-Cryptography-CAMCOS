"""
simple test of factorial
"""

from fhelib.lowlevel.factorial import factorial
import numpy as np

nums = [0, 1, 2, 3, 4, 5, 6, 7]
expected = [1, 1, 2, 6, 24, 120, 720, 5040]
results = factorial(8)

# for i in range(len(nums)):
#     results[i] = factorial(nums[i])

print(f"Factorial test")
print("=" * 50)
print(f"Input: {nums}")
print(f"Expected putput: {expected}")
print(f"output:{results}")