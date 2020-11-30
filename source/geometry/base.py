class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Segment:
    def __init__(self, point1: Point, point2: Point):
        self.a = point1
        self.b = point2
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        self.len_x = x2 - x1
        self.len_y = y2 - y1
        self.seg_len = (self.len_x ** 2 + self.len_y ** 2) ** 0.5

    def len(self) -> int:
        return self.seg_len

    def point1(self) -> Point:
        return self.a

    def point2(self) -> Point:
        return self.b


def distance(point1: Point, point2: Point):
    return abs(((point2.y - point1.y) ** 2 + (point2.x - point1.x) ** 2) ** 0.5)


def near_point_on_segment(point: Point, seg: Segment):
    p1 = seg.point1()
    p2 = seg.point2()
    length = (p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) * (p1.y - p2.y)
    pr = (point.x - p1.x) * (p2.x - p1.x) + (point.y - p1.y) * (p2.y - p1.y)
    cf = pr / length
    if cf < 0:
        cf = 0
    if cf > 1:
        cf = 1
    x_res = p1.x + cf * (p2.x - p1.x)
    y_res = p1.y + cf * (p2.y - p1.y)
    return x_res, y_res


def distance_to_segment(point: Point, seg: Segment):
    return distance(point, near_point_on_segment(point, seg))
