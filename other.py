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
