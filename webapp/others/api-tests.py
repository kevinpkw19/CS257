'''
   primecheckertests.py
   Jeff Ondich, 9 May 2012
   Updated for use in a lab exercise, 4 Nov 2013
'''

import apichecker
import unittest


class ApiTester(unittest.TestCase):
    def setUp(self):
        # self.prime_checker = primechecker.PrimeChecker(100)
        self.apichecker= apichecker.get_search_results()

    def tearDown(self):
        pass

    def test_empty(self):
        self.assertRaises(ValueError,self.apichecker)

    def test_ascii(self):
        self.assertRaises(TypeError,self.apichecker)

    def test_return_type(self):
        self.assertRaises(TypeError,self.apichecker)

if __name__ == '__main__':
    unittest.main()
