from pygame import display


class Layout:
    class LayoutElement:
        def __init__(self, elem):
            self.origin_rect = elem.get_rect()
            self.elem = elem

        def resize_render(self, percentX, percentY):
            new_rect = [0, 0, 0, 0]
            new_rect[0] = self.origin_rect[0] * percentX // 100
            new_rect[1] = self.origin_rect[1] * percentY // 100
            new_rect[2] = self.origin_rect[2] * percentX // 100
            new_rect[3] = self.origin_rect[3] * percentY // 100
            self.elem.set_rect(tuple(new_rect))
            self.elem.updated = True

        def draw(self, screen):
            self.elem.draw(screen)

        def update(self):
            self.elem.update()

    def __init__(self):
        """
        if you want to use this layout you must define this functions:
        set_rect()
        get_rect()
        """
        self.start_size = display.get_window_size()
        self.cur_size = display.get_window_size()
        self.updated = False
        self.data = []

    def draw(self, screen):
        if self.updated:
            self.render()
            self.updated = False
        for elem in self.data:
            elem.draw(screen)

    def render(self):
        new_size = display.get_window_size()
        percent_x = int((new_size[0] / self.start_size[0] ) * 100)
        percent_y = int((new_size[1] / self.start_size[1]) * 100)
        self.cur_size = new_size
        for elem in self.data:
            elem.resize_render(percent_x, percent_y)

    def add_element(self, elem):
        self.data.append(self.LayoutElement(elem))

    def update(self):
        if self.cur_size != display.get_window_size():
            self.updated = True
        for elem in self.data:
            elem.update()
