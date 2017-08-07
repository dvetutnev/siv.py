import unittest
from unittest.mock import patch, call, Mock, ANY


from libs.storage import Storage, Path, Image


class CreateTest(unittest.TestCase):

    @patch('libs.storage.Path', name='Path_mock', autospec=True, sec_set=True)
    def test(self, Path_mock):
        instance = Storage('/home/user/pictures', ['*.jpg', '*.png'])
        Path_mock.assert_called_once_with('/home/user/pictures')
        del instance
        pass


class TestFirstUse(unittest.TestCase):

    def setUp(self):
        with patch('libs.storage.Path', name='Path_mock', autospec=True, spec_set=True) as Path_mock:
            self.path_mock = Mock(name='path_mock', spec_set=Path)
            Path_mock.return_value = self.path_mock
            self.instance = Storage('/home/user/pictures', ['*.jpg', '*.png'])

    def test_get_0_None(self):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = [[], []]

        result = self.instance.get(0)

        self.assertIsNone(result)
        glob_mock.assert_has_calls([call('*.jpg'), call('*.png')])

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_0_Normal(self, Image_mock):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = [['3.jpg', '1.jpg'], ['2.png', '4.png']]

        img_mock = Mock(name='img_mock', spec_set=Image.Image)
        Image_mock.open.return_value = img_mock
        expect_open = [call.open('1.jpg')]

        result = self.instance.get(0)

        Image_mock.assert_has_calls(expect_open)
        img_mock.load.assert_called_once_with()
        self.assertEqual(result, img_mock)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_0_AllBadImage(self, Image_mock):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = [['3.jpg', '1.jpg'], ['2.png', '4.png']]

        Image_mock.open.side_effect = FileNotFoundError('Mock: not found')
        expect_open = [call.open('1.jpg'), call.open('2.png'), call.open('3.jpg'), call.open('4.png')]

        result = self.instance.get(0)

        Image_mock.assert_has_calls(expect_open)
        self.assertIsNone(result)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_0_SkipBadImage(self, Image_mock):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = [['3.jpg', '1.jpg'], ['2.png', '4.png']]

        img_bad = Mock(name='img_mock', spec_set=Image.Image)
        img_bad.load.side_effect = OSError('Mock: format invalid')
        img_normal = Mock(name='img_normal', spec_set=Image.Image)

        def _open(fname):
            if not hasattr(_open, 'count'):
                _open.count = 0
                raise FileNotFoundError('Mock: ' + fname + ' not found')
            if _open.count == 0:
                _open.count = 1
                return img_bad
            if _open.count == 1:
                return img_normal
        Image_mock.open.side_effect = _open
        expect_open = [call.open('1.jpg'), call.open('2.png'), call.open('3.jpg')]

        result = self.instance.get(0)

        Image_mock.assert_has_calls(expect_open)
        img_bad.load.assert_called_once_with()
        img_normal.load.assert_called_once_with()
        self.assertEqual(result, img_normal)


if __name__ == '__main__':
    unittest.main()
