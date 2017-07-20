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
            result = self._renderer.calc(side_left, pic_current)
            if result['left_done']:
                break
            i += 1

        self._storage.step_next()
        pic_next = self._storage.get_current()
        if pic_next is None:
            pic_ui = self._renderer.render_to_left(side_left, pic_current, 100)
            self._ui.draw(pic_ui)
            return

        side_right = [pic_next]
        i = 0
        while True:
            pic = self._storage.get_next(i)
            if pic is None:
                break
            side_right.append(pic)
            result = self._renderer.calc(side_right, pic_next)
            if result['right_done']:
                break
            i += 1

        for i in range(101):
            pic = self._renderer.render_to_left(side_left + side_right, pic_next, i)
            self._ui.draw(pic)

    def to_right(self):
        pic_current = self._storage.get_current()
        if pic_current is None:
            pic = self._renderer.render_default()
            self._ui.draw(pic)
            return

        side_right = [pic_current]
        i = 0
        while True:
            pic = self._storage.get_next(i)
            if pic is None:
                break
            side_right.append(pic)
            result = self._renderer.calc(side_right, pic_current)
            if result['right_done']:
                break
            i += 1

        self._storage.step_previous()
        pic_previous = self._storage.get_current()
        if pic_previous is None:
            pic_ui = self._renderer.render_to_right(side_right, pic_current, 100)
            self._ui.draw(pic_ui)
            return

        side_left = [pic_previous]
        i = 0
        while True:
            pic = self._storage.get_previous(i)
            if pic is None:
                break
            side_left.insert(0, pic)
            result = self._renderer.calc(side_left, pic_previous)
            if result['left_done']:
                break
            i += 1

        for i in range(101):
            pic = self._renderer.render_to_right(side_left + side_right, pic_previous, i)
            self._ui.draw(pic)
