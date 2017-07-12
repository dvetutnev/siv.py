import unittest

import sys
print(sys.path)
#import siv_modules
from siv_modules import renderer


class Fake(unittest.TestCase):

    def test_fake(self):
        self.assertEqual(7, 7)

    def test_import(self):
        sum = renderer.Sum(None, True, None, False)
        self.assertTrue(sum.left_done)
        self.assertFalse(sum.right_done)

if __name__ == '__main__':
    unittest.main()
