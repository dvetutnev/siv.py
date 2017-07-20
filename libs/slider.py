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

        side_left = [pic_current]
        i = 0
        while True:
            pic = self._storage.get_previous(i)
            if pic is None:
                break
            side_left.insert(0, pic)
            result = self._renderer.calc(side_left[::], pic_current)
            if result['left_done']:
                break
            i += 1

        self._storage.step_next()
        pic_next = self._storage.get_current()
        if pic_next is None:
            pic_ui = self._renderer.render_to_left(side_left[::], pic_current, 100)
            self._ui.draw(pic_ui)
            return

        right_side = [pic_next]
        i = 0
        while True:
            pic = self._storage.get_next(i)
            if pic is None:
                break
            right_side.append(pic)
            result = self._renderer.calc(right_side[::], pic_next)
            if result['right_done']:
                break
            i += 1

        for i in range(101):
            pic = self._renderer.render_to_left(side_left + right_side, pic_next, i)
            self._ui.draw(pic)
