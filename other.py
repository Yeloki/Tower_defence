from pygame import transform


class Vector:
    def __init__(self, x1, y1, x2, y2):
        self.x_begin, self.y_begin = x1, y1
        self.x_end, self.y_end = x2, y2
        self.len_x = x2 - x1
        self.len_y = y2 - y1
        self.vec_len = (self.len_x ** 2 + self.len_y ** 2) ** 0.5

    def len(self) -> int:
        return self.vec_len

    def begin(self) -> tuple:
        return self.x_begin, self.y_begin

    def end(self) -> tuple:
        return self.x_end, self.y_end


def distance(point1, point2):
    return abs(((point2[1] - point1[1]) ** 2 + (point2[0] - point1[0]) ** 2) ** 0.5)


def distance_to_vector(point1, vec: Vector):
    x, y = point1
    x1, y1 = vec.begin()
    x2, y2 = vec.end()
    l = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
    pr = (x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)
    cf = pr / l
    if cf < 0:
        cf = 0
    if cf > 1:
        cf = 1
    x_res = x1 + cf * (x2 - x1)
    y_res = y1 + cf * (y2 - y1)
    return distance(point1, (x_res, y_res))


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
