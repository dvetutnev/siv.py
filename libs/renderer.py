from PIL import Image
from math import ceil


class Renderer(object):

    def __init__(self, width, height, distance):
        self._width = width
        self._height = height
        self._distance = distance

    def calc(self, pics, pic_center):
        half_width_center = pic_center.width // (2 * (pic_center.height / self._height))
        center = pics.index(pic_center)

        fill_left = half_width_center
        left = center
        left_done = False
        for i in range(center - 1, -1, -1):
            left = i
            fill_left += pics[i].width // (pics[i].height / self._height)
            fill_left += self._distance
            if fill_left >= (self._width // 2):
                left_done = True
                break

        fill_right = half_width_center
        right = center
        right_done = False
        for pic in pics[center + 1::]:
            right += 1
            fill_right += pic.width // (pic.height / self._height)
            fill_right += self._distance
            if fill_right >= (self._width // 2):
                right_done = True
                break

        return {'left': left, 'left_done': left_done, 'right': right, 'right_done': right_done}

    def render_default(self):
        return Image.new('RGB', (self._width, self._height), 'black')

    def render_to_left(self, pics, pic_next, shift):
        idx_next = pics.index(pic_next)
        pics = self._normalize_pictures(pics)
        tape = self._make_tape(pics)

        center = sum(p.width + self._distance for p in pics[:idx_next - 1:])
        center += int(pics[idx_next - 1].width / 2)
        p_current, p_next = pics[idx_next - 1], pics[idx_next]
        center += int((ceil(p_current.width / 2) + self._distance + int(p_next.width / 2)) * (shift / 100))
        half_width = int(self._width / 2)

        left = center - half_width
        right = center + self._width - half_width
        return self._normalize_tape(tape, left, right)

    def render_to_right(self, pics, pic_next, shift):
        idx_next = pics.index(pic_next)
        pics = self._normalize_pictures(pics)
        tape = self._make_tape(pics)

        center = sum(p.width + self._distance for p in pics[:idx_next + 1:])
        center += int(pics[idx_next + 1].width / 2)
        p_current, p_next = pics[idx_next + 1], pics[idx_next]
        center -= ceil((int(p_current.width / 2) + self._distance + ceil(p_next.width / 2)) * (shift / 100))
        half_width = int(self._width / 2)

        left = center - half_width
        right = center + self._width - half_width
        return self._normalize_tape(tape, left, right)

    def _normalize_pictures(self, pics):
        result = []
        for pic in pics:
            width = int(pic.width * (self._height / pic.height))
            p = pic.resize((width, self._height))
            result.append(p)
        return result

    def _make_tape(self, pics):
        widths = (p.width for p in pics)
        total_width = sum(widths) + (self._distance * (len(pics) - 1))
        tape = Image.new('RGB', (total_width, self._height), 'black')
        offset = 0
        for p in pics:
            tape.paste(p, (offset, 0))
            offset += p.width + self._distance
        return tape

    def _normalize_tape(self, tape, left, right):
        if left > 0 or right < tape.width:
            offset_left = max(left, 0)
            offset_right = min(right, tape.width)
            box = (offset_left, 0, offset_right, self._height)
            tape = tape.crop(box)
        if tape.width < self._width:
            result_tape = Image.new('RGB', (self._width, self._height), 'black')
            offset = max(0, -left)
            result_tape.paste(tape, (offset, 0))
            tape = result_tape
        return tape
