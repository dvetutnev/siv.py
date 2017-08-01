import unittest
from unittest.mock import Mock, patch, call, ANY
import itertools


from libs.slider import Slider


class ToLeft(unittest.TestCase):

    def setUp(self):
        self.storage_mock = Mock()
        self.renderer_mock = Mock()
        self.ui_mock = Mock(spec_set=['draw'])
        self.instance = Slider(self.storage_mock, self.renderer_mock, self.ui_mock)
        self.patcher = patch('libs.slider.sleep')
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_StorageNoData(self):
        self.storage_mock.mock_add_spec(['get_current'], spec_set=True)
        self.storage_mock.get_current.return_value = None

        self.renderer_mock.mock_add_spec(['render_default'], spec_set=True)
        pic_mock = object()
        self.renderer_mock.render_default.return_value = pic_mock

        self.instance.to_left()

        self.storage_mock.get_current.assert_called_once_with()
        self.renderer_mock.render_default.assert_called_once_with()
        self.ui_mock.draw.assert_called_once_with(pic_mock)

    def test_StorageNoNext(self):
        self.storage_mock.mock_add_spec(['get_previous', 'get_current', 'step_next'], spec_set=True)
        pic_current = object()
        self.storage_mock.get_current.side_effect = (pic_current, None)
        pic_previous_1, pic_previous_2 = object(), object()
        self.storage_mock.get_previous.side_effect = (pic_previous_1, pic_previous_2, None)
        expect_storage = (
            call.get_current(),
            call.get_previous(0), call.get_previous(1), call.get_previous(2),
            call.step_next(),
            call.get_current()
        )

        self.renderer_mock.mock_add_spec(['calc', 'render_to_left'], spec_set=True)
        calc_result = (
            # only left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False}
        )
        self.renderer_mock.calc.side_effect = calc_result
        pic_ui = object()
        self.renderer_mock.render_to_left.return_value = pic_ui
        expect_renderer = (
            call.calc(ANY, ANY), call.calc(ANY, ANY),
            call.render_to_left([pic_previous_2, pic_previous_1, pic_current], pic_current, 100)
        )

        self.instance.to_left()

        self.storage_mock.assert_has_calls(expect_storage)
        self.renderer_mock.assert_has_calls(expect_renderer)
        self.ui_mock.draw.assert_called_once_with(pic_ui)

    def test_StorageLimit(self):
        self.storage_mock.mock_add_spec(['get_previous', 'get_current', 'get_next', 'step_next'], spec_set=True)
        left_data = [None, object(), object()]
        self.storage_mock.get_previous.side_effect = left_data[::-1]
        pic_next = object()
        current_data = [object(), pic_next]
        self.storage_mock.get_current.side_effect = current_data
        right_data = [object(), object(), None]
        self.storage_mock.get_next.side_effect = right_data
        expect_storage = (
            call.get_current(),
            call.get_previous(0), call.get_previous(1), call.get_previous(2),
            call.step_next(),
            call.get_current(),
            call.get_next(0), call.get_next(1), call.get_next(2)
        )

        self.renderer_mock.mock_add_spec(['calc', 'render_to_left'], spec_set=True)
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
        expect_renderer_calc = list(itertools.repeat(call.calc(ANY, ANY), len(calc_result)))
        expect_renderer_render = [
            call.render_to_left(left_data[1::] + current_data + right_data[:-1:], pic_next, i) for i in range(101)
        ]

        expect_ui = (call.draw(pic) for pic in render_result)

        self.instance.to_left()

        self.storage_mock.assert_has_calls(expect_storage)
        self.assertEqual(self.renderer_mock.render_to_left.call_count, len(expect_renderer_render))
        self.renderer_mock.assert_has_calls(expect_renderer_calc + expect_renderer_render)
        self.ui_mock.assert_has_calls(expect_ui)

    def test_RendererLimit(self):
        self.storage_mock.mock_add_spec(['get_previous', 'get_current', 'get_next', 'step_next'], spec_set=True)
        left_data = [object(), object(), object()]
        self.storage_mock.get_previous.side_effect = left_data[::-1]
        pic_current, pic_next = object(), object()
        current_data = [pic_current, pic_next]
        self.storage_mock.get_current.side_effect = current_data
        right_data = [object(), object(), object()]
        self.storage_mock.get_next.side_effect = right_data
        expect_storage = (
            call.get_current(),
            call.get_previous(0), call.get_previous(1), call.get_previous(2),
            call.step_next(),
            call.get_current(),
            call.get_next(0), call.get_next(1), call.get_next(2)
        )

        self.renderer_mock.mock_add_spec(['calc', 'render_to_left'], spec_set=True)
        calc_result = (
            # left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': True, 'right': 2, 'right_done': False},
            # right side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 2, 'right_done': True}
        )
        self.renderer_mock.calc.side_effect = calc_result
        self.renderer_mock.render_to_left.side_effect = itertools.repeat(object, 101)
        left_data_calc = left_data[::] + [pic_current]
        right_data_calc = [pic_next] + right_data[::]
        expect_renderer_calc = [
            #left side
            call.calc(ANY, pic_current),
            call.calc(ANY, pic_current),
            call.calc(left_data_calc, pic_current),
            #right side
            call.calc(ANY, pic_next),
            call.calc(ANY, pic_next),
            call.calc(right_data_calc, pic_next)
        ]
        expect_renderer_render = [
            call.render_to_left(left_data + current_data + right_data, pic_next, i) for i in range(101)
        ]

        expect_ui = list(itertools.repeat(call.draw(ANY), 101))

        self.instance.to_left()

        self.storage_mock.assert_has_calls(expect_storage)
        self.renderer_mock.calc.assert_has_calls(expect_renderer_calc)
        self.renderer_mock.assert_has_calls(expect_renderer_calc + expect_renderer_render)
        self.ui_mock.assert_has_calls(expect_ui)


