import unittest
from PIL import Image, ImageChops

from libs.renderer import Renderer


def join_pics(pics, size):
    result = Image.new('RGB', size)
    offset = 0
    for p in pics:
        result.paste(p, (offset, 0))
        offset += p.width
    return result


class RenderDefault(unittest.TestCase):
    def setUp(self):
        self.instance = Renderer(width=400, height=100, distance=20)

    def test_Render(self):
        result = self.instance.render_default()
        self.assertEqual(result.size, (400, 100))


class RenderToLeft(unittest.TestCase):
    def setUp(self):
        self.instance = Renderer(width=400, height=100, distance=20)

    def test_Shift_0(self):
        next_pic = Image.new('RGB', (182, 200), 'green')
        pics_input = (
            Image.new('RGB', (100, 100), 'grey'),
            Image.new('RGB', (35, 50), 'cyan'),
            Image.new('RGB', (200, 200), 'red'),
            next_pic
        )
        pics_output = (
            Image.new('RGB', (40, 100), 'grey'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (70, 100), 'cyan'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (100, 100), 'red'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (91, 100), 'green'),
            Image.new('RGB', (39, 100), 'black')
        )
        correct_result = join_pics(pics_output, (400, 100))
        result = self.instance.render_to_left(pics_input, next_pic, 0)
        self.assertEqual(result.size, correct_result.size)
        self.assertIsNone(ImageChops.difference(result, correct_result).getbbox())

    def test_Shift_50(self):
        next_pic = Image.new('RGB', (114, 100), 'pink')
        pics_input = (
            Image.new('RGB', (73, 100), 'red'),
            Image.new('RGB', (79, 100), 'green'),
            next_pic,
            Image.new('RGB', (160, 160), 'orange')
        )
        pics_output = (
            Image.new('RGB', (10, 100), 'black'),
            Image.new('RGB', (73, 100), 'red'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (79, 100), 'green'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (114, 100), 'pink'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (64, 100), 'orange')
        )
        correct_result = join_pics(pics_output, (400, 100))
        result = self.instance.render_to_left(pics_input, next_pic, 50)
        self.assertEqual(result.size, correct_result.size)
        self.assertIsNone(ImageChops.difference(result, correct_result).getbbox())

    def test_Shift_100(self):
        next_pic = Image.new('RGB', (99, 100), 'red')
        pics_input = (
            Image.new('RGB', (100, 100), 'navy'),
            Image.new('RGB', (85, 100), 'lime'),
            next_pic,
            Image.new('RGB', (80, 100), 'green'),
            Image.new('RGB', (100, 100), 'magenta')
        )
        pics_output = (
            Image.new('RGB', (26, 100), 'navy'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (85, 100), 'lime'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (99, 100), 'red'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (80, 100), 'green'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (30, 100), 'magenta')
        )
        correct_result = join_pics(pics_output, (400, 100))
        result = self.instance.render_to_left(pics_input, next_pic, 100)
        self.assertEqual(result.size, correct_result.size)
        self.assertIsNone(ImageChops.difference(result, correct_result).getbbox())
