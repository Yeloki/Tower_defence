import math
from time import time
import pygame

from ...consts import RESIZE_K, WIDTH, HEIGHT

class BasePercentRect:
    def __init__(self):
        self.rect = [Po]


class PercentLabel:
    x: int = 0
    y: int = 0
    size_x: int = 0
    size_y: int = 0
    rect = None
    text_color: pygame.Color = pygame.Color(0, 0, 0)
    text: str = ''
    font_size = None

    def __init__(self, x, y, size_x, size_y):
        self.x, self.y, self.size_x, self.size_y = x, y, size_x, size_y

    def __text_resize(self, button_size, fix):
        lines = self.text.split('\n')
        max_height = 0
        max_width = 0
        best = 1
        for size in range(1, 100):
            font = pygame.font.SysFont(used_font, size)
            for i, elem in enumerate(lines):
                text = font.render(str(elem), False, self.text_color)
                max_height = max(text.get_height(), max_height)
                max_width = max(text.get_width(), max_width)
            width = max_width + 10
            height = max_height * len(lines) - fix * (len(lines) - 2)
            if width >= button_size[0] or height >= button_size[1]:
                self.font_size = best
                return
            best = size

    def set_rect(self, screen):
        screen_height, screen_width = screen.get_height(), screen.get_width()
        self.rect = (int(screen_width * self.x / 100),
                     int(screen_height * self.y / 100),
                     int(screen_width * self.size_x / 100),
                     int(screen_height * self.size_y / 100))
        self.__text_resize((self.rect[2], self.rect[3]), self.rect[4])
        return

    def update(self, screen):
        if self.rect is None or self.font_size is None:
            self.set_rect(screen)
        lines = self.text.split('\n')
        font = pygame.font.SysFont(used_font, self.font_size)
        for i, line in enumerate(lines):
            text = font.render(str(line), False, self.text_color)
            text_h = text.get_height()
            screen.blit(text,
                        (self.rect[0] + 5, self.rect[1] + (text_h - self.rect[4]) * i))

    # stubs2
    @staticmethod
    def event_handler(_) -> None:
        return None


class PushButton:
    # Params of this class

    def __init__(self, x: 'x in percent', y, size_x, size_y):
        self.text_color: pygame.Color = pygame.Color(0, 0, 0)
        self.text: str = ''
        self.fix = 0.1
        self.alpha: int = 200
        self.rect = None
        self.style = None
        self.handler = None
        self.font_size = None
        # flags of this class:
        self.flag: bool = False
        self.triggered: bool = False

        self.last_clicked_time = 0
        self.clicked = False
        self.clicked_style = None
        self.x, self.y, self.size_x, self.size_y = x, y, size_x, size_y

    def event_handler(self, event, fix_x=0, fix_y=0):
        if event.type == pygame.MOUSEMOTION:
            if self.collide(event.pos, fix_x, fix_y):
                self.triggered = True
            else:
                self.triggered = False
        if event.type == pygame.MOUSEBUTTONUP and self.flag:
            self.flag = False
            # print(1)
            if self.collide(event.pos, fix_x, fix_y):
                self.last_clicked_time = time()
                self.clicked = True
                return self.handler
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.flag = True

    def collide(self, mouse_pos, fix_x=0, fix_y=0):
        return mouse_pos[0] in range(self.rect[0] + fix_x, self.rect[2] + self.rect[0] + fix_x) and \
               mouse_pos[1] in range(self.rect[1] + fix_y, self.rect[3] + self.rect[1] + fix_y)

    def set_style(self, image):
        if self.rect is not None:
            self.style = pygame.transform.scale(image, self.rect[2:-1])
        else:
            self.style = image

    def set_clicked_style(self, image):
        self.clicked_style = image
        if self.rect is not None:
            self.clicked_style = pygame.transform.scale(image, self.rect[2:-1])
        else:
            self.style = image

    def __text_resize(self, button_size, fix):
        lines = self.text.split('\n')
        max_height = 0
        max_width = 0
        best = 1
        for size in range(1, 100):
            font = pygame.font.SysFont(used_font, size)
            for i, elem in enumerate(lines):
                text = font.render(str(elem), False, self.text_color)
                max_height = max(text.get_height(), max_height)
                max_width = max(text.get_width(), max_width)
            width = max_width + 10
            height = max_height * len(lines) - fix * (len(lines) - 2)
            if width >= button_size[0] or height >= button_size[1]:
                self.font_size = best
                return
            best = size

    def set_rect(self, screen):
        screen_height, screen_width = screen.get_height(), screen.get_width()
        self.rect = (int(screen_width * self.x / 100),
                     int(screen_height * self.y / 100),
                     int(screen_width * self.size_x / 100),
                     int(screen_height * self.size_y / 100),
                     int(screen_height * self.fix / 100))
        self.__text_resize((self.rect[2], self.rect[3]), self.rect[4])
        if self.style is not None:
            self.style = pygame.transform.scale(self.style, self.rect[2:-1])
        if self.clicked_style is not None:
            self.clicked_style = pygame.transform.scale(self.clicked_style, self.rect[2:-1])
        return

    def update(self, screen):
        if self.rect is None or self.font_size is None:
            self.set_rect(screen)

        button = pygame.Surface((self.rect[2], self.rect[3]))
        if self.clicked:
            button.blit(self.clicked_style, (0, 0))
            if time() - self.last_clicked_time >= 0.1:
                self.clicked = False
        else:
            button.blit(self.style, (0, 0))
        button.set_alpha(min(self.alpha + 50, 255) if self.triggered else self.alpha)

        screen.blit(button, (self.rect[0], self.rect[1]))
        lines = self.text.split('\n')
        font = pygame.font.SysFont(used_font, self.font_size)
        for i, line in enumerate(lines):
            text = font.render(str(line), False, self.text_color)
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text,
                        ((self.rect[2] - text_w) // 2 + (self.rect[0]),
                         self.rect[1] + (text_h - self.rect[4]) * i))


class PixelLabel:
    x: int = 0
    y: int = 0
    rect = None
    text = 0
    font_size = None
    fix: int = 10

    def __init__(self, x, y):
        self.x, self.y = x, y

    def update(self, screen):
        text = NUMS[self.text]
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (self.x - text_w // 2, self.y - (text_h // 2)))

    # stubs
    @staticmethod
    def event_handler(_) -> None:
        return None
