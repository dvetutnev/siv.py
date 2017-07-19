import unittest
from unittest.mock import Mock

from lib import renderer


class Fake(unittest.TestCase):
    def test_fake(self):
        mock = Mock()
        list = [None, 1, 2, 3]
        current = list.index(2)
        def get_current(idx=0):
            return list[current + idx]
        mock.side_effect = get_current
        print(mock(-1))
        print(mock())
        pass

    def test_import(self):
        sum = renderer.Sum(None, True, None, False)
        self.assertTrue(sum.left_done)
        self.assertFalse(sum.right_done)


if __name__ == '__main__':
    unittest.main()
