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
