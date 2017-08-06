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
        storage = self.storage_mock
        renderer = self.renderer_mock
        ui = self.ui_mock

        storage.mock_add_spec(['get'], spec_set=True)
        storage.get.return_value = None
        renderer.mock_add_spec(['render_default'], spec_set=True)
        img_mock = Mock(spec_set=[])
        renderer.render_default.return_value = img_mock

        self.instance.to_left()

        storage.get.assert_called_once_with(0)
        renderer.render_default.assert_called_once_with()
        ui.draw.assert_called_once_with(img_mock)

    def test_StorageNoNext(self):
        storage = self.storage_mock
        renderer = self.renderer_mock
        ui = self.ui_mock

        storage.mock_add_spec(['get'], spec_set=True)
        img_current = Mock(spec_set=[], name='image_current')
        imgs = {
            -3: None,
            -2: Mock(spec_set=[], name='img_-2'),
            -1: Mock(spec_set=[], name='img_-1'),
            0: img_current,
            1: None
        }

        def _get(offset):
            return imgs[offset]

        storage.get.side_effect = _get
        expect_storage_get = [
            call.get(0), call.get(-1), call.get(-2), call.get(-3),
            call.get(1)
        ]

        renderer.mock_add_spec(['calc', 'render_to_left'], spec_set=True)
        calc_result = [
            # only left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 2, 'right_done': False}
        ]
        renderer.calc.side_effect = calc_result
        expect_renderer_calc = list(itertools.repeat(call.calc(ANY, ANY), len(calc_result)))
        img_ui = Mock(spec_set=[])
        renderer.render_to_left.return_value = img_ui
        expect_renderer_render = [call.render_to_left([imgs[-2], imgs[-1], imgs[0]], img_current, 100)]

        self.instance.to_left()

        storage.assert_has_calls(expect_storage_get)
        renderer.assert_has_calls(expect_renderer_calc + expect_renderer_render)
        ui.draw.assert_called_once_with(img_ui)

    def test_StorageLimit(self):
        storage = self.storage_mock
        renderer = self.renderer_mock
        ui = self.ui_mock

        storage.mock_add_spec(['get', 'step_next'], spec_set=True)
        img_next = Mock(spec_set=[], name='img_next')
        imgs = {
            -3: None,
            -2: Mock(spec_set=[], name='img_-2'),
            -1: Mock(spec_set=[], name='img_-1'),
            0: Mock(spec_set=[], name='img_0'),
            1: img_next,
            2: Mock(spec_set=[], name='img_2'),
            3: Mock(spec_set=[], name='img_3'),
            4: None,
        }

        def _get(offset):
            return imgs[offset]

        storage.get.side_effect = _get
        expect_storage_get = [
            call.get(0), call.get(-1), call.get(-2), call.get(-3),
            call.get(1), call.get(2), call.get(3), call.get(4)
        ]

        renderer.mock_add_spec(['calc', 'render_to_left'], spec_set=True)
        calc_result = [
            # left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 2, 'right_done': False},
            # right side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 2, 'right_done': False}
        ]
        renderer.calc.side_effect = calc_result
        expect_renderer_calc = list(itertools.repeat(call.calc(ANY, ANY), len(calc_result)))

        render_result = list(itertools.repeat(Mock(spec_set=[]), 101))
        renderer.render_to_left.side_effect = render_result
        args_render = [imgs[-2], imgs[-1], imgs[0], imgs[1], imgs[2], imgs[3]]
        expect_renderer_render = [
            call.render_to_left(args_render, img_next, i) for i in range(101)
        ]

        expect_ui = [call.draw(pic) for pic in render_result]

        self.instance.to_left()

        storage.assert_has_calls(expect_storage_get + [call.step_next()])
        self.assertEqual(renderer.calc.call_count, len(expect_renderer_calc))
        self.assertEqual(renderer.render_to_left.call_count, len(expect_renderer_render))
        renderer.assert_has_calls(expect_renderer_calc + expect_renderer_render)
        ui.assert_has_calls(expect_ui)

    def test_RendererLimit(self):
        storage = self.storage_mock
        renderer = self.renderer_mock
        ui = self.ui_mock

        storage.mock_add_spec(['get', 'step_next'], spec_set=True)
        img_current = Mock(spec_set=[], name='img_next')
        img_next = Mock(spec_set=[], name='img_next')
        imgs = {
            -2: Mock(spec_set=[], name='img_-2'),
            -1: Mock(spec_set=[], name='img_-1'),
            0: img_current,
            1: img_next,
            2: Mock(spec_set=[], name='img_2'),
            3: Mock(spec_set=[], name='img_3')
        }

        def _get(offset):
            return imgs[offset]

        storage.get.side_effect = _get
        expect_storage_get = [
            call.get(0), call.get(-1), call.get(-2),
            call.get(1), call.get(2), call.get(3)
        ]

        renderer.mock_add_spec(['calc', 'render_to_left'], spec_set=True)
        calc_result = [
            # left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': True, 'right': 2, 'right_done': False},
            # right side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 2, 'right_done': True}
        ]
        renderer.calc.side_effect = calc_result

        expect_renderer_calc = [
            #left side
            call.calc(ANY, img_current),
            call.calc(ANY, img_current),
            call.calc([imgs[-2], imgs[-1], imgs[0]], img_current),
            #right side
            call.calc(ANY, img_next),
            call.calc(ANY, img_next),
            call.calc([imgs[1], imgs[2], imgs[3]], img_next)
        ]

        renderer.render_to_left.side_effect = list(itertools.repeat(Mock(spec_set=[]), 101))
        args_render = [imgs[-2], imgs[-1], imgs[0], imgs[1], imgs[2], imgs[3]]
        expect_renderer_render = [
            call.render_to_left(args_render, img_next, i) for i in range(101)
        ]

        expect_ui = list(itertools.repeat(call.draw(ANY), 101))

        self.instance.to_left()

        storage.assert_has_calls(expect_storage_get + [call.step_next()])
        self.assertEqual(renderer.calc.call_count, len(expect_renderer_calc))
        self.assertEqual(renderer.render_to_left.call_count, len(expect_renderer_render))
        renderer.assert_has_calls(expect_renderer_calc + expect_renderer_render)
        ui.assert_has_calls(expect_ui)


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
        storage = self.storage_mock
        renderer = self.renderer_mock
        ui = self.ui_mock

        storage.mock_add_spec(['get'], spec_set=True)
        storage.get.return_value = None
        renderer.mock_add_spec(['render_default'], spec_set=True)
        img_mock = Mock(spec_set=[])
        renderer.render_default.return_value = img_mock

        self.instance.to_right()

        storage.get.assert_called_once_with(0)
        renderer.render_default.assert_called_once_with()
        ui.draw.assert_called_once_with(img_mock)

    def test_StorageNoPrevious(self):
        storage = self.storage_mock
        renderer = self.renderer_mock
        ui = self.ui_mock

        storage.mock_add_spec(['get'], spec_set=True)
        img_current = Mock(spec_set=[], name='img_current')
        imgs = {
            -1: None,
            0: img_current,
            1: Mock(spec_set=[], name='img_1'),
            2: Mock(spec_set=[], name='img_2'),
            3: None
        }

        def _get(offset):
            return imgs[offset]

        storage.get.side_effect = _get
        expect_storage_get = [
            call.get(0), call.get(1), call.get(2), call.get(3),
            call.get(-1)
        ]

        renderer.mock_add_spec(['calc', 'render_to_right'], spec_set=True)
        calc_result = [
            # only right side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 2, 'right_done': False}
        ]
        renderer.calc.side_effect = calc_result
        expect_renderer_calc = list(itertools.repeat(call.calc(ANY, ANY), len(calc_result)))
        img_ui = Mock(spec_set=[])
        renderer.render_to_right.return_value = img_ui
        expect_renderer_render = [call.render_to_right([imgs[0], imgs[1], imgs[2]], img_current, 100)]

        self.instance.to_right()

        storage.assert_has_calls(expect_storage_get)
        renderer.assert_has_calls(expect_renderer_calc + expect_renderer_render)
        ui.draw.assert_called_once_with(img_ui)

    def test_StorageLimit(self):
        storage = self.storage_mock
        renderer = self.renderer_mock
        ui = self.ui_mock

        storage.mock_add_spec(['get', 'step_previous'], spec_set=True)
        img_previous = Mock(spec_set=[], name='img_previous')
        imgs = {
            -4: None,
            -3: Mock(spec_set=[], name='img_-3'),
            -2: Mock(spec_set=[], name='img_-2'),
            -1: img_previous,
            0: Mock(spec_set=[], name='img_0'),
            1: Mock(spec_set=[], name='img_1'),
            2: Mock(spec_set=[], name='img_2'),
            3: None
        }

        def _get(offset):
            return imgs[offset]

        storage.get.side_effect = _get
        expect_storage_get = [
            call.get(0), call.get(1), call.get(2), call.get(3),
            call.get(-1), call.get(-2), call.get(-3), call.get(-4)
        ]

        renderer.mock_add_spec(['calc', 'render_to_right'], spec_set=True)
        calc_result = [
            # left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 2, 'right_done': False},
            # right side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 2, 'right_done': False}
        ]
        renderer.calc.side_effect = calc_result
        expect_renderer_calc = list(itertools.repeat(call.calc(ANY, ANY), len(calc_result)))

        render_result = list(itertools.repeat(Mock(spec_set=[]), 101))
        renderer.render_to_right.side_effect = render_result
        args_render = [imgs[-3], imgs[-2], imgs[-1], imgs[0], imgs[1], imgs[2]]
        expect_renderer_render = [
            call.render_to_right(args_render, img_previous, i) for i in range(101)
        ]

        expect_ui = [call.draw(pic) for pic in render_result]

        self.instance.to_right()

        storage.assert_has_calls(expect_storage_get + [call.step_previous()])
        self.assertEqual(renderer.calc.call_count, len(expect_renderer_calc))
        self.assertEqual(renderer.render_to_right.call_count, len(expect_renderer_render))
        renderer.assert_has_calls(expect_renderer_calc + expect_renderer_render)
        ui.assert_has_calls(expect_ui)

    def test_RendererLimit(self):
        storage = self.storage_mock
        renderer = self.renderer_mock
        ui = self.ui_mock

        storage.mock_add_spec(['get', 'step_previous'], spec_set=True)
        img_current = Mock(spec_set=[], name='img_next')
        img_previous = Mock(spec_set=[], name='img_next')
        imgs = {
            -3: Mock(spec_set=[], name='img_-3'),
            -2: Mock(spec_set=[], name='img_-2'),
            -1: img_previous,
            0: img_current,
            1: Mock(spec_set=[], name='img_1'),
            2: Mock(spec_set=[], name='img_2')
        }

        def _get(offset):
            return imgs[offset]

        storage.get.side_effect = _get
        expect_storage_get = [
            call.get(0), call.get(1), call.get(2),
            call.get(-1), call.get(-2), call.get(-3)
        ]

        renderer.mock_add_spec(['calc', 'render_to_right'], spec_set=True)
        calc_result = [
            # right side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 2, 'right_done': True},
            # left side
            {'left': 0, 'left_done': False, 'right': 0, 'right_done': False},
            {'left': 0, 'left_done': False, 'right': 1, 'right_done': False},
            {'left': 0, 'left_done': True, 'right': 2, 'right_done': False}
        ]
        renderer.calc.side_effect = calc_result

        expect_renderer_calc = [
            #left side
            call.calc(ANY, img_current),
            call.calc(ANY, img_current),
            call.calc([imgs[0], imgs[1], imgs[2]], img_current),
            #right side
            call.calc(ANY, img_previous),
            call.calc(ANY, img_previous),
            call.calc([imgs[-3], imgs[-2], imgs[-1]], img_previous)
        ]

        renderer.render_to_right.side_effect = list(itertools.repeat(Mock(spec_set=[]), 101))
        args_render = [imgs[-3], imgs[-2], imgs[-1], imgs[0], imgs[1], imgs[2]]
        expect_renderer_render = [
            call.render_to_right(args_render, img_previous, i) for i in range(101)
        ]

        expect_ui = list(itertools.repeat(call.draw(ANY), 101))

        self.instance.to_right()

        storage.assert_has_calls(expect_storage_get + [call.step_previous()])
        self.assertEqual(renderer.calc.call_count, len(expect_renderer_calc))
        self.assertEqual(renderer.render_to_right.call_count, len(expect_renderer_render))
        renderer.assert_has_calls(expect_renderer_calc + expect_renderer_render)
        ui.assert_has_calls(expect_ui)


if __name__ == '__main__':
    unittest.main()
