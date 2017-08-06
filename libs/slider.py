from time import sleep


class Slider(object):
    
    def __init__(self, storage, renderer, ui):
        self._storage = storage
        self._renderer = renderer
        self._ui = ui

    def to_left(self):
        imgs_left = self._get_side_left(0)
        if not imgs_left:
            img_ui = self._renderer.render_default()
            self._ui.draw(img_ui)
            return
        img_current = imgs_left[-1]

        imgs_right = self._get_side_right(1)
        if not imgs_right:
            img_ui = self._renderer.render_to_left(imgs_left, img_current, 100)
            self._ui.draw(img_ui)
            return
        img_next = imgs_right[0]

        for i in range(101):
            pic = self._renderer.render_to_left(imgs_left + imgs_right, img_next, i)
            self._ui.draw(pic)
            sleep(0.001)
        self._storage.step_next()

    def to_right(self):
        imgs_right = self._get_side_right(0)
        if not imgs_right:
            img_ui = self._renderer.render_default()
            self._ui.draw(img_ui)
            return
        img_current = imgs_right[0]

        imgs_left = self._get_side_left(-1)
        if not imgs_left:
            img_ui = self._renderer.render_to_right(imgs_right, img_current, 100)
            self._ui.draw(img_ui)
            return
        img_previous = imgs_left[-1]

        for i in range(101):
            pic = self._renderer.render_to_right(imgs_left + imgs_right, img_previous, i)
            self._ui.draw(pic)
            sleep(0.001)
        self._storage.step_previous()

    def _get_side_left(self, offset):
        img_center = self._storage.get(offset)
        if img_center is None:
            return []
        result = [img_center]
        offset -= 1
        while True:
            attempt = self._renderer.calc(result, img_center)
            if attempt['left_done']:
                break
            img = self._storage.get(offset)
            if img is None:
                break
            result.insert(0, img)
            offset -= 1
        return result

    def _get_side_right(self, offset):
        img_center = self._storage.get(offset)
        if img_center is None:
            return []
        result = [img_center]
        offset += 1
        while True:
            attempt = self._renderer.calc(result, img_center)
            if attempt['right_done']:
                break
            img = self._storage.get(offset)
            if img is None:
                break
            result.append(img)
            offset += 1
        return result
