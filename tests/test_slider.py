import unittest
from unittest import mock
import itertools


from libs.slider import Slider


class ToLeft(unittest.TestCase):

    def setUp(self):
        self.storage_mock = mock.Mock()
        self.renderer_mock = mock.Mock()
        self.ui_mock = mock.Mock()
        self.instance = Slider(self.storage_mock, self.renderer_mock, self.ui_mock)

    def test_create(self):
        self.assertIsNotNone(self.instance)

    def test_StorageLimit(self):
        left_data = [None, object(), object()]
        current_data = [object(), object()]
        right_data = [object(), object(), None]

        self.storage_mock.get_previous.side_effect = left_data[::-1]
        self.storage_mock.get_current.side_effect = current_data
        self.storage_mock.get_next.side_effect = right_data

        expect_storage = (
            mock.call.get_current(),
            mock.call.get_previous(0), mock.call.get_previous(1), mock.call.get_previous(2),
            mock.call.step_next(),
            mock.call.get_current(),
            mock.call.get_next(0), mock.call.get_next(1), mock.call.get_next(2)
        )

        calc_result = (
            # left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            # right side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False}
        )

        self.renderer_mock.calc.side_effect = calc_result

        render_result = itertools.repeat(object, 101)
        self.renderer_mock.render.side_effect = render_result

        expect_renderer = itertools.chain(
            itertools.repeat(mock.call.calc(mock.ANY, mock.ANY), len(calc_result)),
            (mock.call.render(mock.ANY, mock.ANY, i) for i in range(0, 100))
        )
        expect_renderer = list(expect_renderer)

        expect_ui = (mock.call.draw(pic_mock) for pic_mock in render_result)

        self.instance.to_left()

        self.storage_mock.assert_has_calls(expect_storage)
        self.renderer_mock.assert_has_calls(expect_renderer)
        self.ui_mock.assert_has_calls(expect_ui)


if __name__ == '__main__':
    unittest.main()
