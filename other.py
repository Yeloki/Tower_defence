from pygame import transform


class Segment:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.len_x = x2 - x1
        self.len_y = y2 - y1
        self.seg_len = (self.len_x ** 2 + self.len_y ** 2) ** 0.5

    def len(self) -> int:
        return self.seg_len

    def a(self) -> tuple:
        return self.x1, self.y1

    def b(self) -> tuple:
        return self.x2, self.y2


def distance(point1, point2):
    return abs(((point2[1] - point1[1]) ** 2 + (point2[0] - point1[0]) ** 2) ** 0.5)


def near_point_on_segment(point, vec: Segment):
    x, y = point
    x1, y1 = vec.a()
    x2, y2 = vec.b()
    length = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
    pr = (x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)
    cf = pr / length
    if cf < 0:
        cf = 0
    if cf > 1:
        cf = 1
    x_res = x1 + cf * (x2 - x1)
    y_res = y1 + cf * (y2 - y1)
    return x_res, y_res


def distance_to_segment(point, vec: Segment):
    return distance(point, near_point_on_segment(point, vec))


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    rot_image = transform.rotate(image, angle)
    rot_rect = image.get_rect().copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
