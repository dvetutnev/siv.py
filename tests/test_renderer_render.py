import unittest
from PIL import Image


from libs.renderer import Renderer


def join_pics(pics, size):
    result = Image.new('RGB', size)
    offset = 0
    for p in pics:
        result.paste(p, (offset, 0))
        offset += p.width
    return result

class RenderToLeft(unittest.TestCase):

    def setUp(self):
        self.instance = Renderer(width=400, height=100, distance=20)

    def test_Shift_0(self):
        next_pic = Image.new('RGB', (182, 200), 'green')
        pics_input = (
            Image.new('RGB', (100, 100), 'grey'),
            Image.new('RGB', (50, 50), 'cyan'),
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
        correct_result.save('to_left_0.jpg')
        pass

    def test_Shift_50(self):
        next_pic = Image.new('RGB', (242, 200), 'pink')
        pics_input = (
            Image.new('RGB', (75, 150), 'red'),
            Image.new('RGB', (40, 50), 'green'),
            next_pic,
            Image.new('RGB', (160, 160), 'orange')
        )
        pics_output = (
            Image.new('RGB', (10, 100), 'black'),
            Image.new('RGB', (50, 100), 'red'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (80, 100), 'green'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (121, 100), 'pink'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (69, 100), 'orange')
        )
        correct_result = join_pics(pics_output, (400, 100))
        correct_result.save('to_left_50.jpg')
        pass

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
            Image.new('RGB', (25, 100), 'navy'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (85, 100), 'lime'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (99, 100), 'red'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (80, 100), 'green'),
            Image.new('RGB', (20, 100), 'black'),
            Image.new('RGB', (31, 100), 'magenta')
        )
        correct_result = join_pics(pics_output, (400, 100))
        correct_result.save('to_left_100.jpg')
        pass
