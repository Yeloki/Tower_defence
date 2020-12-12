import math
from time import time
import pygame
from pygame import Color
from pygame.locals import *
from typing import Union, NoReturn, Callable
from consts import RESIZE_K, WIDTH, HEIGHT
from consts import USED_FONT


class BasePercentRect:
    def __init__(self, x, y, width, height, background_color=None):
        self.x, self.y, self.width, self.height = x, y, width, height
        self.surf: Union[pygame.Surface, None] = None
        self.background_color = background_color

    def check_render(self) -> bool:
        return (self.surf is None) or (self.surf.get_height() != self.height * RESIZE_K) or (
                self.surf.get_width() != self.width * RESIZE_K)

    def render(self, screen_width, screen_height) -> NoReturn:
        if self.check_render():

            self.surf = pygame.Surface((screen_width, screen_height), SRCALPHA)
            if self.background_color is not None:
                pygame.draw.rect(self.surf, self.background_color, (0, 0, self.width, self.height))

    def draw(self, screen: pygame.Surface) -> NoReturn:
        self.render(screen.get_width(), screen.get_height())
        screen.blit(self.surf, (self.x * RESIZE_K, self.y * RESIZE_K))


class TextLabel(BasePercentRect):
    event_handler = (lambda event: None)

    def __init__(self, x, y, width, height,
                 text: str, font=USED_FONT,
                 font_size: int = 20,
                 text_color=Color(0, 0, 0),
                 background_color=None
                 ):
        super(TextLabel, self).__init__(x, y, width, height, background_color)
        self.text = text
        self.font_size = font_size
        self.font = font
        self.text_color = text_color

    def render(self, screen_width, screen_height) -> NoReturn:
        super(TextLabel, self).render(screen_width, screen_width)
        lines = self.text.split('\n')
        font = pygame.font.SysFont(USED_FONT, self.font_size)
        for i, line in enumerate(lines):
            text = font.render(str(line), True, self.text_color)
            self.surf.blit(text, ((self.width - text.get_width()) / 2, text.get_height() * i))


class Button(TextLabel):
    def __init__(self, x, y, width, height,
                 text: str,
                 value: int,
                 font=USED_FONT,
                 font_size: int = 20,
                 text_color=Color(0, 0, 0),
                 background_color=None):
        super(Button, self).__init__(x, y, width, height,
                                     text, font, font_size,
                                     text_color, background_color)
        self.value = value
        self.is_active = False
        self.is_pushed = False

    def event_handler(self, event):
        pass

    def collide(self, mouse_pos):
        return (self.x <= mouse_pos[0] <= self.x + self.width and
                self.y <= mouse_pos[1] <= self.y + self.height)
