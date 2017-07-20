import unittest
from unittest import mock
import itertools


from libs.slider import Slider


class ToLeft(unittest.TestCase):

    def setUp(self):
        self.storage_mock = mock.Mock()
        self.renderer_mock = mock.Mock()
        self.ui_mock = mock.Mock(spec=['draw'])
        self.instance = Slider(self.storage_mock, self.renderer_mock, self.ui_mock)

    def test_StorageNoData(self):
        self.storage_mock.mock_add_spec(['get_current'])
        self.storage_mock.get_current.return_value = None

        self.renderer_mock.mock_add_spec(['render_default'])
        pic_mock = object()
        self.renderer_mock.render_default.return_value = pic_mock

        self.instance.to_left()

        self.storage_mock.get_current.assert_called_once_with()
        self.renderer_mock.render_default.assert_called_once_with()
        self.ui_mock.draw.assert_called_once_with(pic_mock)

    def test_StorageNoNext(self):
        self.storage_mock.mock_add_spec(['get_previous', 'get_current', 'step_next'])
        pic_current = object()
        self.storage_mock.get_current.side_effect = (pic_current, None)
        pic_previous_1, pic_previous_2 = object(), object()
        self.storage_mock.get_previous.side_effect = (pic_previous_2, pic_previous_1, None)
        expect_storage = (
            mock.call.get_current(),
            mock.call.get_previous(0), mock.call.get_previous(1), mock.call.get_previous(2),
            mock.call.step_next(),
            mock.call.get_current()
        )

        self.renderer_mock.mock_add_spec(['calc', 'render_to_left'])
        calc_result = (
            # only left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False}
        )
        self.renderer_mock.calc.side_effect = calc_result
        pic_ui = object()
        self.renderer_mock.render_to_left.return_value = pic_ui
        expect_renderer = (
            mock.call.calc(mock.ANY, mock.ANY), mock.call.calc(mock.ANY, mock.ANY),
            mock.call.render_to_left([pic_previous_1, pic_previous_2, pic_current], pic_current, 100)
        )

        self.instance.to_left()

        self.storage_mock.assert_has_calls(expect_storage)
        self.renderer_mock.assert_has_calls(expect_renderer)
        self.ui_mock.draw.assert_called_once_with(pic_ui)

    def test_StorageLimit(self):
        self.storage_mock.mock_add_spec(['get_previous', 'get_current', 'get_next', 'step_next'])
        left_data = [None, object(), object()]
        self.storage_mock.get_previous.side_effect = left_data[::-1]
        pic_next = object()
        current_data = [object(), pic_next]
        self.storage_mock.get_current.side_effect = current_data
        right_data = [object(), object(), None]
        self.storage_mock.get_next.side_effect = right_data
        expect_storage = (
            mock.call.get_current(),
            mock.call.get_previous(0), mock.call.get_previous(1), mock.call.get_previous(2),
            mock.call.step_next(),
            mock.call.get_current(),
            mock.call.get_next(0), mock.call.get_next(1), mock.call.get_next(2)
        )

        self.renderer_mock.mock_add_spec(['calc', 'render_to_left'])
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
        self.renderer_mock.render_to_left.side_effect = render_result
        expect_renderer = itertools.chain(
            itertools.repeat(mock.call.calc(mock.ANY, mock.ANY), len(calc_result)),
            (mock.call.render_to_left(left_data[1::] + current_data + right_data[:-1:], pic_next, i) for i in range(0, 100))
        )
        expect_renderer = list(expect_renderer)

        expect_ui = (mock.call.draw(pic) for pic in render_result)

        self.instance.to_left()

        self.storage_mock.assert_has_calls(expect_storage)
        self.renderer_mock.assert_has_calls(expect_renderer)
        self.ui_mock.assert_has_calls(expect_ui)


if __name__ == '__main__':
    unittest.main()
