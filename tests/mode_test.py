from fhelib import Ciphertext
from fhelib.stats.mode import mode
import unittest

""" Test file for mode.py

"""
class Mode_Test(unittest.TestCase):

    def test_int(self):
        values = [2, 2, 1, -2]
        print(values)
        a = Ciphertext(4)
        for idx, val in enumerate(values):
            a.set_element(idx, val)
        print(a)

        print("=" * 50)
        print(f"Mode test on {values}")
        print("Expected output: 2.+0.j")
        print("=" * 50)

        result = mode(a)
        print(f"Result: {result}")

        self.assertEqual(result, 2+0j)

if __name__ == '__main__':
    unittest.main()