class ToRight(unittest.TestCase):

    def setUp(self):
        self.storage_mock = Mock()
        self.renderer_mock = Mock()
        self.ui_mock = Mock(spec_set=['draw'])
        self.instance = Slider(self.storage_mock, self.renderer_mock, self.ui_mock)
        self.patcher = patch('libs.slider.sleep')
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_StorageNoData(self):
        self.storage_mock.mock_add_spec(['get_current'], spec_set=True)
        self.storage_mock.get_current.return_value = None

        self.renderer_mock.mock_add_spec(['render_default'], spec_set=True)
        pic_mock = object()
        self.renderer_mock.render_default.return_value = pic_mock

        self.instance.to_right()

        self.storage_mock.get_current.assert_called_once_with()
        self.renderer_mock.render_default.assert_called_once_with()
        self.ui_mock.draw.assert_called_once_with(pic_mock)

    def test_StorageNoPrevious(self):
        self.storage_mock.mock_add_spec(['get_current', 'get_next', 'step_previous'], spec_set=True)
        pic_current = object()
        self.storage_mock.get_current.side_effect = (pic_current, None)
        pic_next_1, pic_next_2 = object(), object()
        self.storage_mock.get_next.side_effect = (pic_next_1, pic_next_2, None)
        expect_storage = (
            call.get_current(),
            call.get_next(0), call.get_next(1), call.get_next(2),
            call.step_previous(),
            call.get_current()
        )

        self.renderer_mock.mock_add_spec(['calc', 'render_to_right'], spec_set=True)
        calc_result = (
            # only left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False}
        )
        self.renderer_mock.calc.side_effect = calc_result
        pic_ui = object()
        self.renderer_mock.render_to_right.return_value = pic_ui
        expect_renderer = (
            call.calc(ANY, ANY), call.calc(ANY, ANY),
            call.render_to_right([pic_current, pic_next_1, pic_next_2], pic_current, 100)
        )

        self.instance.to_right()

        self.storage_mock.assert_has_calls(expect_storage)
        self.renderer_mock.assert_has_calls(expect_renderer)
        self.ui_mock.draw.assert_called_once_with(pic_ui)

    def test_StorageLimit(self):
        self.storage_mock.mock_add_spec(['get_previous', 'get_current', 'get_next', 'step_previous'], spec_set=True)
        left_data = [None, object(), object()]
        self.storage_mock.get_previous.side_effect = left_data[::-1]
        pic_previous = object()
        current_data = [object(), pic_previous]
        self.storage_mock.get_current.side_effect = current_data
        right_data = [object(), object(), None]
        self.storage_mock.get_next.side_effect = right_data
        expect_storage = (
            call.get_current(),
            call.get_next(0), call.get_next(1), call.get_next(2),
            call.step_previous(),
            call.get_current(),
            call.get_previous(0), call.get_previous(1), call.get_previous(2),
        )

        self.renderer_mock.mock_add_spec(['calc', 'render_to_right'], spec_set=True)
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
        self.renderer_mock.render_to_right.side_effect = render_result
        expect_renderer_calc = list(itertools.repeat(call.calc(ANY, ANY), len(calc_result)))
        expect_renderer_render = [
            call.render_to_right(left_data[1::] + current_data[::-1] + right_data[:-1:], pic_previous, i) for i in range(101)
        ]

        expect_ui = (call.draw(pic) for pic in render_result)

        self.instance.to_right()

        self.storage_mock.assert_has_calls(expect_storage)
        self.assertEqual(self.renderer_mock.render_to_right.call_count, len(expect_renderer_render))
        self.renderer_mock.assert_has_calls(expect_renderer_calc + expect_renderer_render)
        self.ui_mock.assert_has_calls(expect_ui)

    def test_RendererLimit(self):
        self.storage_mock.mock_add_spec(['get_previous', 'get_current', 'get_next', 'step_previous'], spec_set=True)
        left_data = [object(), object(), object()]
        self.storage_mock.get_previous.side_effect = left_data[::-1]
        pic_current, pic_previous = object(), object()
        current_data = [pic_current, pic_previous]
        self.storage_mock.get_current.side_effect = current_data
        right_data = [object(), object(), object()]
        self.storage_mock.get_next.side_effect = right_data
        expect_storage = (
            call.get_current(),
            call.get_next(0), call.get_next(1), call.get_next(2),
            call.step_previous(),
            call.get_current(),
            call.get_previous(0), call.get_previous(1), call.get_previous(2),
        )

        self.renderer_mock.mock_add_spec(['calc', 'render_to_right'], spec_set=True)
        calc_result = (
            # right side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 2, 'right_done': True},
            # left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': True, 'right': 2, 'right_done': False}
        )
        self.renderer_mock.calc.side_effect = calc_result
        self.renderer_mock.render_to_right.side_effect = itertools.repeat(object, 101)
        left_data_calc = left_data[::] + [pic_previous]
        right_data_calc = [pic_current] + right_data[::]
        expect_renderer_calc = [
            #right side
            call.calc(ANY, pic_current),
            call.calc(ANY, pic_current),
            call.calc(right_data_calc, pic_current),
            #left side
            call.calc(ANY, pic_previous),
            call.calc(ANY, pic_previous),
            call.calc(left_data_calc, pic_previous),
        ]
        expect_renderer_render = [
            call.render_to_right(left_data + current_data[::-1] + right_data, pic_previous, i) for i in range(101)
        ]

        expect_ui = list(itertools.repeat(call.draw(ANY), 101))

        self.instance.to_right()

        self.storage_mock.assert_has_calls(expect_storage)
        self.renderer_mock.calc.assert_has_calls(expect_renderer_calc)
        self.renderer_mock.assert_has_calls(expect_renderer_calc + expect_renderer_render)
        self.ui_mock.assert_has_calls(expect_ui)


if __name__ == '__main__':
    unittest.main()
