from time import sleep


class Slider(object):
    
    def __init__(self, storage, renderer, ui):
        self._storage = storage
        self._renderer = renderer
        self._ui = ui

    def to_left(self):
        pic_current = self._storage.get_current()
        if pic_current is None:
            pic = self._renderer.render_default()
            self._ui.draw(pic)
            return

        side_left = self._get_side_left(pic_current)

        self._storage.step_next()
        pic_next = self._storage.get_current()
        if pic_next is None:
            pic_ui = self._renderer.render_to_left(side_left, pic_current, 100)
            self._ui.draw(pic_ui)
            return

        side_right = self._get_right_side(pic_next)

        for i in range(101):
            pic = self._renderer.render_to_left(side_left + side_right, pic_next, i)
            self._ui.draw(pic)
            sleep(0.01)

    def to_right(self):
        pic_current = self._storage.get_current()
        if pic_current is None:
            pic = self._renderer.render_default()
            self._ui.draw(pic)
            return

        side_right = self._get_right_side(pic_current)

        self._storage.step_previous()
        pic_previous = self._storage.get_current()
        if pic_previous is None:
            pic_ui = self._renderer.render_to_right(side_right, pic_current, 100)
            self._ui.draw(pic_ui)
            return

        side_left = self._get_side_left(pic_previous)

        for i in range(101):
            pic = self._renderer.render_to_right(side_left + side_right, pic_previous, i)
            self._ui.draw(pic)
            sleep(0.01)

    def _get_side_left(self, pic_center):
        result = [pic_center]
        i = 0
        while True:
            pic = self._storage.get_previous(i)
            if pic is None:
                break
            result.insert(0, pic)
            attempt = self._renderer.calc(result, pic_center)
            if attempt['left_done']:
                break
            i += 1
        return result

    def _get_right_side(self, pic_center):
        result = [pic_center]
        i = 0
        while True:
            pic = self._storage.get_next(i)
            if pic is None:
                break
            result.append(pic)
            attempt = self._renderer.calc(result, pic_center)
            if attempt['right_done']:
                break
            i += 1
        return result
