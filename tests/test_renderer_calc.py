import unittest
from PIL import Image


from libs.renderer import Renderer


class Calc(unittest.TestCase):

    def setUp(self):
        self.instance = Renderer(width=400, height=100, distance=20)

    def test_NoComplete(self):
        pic_left = Image.new('RGB', (200, 200))
        pic_center = Image.new('RGB', (150, 200))
        pic_right = Image.new('RGB', (50, 50))

        result_correct = {'left': 0, 'left_done': False, 'right': 2, 'right_done': False}
        pictures = [pic_left, pic_center, pic_right]

        result = self.instance.calc(pictures, pic_center)
        self.assertEqual(result, result_correct)

    def test_LeftComplete(self):
        pic_left_1 = Image.new('RGB', (500, 500))
        pic_left_2 = Image.new('RGB', (400, 400))
        pic_left_3 = Image.new('RGB', (200, 200))
        pic_center = Image.new('RGB', (150, 200))
        pic_right = Image.new('RGB', (50, 50))

        pictures = [pic_left_1, pic_left_2, pic_left_3, pic_center, pic_right]
        result_correct = {'left': 1, 'left_done': True, 'right': 4, 'right_done': False}

        result = self.instance.calc(pictures, pic_center)
        self.assertEqual(result, result_correct)

    def test_RightComplete(self):
        pic_left = Image.new('RGB', (200, 200))
        pic_center = Image.new('RGB', (150, 200))
        pic_right_1 = Image.new('RGB', (50, 50))
        pic_right_2 = Image.new('RGB', (46, 200))
        pic_right_3 = Image.new('RGB', (200, 200))

        pictures = [pic_left, pic_center, pic_right_1, pic_right_2, pic_right_3]
        result_correct = {'left': 0, 'left_done': False, 'right': 3, 'right_done': True}

        result = self.instance.calc(pictures, pic_center)
        self.assertEqual(result, result_correct)

    def test_Complete(self):
        pic_left_1 = Image.new('RGB', (500, 500))
        pic_left_2 = Image.new('RGB', (400, 400))
        pic_left_3 = Image.new('RGB', (200, 200))
        pic_center = Image.new('RGB', (150, 200))
        pic_right_1 = Image.new('RGB', (50, 50))
        pic_right_2 = Image.new('RGB', (407, 407))
        pic_right_3 = Image.new('RGB', (200, 200))

        pictures = [pic_left_1, pic_left_2, pic_left_3, pic_center, pic_right_1, pic_right_2, pic_right_3]
        result_correct = {'left': 1, 'left_done': True, 'right': 5, 'right_done': True}

        result = self.instance.calc(pictures, pic_center)
        self.assertEqual(result, result_correct)

    def test_NoLeftPics(self):
        pic_center = Image.new('RGB', (150, 200))
        pic_right = Image.new('RGB', (50, 50))

        result_correct = {'left': 0, 'left_done': False, 'right': 1, 'right_done': False}
        pictures = [pic_center, pic_right]

        result = self.instance.calc(pictures, pic_center)
        self.assertEqual(result, result_correct)

    def test_NoRightPics(self):
        pic_left = Image.new('RGB', (200, 200))
        pic_center = Image.new('RGB', (150, 200))

        result_correct = {'left': 0, 'left_done': False, 'right': 1, 'right_done': False}
        pictures = [pic_left, pic_center]

        result = self.instance.calc(pictures, pic_center)
        self.assertEqual(result, result_correct)
