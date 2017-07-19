class Slider(object):
    
    def __init__(self, storage, renderer, ui):
        self._storage = storage
        self._renderer = renderer
        self._ui = ui

    def to_left(self):
        current = self._storage.get_current()
        if current is None:
            pic = self._renderer.render_default()
            self._ui.draw(pic)
            return

        i = 0
        while True:
            pic = self._storage.get_previous(i)
            if pic is None:
                break
            self._renderer.calc(None, None)
            i += 1

        self._storage.step_next()
        next = self._storage.get_current()

        i = 0
        while True:
            pic = self._storage.get_next(i)
            if pic is None:
                break
            self._renderer.calc(None, None)
            i += 1

        for i in range(0, 100):
            pic = self._renderer.render_to_left(None, None, i)
            self._ui.draw(pic)
