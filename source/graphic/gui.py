import math
from time import time
import pygame
from pygame import Color
from pygame.locals import *
from typing import Union, NoReturn, Callable
from consts import RESIZE_K, WIDTH, HEIGHT
from consts import USED_FONT
from source.geometry.base import Point


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
        super(Button, self).__init__(x, y, width, height, text)
        self.value = value
        self.rect = []

    def event_handler(self, event, fix_x=0, fix_y=0):
        if event.type == pygame.MOUSEMOTION:
            if self.collide(event.pos):
                self.triggered = True
            else:
                self.triggered = False
        if event.type == pygame.MOUSEBUTTONUP and self.flag:
            self.flag = False
            # print(1)
            if self.collide(event.pos):
                self.last_clicked_time = time()
                self.clicked = True
                return self.value
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.flag = True

    def collide(self, mouse_pos):
        return mouse_pos[0] in range(self.rect[0], self.rect[2] + self.rect[0]) and \
               mouse_pos[1] in range(self.rect[1], self.rect[3] + self.rect[1])

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

    def set_rect(self, screen):
        screen_height, screen_width = screen.get_height(), screen.get_width()
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
        font = pygame.font.SysFont(USED_FONT, self.font_size)
        for i, line in enumerate(lines):
            text = font.render(str(line), False, self.text_color)
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text,
                        ((self.rect[2] - text_w) // 2 + (self.rect[0]),
                         self.rect[1] + (text_h - self.rect[4]) * i))
