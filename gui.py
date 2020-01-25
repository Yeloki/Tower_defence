import math

import pygame

pygame.init()
NUMS = dict()
size = 18
font = pygame.font.SysFont('Comic Sans MS', size)
for i in range(101):
    NUMS[i] = font.render(str(i), 1, pygame.Color(0, 0, 0))
del font, i, size


def updater(obj_list, screen):
    for obj in obj_list:
        obj.update(screen)


def objects_resize(list_of_objects, screen):
    for obj in list_of_objects:
        obj.resize(screen)


def emit_event_to_objects(obj_list, event, fix_x=None, fix_y=None):
    for obj in obj_list:
        if fix_x is not None and fix_y is not None:
            a = obj.event_handler(event, fix_x, fix_y)
        elif fix_x is not None:
            a = obj.event_handler(event, fix_x)
        elif fix_y is not None:
            a = obj.event_handler(event, fix_y=fix_y)
        else:
            a = obj.event_handler(event)
        if a is not None:
            print(a)
            return a
    return None


def draw_better_line(screen, point1: tuple, point2: tuple, color, width):
    x1, y1, x2, y2 = *point1, *point2
    dx = x2 - x1
    dy = y2 - y1
    len = math.sqrt(dx * dx + dy * dy)
    udx = dx / len
    udy = dy / len
    perpx = -udy * width
    perpy = udx * width
    # "left" line start
    x1_ = x1 + perpx
    y1_ = y1 + perpy
    # "left" line end
    x2_ = x1_ + dx
    y2_ = y1_ + dy
    # "right" line start
    x1__ = x1 - perpx
    y1__ = y1 - perpy

    # "right" line start
    x2__ = x1__ + dx
    y2__ = y1__ + dy
    points = ((x1_, y1_), (x2_, y2_), (x2__, y2__), (x1__, y1__))
    pygame.draw.polygon(screen, color, points)
    pass


# All sizes stated in percent
class PercentLabel:
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

    def __init__(self, x, y, size_x, size_y):
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
    flag: bool = False
    font: str = 'Comic Sans MS'
    font_size = None
    fix: int = 0.1
    handler: None
    # flags of this class:
    triggered: bool = False

    def __init__(self, x: 'x in percent', y, size_x, size_y):
        self.x, self.y, self.size_x, self.size_y = x, y, size_x, size_y

    def event_handler(self, event, fix_x=0, fix_y=0):
        if event.type == pygame.MOUSEMOTION:
            if self.collide(event.pos, fix_x, fix_y):
                self.triggered = True
            else:
                self.triggered = False
        if event.type == pygame.MOUSEBUTTONUP and self.flag:
            self.flag = False
            print(1)
            if self.collide(event.pos, fix_x, fix_y):
                return self.handler
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.flag = True

    def collide(self, mouse_pos, fix_x=0, fix_y=0):
        return mouse_pos[0] in range(self.rect[0] + fix_x, self.rect[2] + self.rect[0] + fix_x) and \
               mouse_pos[1] in range(self.rect[1] + fix_y, self.rect[3] + self.rect[1] + fix_y)

    def __text_resize(self, button_size, fix):
        lines = self.text.split('\n')
        max_height = 0
        max_width = 0
        best = 1
        for size in range(1, 100):
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
            text_h = text.get_height()
            screen.blit(text,
                        (self.rect[0] + 5, self.rect[1] + (text_h - self.rect[4]) * i))


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
    def event_handler(event) -> None:
        return None


class GameMenu:
    buttons = list()
    labels = list()
    height = 15
    rect = None
    turret_id = None
    characteristics_labels = []
    count_of_characteristics = 0
    characteristics_upgrades_buttons = []

    def __init__(self):
        next_wave = PushButton(0, 0, 10, 50)
        next_wave.background_color = pygame.Color('red')
        next_wave.text_color = pygame.Color('black')
        next_wave.text = 'next\nwave'
        next_wave.handler = 1
        next_wave.alpha = 200

        build_inferno = PushButton(0, 50, 10, 50)
        build_inferno.background_color = pygame.Color('red')
        build_inferno.text_color = pygame.Color('black')
        build_inferno.text = 'build inferno\ntower'
        build_inferno.handler = 2
        build_inferno.alpha = 200

        self.time_before_new_wave = PercentLabel(85, 0, 15, 50)
        self.time_before_new_wave.text = '20'
        self.time_before_new_wave.text_color = pygame.Color(0, 0, 0)

        self.money_label = PercentLabel(85, 50, 15, 50)
        self.money_label.text = '30$'
        self.money_label.text_color = pygame.Color(0, 0, 0)

        for i in range(5):
            self.characteristics_labels.append(PercentLabel(10 * (i + 1), 0, 10, 50))
        for i in range(5):
            self.characteristics_upgrades_buttons.append(PushButton(10 * (i + 1), 50, 10, 50))
            self.characteristics_upgrades_buttons[i].alpha = 200
            self.characteristics_upgrades_buttons[i].background_color = pygame.Color('red')
            self.characteristics_upgrades_buttons[i].handler = i + 3
        self.buttons.append(next_wave)
        self.buttons.append(build_inferno)
        pass

    def load_upgrades(self, upgrades):
        pass

    def load_characteristics(self, characteristics):
        pass

    def event_handler(self, event):
        if self.rect is None:
            return
        if self.turret_id is not None:
            a = emit_event_to_objects(
                (*self.buttons, *self.characteristics_upgrades_buttons[:self.count_of_characteristics]), event,
                *self.rect[:2])
        else:
            a = emit_event_to_objects(self.buttons, event, *self.rect[:2])
        return a

    def resize(self, screen) -> None:
        screen_height, screen_width = screen.get_height(), screen.get_width()
        self.rect = (
            int(screen_width * 0 / 100),
            int(screen_height * (100 - self.height) / 100),
            int(screen_width),
            int(screen_height * self.height / 100)
        )
        return None

    def update(self, screen, time_to_next_wave, money, turret_id, turrets_list):
        self.turret_id = turret_id
        self.time_before_new_wave.text = 'Time before\nnext wave:' + str(time_to_next_wave)
        self.money_label.text = str(money) + '$'

        if self.rect is None:
            self.resize(screen)

        menu = pygame.Surface(self.rect[2:], pygame.SRCALPHA)
        menu.fill(pygame.Color(100, 50, 100, 100))

        self.money_label.update(menu)
        if self.turret_id is not None:

            for label, text in zip(self.characteristics_labels,
                                   turrets_list[self.turret_id].get_characteristics()):
                label.text = text
                label.update(menu)

            for button, text in zip(self.characteristics_upgrades_buttons,
                                    turrets_list[self.turret_id].get_costs_of_upgrades()):
                button.text = text
                button.update(menu)
            self.count_of_characteristics = len(turrets_list[self.turret_id].get_costs_of_upgrades())

        self.time_before_new_wave.update(menu)

        updater(self.buttons, menu)
        screen.blit(menu, (self.rect[0], self.rect[1]))

        return None
