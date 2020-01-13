import pygame
# from main import SIZE
from pygame import Color


class Label:
    def __init__(self, x, y):
        self.text = ''
        self.x, self.y = x, y
        self.fix = 20
        self.text_color = Color(0, 0, 0)
        try:
            self.font = pygame.font.SysFont('mvboli', 34)
        except Exception as err:
            self.font = pygame.font.Font(None, 34)

    def move(self, x, y):
        self.x = x
        self.y = y

    def set_text(self, text):
        self.text = text

    def set_text_color(self, color: Color):
        self.text_color = color

    def set_font_size(self, size, fix=20):
        self.font = pygame.font.SysFont('mvboli', size)
        self.fix = fix

    def event_handler(self) -> None:
        pass

    def update(self, screen):
        lines = self.text.split('\n')
        for i, line in enumerate(lines):
            text = self.font.render(str(line), 1, self.text_color)
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (self.x + 5, self.y + 5 + (text_h - self.fix) * i))


class PushButton:
    def __init__(self, left, top, width, height):
        self.x, self.y, self.width, self.height = left, top, width, height
        self.triggered = False

        self.handler = lambda: None

        self.fix = 20
        self.text = ''
        self.text_color = Color(0, 0, 0)

        self.alpha = 100
        self.contour = False
        self.contour_fixed = False
        self.contour_width = 1
        self.contour_alpha = 200
        self.contour_color = Color(0, 0, 0)
        self.background_color = Color(0, 0, 0)

        try:
            self.font = pygame.font.SysFont('mvboli', 34)
        except Exception as err:
            self.font = pygame.font.Font(None, 34)

    def set_handler(self, func):
        del self.handler
        self.handler = func

    def set_text(self, text):
        self.text = text

    def set_font_size(self, size, fix=20):
        self.font = pygame.font.SysFont('mvboli', size)
        self.fix = fix

    def set_alpha(self, alpha):
        self.alpha = alpha

    def set_color(self, background_color: pygame.Color, text_color: pygame.Color) -> None:
        self.background_color = background_color
        self.text_color = text_color

    def set_contour(self, color=Color(255, 0, 0), line_width=5, contour_fixed=False) -> None:
        self.contour = True
        self.contour_color = color
        self.contour_fixed = contour_fixed
        self.contour_width = line_width

    def del_contour(self):
        self.contour = None

    def resize_by_text(self):
        lines = self.text.split('\n')
        max_height = 0
        max_width = 0
        for i, elem in enumerate(lines):
            text = self.font.render(str(elem), 1, self.text_color)
            max_height = max(text.get_height(), max_height)
            max_width = max(text.get_width(), max_width)
        self.width = max_width + 10
        self.height = (max_height - self.fix) * len(lines) + self.fix

    def event_handler(self, event):
        if event.type == pygame.MOUSEMOTION:
            flag1 = event.pos[0] in range(self.x, self.x + self.width + 1)
            flag2 = event.pos[1] in range(self.y, self.y + self.height + 1)
            if flag1 and flag2:
                self.triggered = True
            else:
                self.triggered = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = event.pos[0] in range(self.x, self.x + self.width + 1)
            flag2 = event.pos[1] in range(self.y, self.y + self.height + 1)
            if flag1 and flag2:
                del flag1, flag2
                self.handler()
                return

    def update(self, screen):
        button = pygame.Surface((self.width, self.height))
        button.fill(self.background_color)
        if self.contour:
            if self.contour_fixed:
                pygame.draw.rect(screen, self.contour_color, (self.x, self.y, self.width, self.height),
                                 self.contour_width)
            pygame.draw.rect(button, self.contour_color, (0, 0, self.width, self.height), self.contour_width)
        button.set_alpha(min(self.alpha + 50, 255) if self.triggered else self.alpha)
        screen.blit(button, (self.x, self.y))
        lines = self.text.split('\n')
        for i, line in enumerate(lines):
            text = self.font.render(str(line), 1, self.text_color)
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (self.x + 5, self.y + 5 + (text_h - self.fix) * i))
