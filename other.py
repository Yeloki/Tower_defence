class Vector:
    def __init__(self, x1, y1, x2, y2):
        self.x_begin, self.y_begin = x1, y1
        self.x_end, self.y_end = x2, y2
        self.len_x = x2 - x1
        self.len_y = y2 - y1
        self.len = (self.len_x ** 2 + self.len_y ** 2) ** 0.5

    def __len__(self) -> int:
        return self.len

    def begin(self) -> tuple:
        return self.x_begin, self.y_begin

    def end(self) -> tuple:
        return self.x_end, self.y_end
