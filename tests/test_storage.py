import unittest
from unittest.mock import patch, call, Mock, ANY


from libs.storage import Storage, Path, Image


class CreateTest(unittest.TestCase):

    @patch('libs.storage.Path', name='Path_mock', autospec=True, sec_set=True)
    def test(self, Path_mock):
        instance = Storage('/home/user/pictures', ['*.jpg'])
        Path_mock.assert_called_once_with('/home/user/pictures')
        del instance


class TestSomeExtensions(unittest.TestCase):

    @patch('libs.storage.Path', name='Path_mock', autospec=True, sec_set=True)
    def test(self, Path_mock):
        path_mock = Mock(name='path_mock', spec_set=Path)
        Path_mock.return_value = path_mock

        path_mock.glob.side_effect = [[], [], []]
        expect_glob = [call.glob('*.jpg'), call.glob('*.png'), call.glob('*.bmp')]

        instance = Storage('/home/user/pictures', ['*.jpg', '*.png', '*.bmp'])
        instance.get(0)

        path_mock.assert_has_calls(expect_glob)


class TestFirstUse(unittest.TestCase):

    def setUp(self):
        with patch('libs.storage.Path', name='Path_mock', autospec=True, spec_set=True) as Path_mock:
            self.path_mock = Mock(name='path_mock', spec_set=Path)
            Path_mock.return_value = self.path_mock
            self.instance = Storage('/home/user/pictures', ['*.jpg'])

    def test_get_0_None(self):
        path = self.path_mock
        path.glob.return_value = []
        expect_glob = [call.glob('*.jpg')]

        result = self.instance.get(0)

        self.assertIsNone(result)
        path.assert_has_calls(expect_glob)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_0_Normal(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['2.jpg', '0.jpg', '1.jpg', '3.jpg']

        img = Mock(name='0.jpg', spec_set=Image.Image)
        Image_mock.open.return_value = img
        expect_open = [call.open('0.jpg')]

        result = self.instance.get(0)

        Image_mock.assert_has_calls(expect_open)
        img.load.assert_called_once_with()
        self.assertEqual(result, img)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_0_AllBadImage(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['2.jpg', '0.jpg', '1.jpg', '3.jpg']

        Image_mock.open.side_effect = FileNotFoundError('Mock: not found')
        expect_open = [call.open('0.jpg'), call.open('1.jpg'), call.open('2.jpg'), call.open('3.jpg')]

        result = self.instance.get(0)

        Image_mock.assert_has_calls(expect_open)
        self.assertIsNone(result)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_0_SkipBadImage(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['2.jpg', '0.jpg', '1.jpg', '3.jpg']

        img_bad = Mock(name='img_bad', spec_set=Image.Image)
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
        expect_open = [call.open('0.jpg'), call.open('1.jpg'), call.open('2.jpg')]

        result = self.instance.get(0)

        Image_mock.assert_has_calls(expect_open)
        img_bad.load.assert_called_once_with()
        img_normal.load.assert_called_once_with()
        self.assertEqual(result, img_normal)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_previous(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['2.jpg', '0.jpg', '1.jpg', '3.jpg']

        Image_mock.open.return_value = Mock(name='0.jpg', spec_set=Image.Image)
        expect_open = [call.open('0.jpg')]

        instance = self.instance
        instance.get(0)

        self.assertIsNone(instance.get(-1))

        self.assertEqual(path.glob.call_count, 1)
        Image_mock.assert_has_calls(expect_open)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_next(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['2.jpg', '0.jpg', '1.jpg', '3.jpg']

        img_0 = Mock(name='0.jpg', spec_set=Image.Image)
        img_1 = Mock(name='1.jpg', spec_set=Image.Image)
        img_2 = Mock(name='2.jpg', spec_set=Image.Image)
        img_3 = Mock(name='3.jpg', spec_set=Image.Image)
        Image_mock.open.side_effect = [img_0, img_1, img_2, img_3]
        expect_open = [call.open('0.jpg'), call.open('1.jpg'), call.open('2.jpg'), call.open('3.jpg')]

        instance = self.instance
        instance.get(0)

        self.assertEqual(instance.get(1), img_1)
        self.assertEqual(instance.get(2), img_2)
        self.assertEqual(instance.get(3), img_3)
        self.assertIsNone(instance.get(4))

        self.assertEqual(path.glob.call_count, 1)
        Image_mock.assert_has_calls(expect_open)


class TestNextUse(unittest.TestCase):

    def setUp(self):
        with patch('libs.storage.Path', name='Path_mock', autospec=True, spec_set=True) as Path_mock:
            self.path_mock = Mock(name='path_mock', spec_set=Path)
            Path_mock.return_value = self.path_mock
            self.instance = Storage('/home/user/pictures', ['*.jpg'])

        instance = self.instance
        path = self.path_mock
        path.glob.return_value = ['0.jpg', '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']
        for _ in range(3):
            instance.get(0)
            instance.step_next()
        path.glob.return_value = None
        path.glob.side_effect = None
        path.reset_mock()

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_0(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['0.jpg', '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']

        img = Mock(name='3.jpg', spec_set=Image.Image)
        Image_mock.open.return_value = img

        result = self.instance.get(0)

        self.assertEqual(path.glob.call_count, 1)
        Image_mock.assert_has_calls([call.open('3.jpg')])
        self.assertEqual(result, img)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_next(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['0.jpg', '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']

        img_0 = Mock(name='3.jpg', spec_set=Image.Image)
        img_1 = Mock(name='4.jpg', spec_set=Image.Image)
        img_2 = Mock(name='5.jpg', spec_set=Image.Image)
        img_3 = Mock(name='6.jpg', spec_set=Image.Image)
        Image_mock.open.side_effect = [img_0, img_1, img_2, img_3]
        expect_open = [call.open('3.jpg'), call.open('4.jpg'), call.open('5.jpg'), call.open('6.jpg')]

        instance = self.instance
        instance.get(0)

        self.assertEqual(instance.get(1), img_1)
        self.assertEqual(instance.get(2), img_2)
        self.assertEqual(instance.get(3), img_3)
        self.assertIsNone(instance.get(4))

        self.assertEqual(path.glob.call_count, 1)
        Image_mock.assert_has_calls(expect_open)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_previous(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['0.jpg', '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']

        img_0 = Mock(name='3.jpg', spec_set=Image.Image)
        img_1 = Mock(name='2.jpg', spec_set=Image.Image)
        img_2 = Mock(name='1.jpg', spec_set=Image.Image)
        img_3 = Mock(name='0.jpg', spec_set=Image.Image)
        Image_mock.open.side_effect = [img_0, img_1, img_2, img_3]
        expect_open = [call.open('3.jpg'), call.open('2.jpg'), call.open('1.jpg'), call.open('0.jpg')]

        instance = self.instance
        instance.get(0)

        self.assertEqual(instance.get(-1), img_1)
        self.assertEqual(instance.get(-2), img_2)
        self.assertEqual(instance.get(-3), img_3)
        self.assertIsNone(instance.get(-4))

        self.assertEqual(path.glob.call_count, 1)
        Image_mock.assert_has_calls(expect_open)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_step_next_limit(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['0.jpg', '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']

        img_0 = Mock(name='3.jpg', spec_set=Image.Image)
        img_1 = Mock(name='4.jpg', spec_set=Image.Image)
        img_2 = Mock(name='5.jpg', spec_set=Image.Image)
        img_3 = Mock(name='6.jpg', spec_set=Image.Image)
        Image_mock.open.side_effect = [img_0, img_1, img_2, img_3, img_3]
        expect_open = [
            call.open('3.jpg'), call.open('4.jpg'), call.open('5.jpg'), call.open('6.jpg'), call.open('6.jpg')
        ]

        instance = self.instance
        for _ in range(3):
            instance.get(0)
            instance.step_next()
        result_1 = instance.get(0)
        instance.step_next()
        result_2 = instance.get(0)

        Image_mock.assert_has_calls(expect_open)
        self.assertEqual(result_1, img_3)
        self.assertEqual(result_2, img_3)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_unlink_current(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['0.jpg', '1.jpg', '2.jpg', '4.jpg', '5.jpg', '6.jpg']

        img = Mock(name='4.jpg', spec_set=Image.Image)
        Image_mock.open.return_value = img

        result = self.instance.get(0)

        self.assertEqual(path.glob.call_count, 1)
        Image_mock.assert_has_calls([call.open('4.jpg')])
        self.assertEqual(result, img)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_unlink_previous(self, Image_mock):
        path = self.path_mock
        path.glob.return_value = ['0.jpg', '1.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg']

        img = Mock(name='3.jpg', spec_set=Image.Image)
        Image_mock.open.return_value = img

        result = self.instance.get(0)

        self.assertEqual(path.glob.call_count, 1)
        Image_mock.assert_has_calls([call.open('3.jpg')])
        self.assertEqual(result, img)


if __name__ == '__main__':
    unittest.main()
