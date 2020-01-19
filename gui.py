from typing import Callable

import pygame


def updater(obj_list, screen):
    for obj in obj_list:
        obj.update(screen)


def objects_resize(list_of_objects, screen):
    for obj in list_of_objects:
        obj.resize(screen)


def emit_event_to_objects(obj_list, event) -> (int or None):
    for obj in obj_list:
        a = obj.event_handler(event)
        if a is not None:
            print(a)
            return a
    return None


# All sizes stated in percent
class Label:
    x: int = 0
    y: int = 0
    size_x: int = 0
    size_y: int = 0
    rect = None
    text_color: pygame.Color = pygame.Color(0, 0, 0)
    text: str = ''
    font: str = 'Comic Sans MS'
    font_size = None
    fix: int = 0.1

    def __init__(self, x: 'x in percent', y, size_x, size_y):
        self.x, self.y, self.size_x, self.size_y = x, y, size_x, size_y

    def __text_resize(self, button_size, fix):
        lines = self.text.split('\n')
        max_height = 0
        max_width = 0
        best = 1
        for size in range(1, 1000):
            font = pygame.font.SysFont('Comic Sans MS', size)
            for i, elem in enumerate(lines):
                text = font.render(str(elem), 1, self.text_color)
                max_height = max(text.get_height(), max_height)
                max_width = max(text.get_width(), max_width)
            width = max_width + 10
            height = max_height * len(lines) - fix * (len(lines) - 2)
            if width >= button_size[0] or height >= button_size[1]:
                self.font_size = best
                return
            best = size

    def resize(self, screen):
        screen_height, screen_width = screen.get_height(), screen.get_width()
        self.rect = (int(screen_width * self.x / 100),
                     int(screen_height * self.y / 100),
                     int(screen_width * self.size_x / 100),
                     int(screen_height * self.size_y / 100),
                     int(screen_height * self.fix / 100))
        self.__text_resize((self.rect[2], self.rect[3]), self.rect[4])
        return

    def update(self, screen):
        if self.rect is None or self.font_size is None:
            self.resize(screen)
        lines = self.text.split('\n')
        font = pygame.font.SysFont(self.font, self.font_size)
        for i, line in enumerate(lines):
            text = font.render(str(line), 1, self.text_color)
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text,
                        (self.rect[0] + 5, self.rect[1] + (text_h - self.rect[4]) * i))

    # stubs
    @staticmethod
    def event_handler(event) -> None:
        return None


class PushButton:
    # Params of this class
    x: int = 0
    y: int = 0
    size_x: int = 0
    size_y: int = 0
    rect = None
    text_color: pygame.Color = pygame.Color(0, 0, 0)
    background_color: pygame.Color = pygame.Color(255, 255, 255)
    alpha: int = 200
    text: str = ''
    font: str = 'Comic Sans MS'
    font_size = None
    fix: int = 0.1
    handler: Callable = lambda: None
    in_handler: Callable = lambda x: None
    # flags of this class:
    triggered: bool = False

    def __init__(self, x: 'x in percent', y, size_x, size_y):
        self.x, self.y, self.size_x, self.size_y = x, y, size_x, size_y

    def event_handler(self, event) -> handler:
        if event.type == pygame.MOUSEMOTION:
            if self.collide(event.pos):
                self.triggered = True
            else:
                self.triggered = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collide(event.pos):
                return self.handler()

    def collide(self, mouse_pos):
        return mouse_pos[0] in range(self.rect[0], self.rect[2] + self.rect[0]) and \
               mouse_pos[1] in range(self.rect[1], self.rect[3] + self.rect[1])

    def __text_resize(self, button_size, fix):
        lines = self.text.split('\n')
        max_height = 0
        max_width = 0
        best = 1
        for size in range(1, 1000):
            font = pygame.font.SysFont('Comic Sans MS', size)
            for i, elem in enumerate(lines):
                text = font.render(str(elem), 1, self.text_color)
                max_height = max(text.get_height(), max_height)
                max_width = max(text.get_width(), max_width)
            width = max_width + 10
            height = max_height * len(lines) - fix * (len(lines) - 2)
            if width >= button_size[0] or height >= button_size[1]:
                self.font_size = best
                return
            best = size

    def resize(self, screen):
        screen_height, screen_width = screen.get_height(), screen.get_width()
        self.rect = (int(screen_width * self.x / 100),
                     int(screen_height * self.y / 100),
                     int(screen_width * self.size_x / 100),
                     int(screen_height * self.size_y / 100),
                     int(screen_height * self.fix / 100))
        self.__text_resize((self.rect[2], self.rect[3]), self.rect[4])
        return

    def update(self, screen):
        if self.rect is None or self.font_size is None:
            self.resize(screen)

        button = pygame.Surface((self.rect[2], self.rect[3]))
        button.fill(self.background_color)

        button.set_alpha(min(self.alpha + 50, 255) if self.triggered else self.alpha)
        screen.blit(button, (self.rect[0], self.rect[1]))
        lines = self.text.split('\n')
        font = pygame.font.SysFont(self.font, self.font_size)
        for i, line in enumerate(lines):
            text = font.render(str(line), 1, self.text_color)
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text,
                        (self.rect[0] + 5, self.rect[1] + (text_h - self.rect[4]) * i))


class GameMenu:
    from time import time
    buttons = list()
    height = 15
    rect = None

    def __init__(self):
        # next_wave = PushButton(0, 0, )
        # self.buttons.append()
        pass

    def event_handler(self, event):

        emit_event_to_objects(self.buttons, event)
        return None

    def resize(self, screen) -> None:
        screen_height, screen_width = screen.get_height(), screen.get_width()
        self.rect = (
            int(screen_width * 0 / 100),
            int(screen_height * (100 - self.height) / 100),
            int(screen_width),
            int(screen_height * self.height / 100)
        )
        return None

    def update(self, screen):
        if self.rect is None:
            self.resize(screen)
        menu = pygame.Surface(self.rect[2:])
        menu.fill(pygame.Color('black'))
        menu.set_alpha(80)
        pass
        updater(self.buttons, menu)
        screen.blit(menu, (self.rect[0], self.rect[1]))
        return None
