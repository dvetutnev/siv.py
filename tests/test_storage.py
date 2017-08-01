import unittest
from unittest.mock import patch, call, Mock

from libs.storage import Storage, Path


class CreateTest(unittest.TestCase):

    @patch('libs.storage.Path', name='Path_mock', autospec=True, sec_set=True)
    def test(self, Path_mock):
        instance = Storage('/home/user/pictures', ('*.jpg', '*.png'))
        Path_mock.assert_called_once_with('/home/user/pictures')
        del instance
        pass


class Test(unittest.TestCase):

    def setUp(self):
        with patch('libs.storage.Path', name='Path_mock', autospec=True, spec_set=True) as Path_mock:
            self.path_mock = Mock(name='path_mock', spec_set=Path)
            Path_mock.return_value = self.path_mock
            self.instance = Storage('/home/user/pictures', ('*.jpg', '*.png'))

    def test_first_get_current_None(self):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = ((), ())

        result = self.instance.get_current()

        self.assertIsNone(result)
        glob_mock.assert_has_calls((call('*.jpg'), call('*.png')))

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_first_get_current(self, Image_mock):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = (('5.jpg', '3.jpg', '1.jpg'), ('2.png', '4.png', '6.png'))
        img_mock = Mock(name='img_mock', spec_set=['load'])
        Image_mock.open.return_value = img_mock

        result = self.instance.get_current()

        self.assertEqual(result, img_mock)
        glob_mock.assert_has_calls((call('*.jpg'), call('*.png')))
        Image_mock.open.assert_called_once_with('1.jpg')
        img_mock.load.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
