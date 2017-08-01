import unittest
from unittest.mock import patch, call, Mock


from libs.storage import Storage


class CreateTest(unittest.TestCase):

    @patch('libs.storage.Path')
    def test(self, Path_mock):
        instance = Storage('/home/user/pictures', ('*.jpg', '*.png'))
        Path_mock.assert_called_once_with('/home/user/pictures')
        pass


class Test(unittest.TestCase):

    def setUp(self):
        self.instance = Storage('/home/user/pictures', ('*.jpg', '*.png'))

    @patch('libs.storage.Image.open')
    @patch('libs.storage.Path.glob')
    def test_first_get_current(self, glob_mock, open_mock):
        glob_mock.side_effect = (('5.jpg', '3.jpg', '1.jpg'), ('2.png', '4.png', '6.png'))
        img_mock = Mock(name='img_mock', spec=['load'])
        open_mock.return_value = img_mock

        result = self.instance.get_current()

        glob_mock.assert_has_calls((call('*.jpg'), call('*.png')))
        open_mock.assert_called_once_with('1.jpg')
        img_mock.load.assert_called_once_with()
        self.assertEqual(result, img_mock)

    @patch('libs.storage.Path.glob')
    def test_first_get_current(self, glob_mock):
        glob_mock.side_effect = ((), ())

        result = self.instance.get_current()

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
