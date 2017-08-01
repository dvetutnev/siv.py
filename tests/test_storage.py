import unittest
from unittest.mock import patch, call, Mock


from libs.storage import Storage, Path, Image


class CreateTest(unittest.TestCase):

    @patch('libs.storage.Path', name='Path_mock', autospec=True, sec_set=True)
    def test(self, Path_mock):
        instance = Storage('/home/user/pictures', ['*.jpg', '*.png'])
        Path_mock.assert_called_once_with('/home/user/pictures')
        del instance
        pass


class Test(unittest.TestCase):

    def setUp(self):
        with patch('libs.storage.Path', name='Path_mock', autospec=True, spec_set=True) as Path_mock:
            self.path_mock = Mock(name='path_mock', spec_set=Path)
            Path_mock.return_value = self.path_mock
            self.instance = Storage('/home/user/pictures', ['*.jpg', '*.png'])

    def test_first_get_current_None(self):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = [[], []]

        result = self.instance.get_current()

        self.assertIsNone(result)
        glob_mock.assert_has_calls([call('*.jpg'), call('*.png')])

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_first_get_current(self, Image_mock):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = [['3.jpg', '1.jpg'], ['2.png', '4.png']]
        img_mock = Mock(name='img_mock', spec_set=Image.Image)
        Image_mock.open.return_value = img_mock

        result = self.instance.get_current()

        self.assertEqual(result, img_mock)
        Image_mock.open.assert_called_once_with('1.jpg')
        img_mock.load.assert_called_once_with()

    def test_first_get_previous_None(self):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = [['3.jpg', '1.jpg'], ['2.png', '4.png']]

        result = self.instance.get_previous(0)
        self.assertIsNone(result)

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_first_get_next(self, Image_mock):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = [['3.jpg', '1.jpg'], ['2.png', '4.png']]
        imgs = [
            Mock(name='img_2_mock', spec_set=Image.Image),
            Mock(name='img_3_mock', spec_set=Image.Image),
            Mock(name='img_4_mock', spec_set=Image.Image)
        ]
        Image_mock.open.side_effect = imgs

        img = self.instance.get_next(0)
        self.assertEqual(img, imgs[0])
        img = self.instance.get_next(1)
        self.assertEqual(img, imgs[1])
        img = self.instance.get_next(2)
        self.assertEqual(img, imgs[2])
        img = self.instance.get_next(3)
        self.assertIsNone(img)

        glob_mock.assert_has_calls([call('*.jpg'), call('*.png')])
        Image_mock.open.assert_has_calls([call('2.png'), call('3.jpg'), call('4.png')])
        imgs[0].load.assert_called_once_with()
        imgs[1].load.assert_called_once_with()
        imgs[2].load.assert_called_once_with()

    @patch('libs.storage.Image', name='Image_mock', autospec=True, spec_set=True)
    def test_get_next_after_get_current(self, Image_mock):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = [['3.jpg', '1.jpg'], ['2.png', '4.png']]
        imgs = [
            Mock(name='img_1_mock', spec_set=Image.Image),
            Mock(name='img_2_mock', spec_set=Image.Image),
        ]
        Image_mock.open.side_effect = imgs

        img_current = self.instance.get_current()
        self.assertEqual(img_current, imgs[0])
        img_next = self.instance.get_next(0)
        self.assertEqual(img_next, imgs[1])

        glob_mock.assert_has_calls([call('*.jpg'), call('*.png')])
        Image_mock.open.assert_has_calls([call('1.jpg'), call('2.png')])
        imgs[0].load.assert_called_once_with()
        imgs[1].load.assert_called_once_with()

    def test_first_get_next_None(self):
        glob_mock = self.path_mock.glob
        glob_mock.side_effect = [['1.jpg'], []]

        result = self.instance.get_next(0)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
