from fhelib import Ciphertext
import unittest

""" simple example 
    to ensure testing within vscode works
"""

class Test_Test(unittest.TestCase):

    ct = Ciphertext(32)
    print(ct)

    def test_foo(self):
        self.assertEqual(2, 1+1)

if __name__ == '__main__':
    unittest.main()