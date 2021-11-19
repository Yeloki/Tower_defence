from pygame.surface import Surface
import pygame
from pygame import mouse
from pygame import key
from pygame.locals import *


class Drawable:
    def __init__(self, x, y, size_x, size_y):
        self.rect = (x, y, size_x, size_y)
        self.updated = True

    def set_rect(self, rect):
        self.rect = rect

    def get_rect(self):
        return self.rect

    def update(self):
        pass

    def render(self):
        self.surf = Surface((self.rect[2], self.rect[3]), SRCALPHA)

    def draw(self, screen: pygame.Surface):
        if self.updated:
            self.render()
            self.updated = False
        screen.blit(self.surf, (self.rect[0], self.rect[1]))


class ClickableDrawable(Drawable):
    def __init__(self, x, y, size_x, size_y):
        super(ClickableDrawable, self).__init__(x, y, size_x, size_y)
        self.collided = False
        self.pushed = False
        self.clicked = False
        self.handler = None

    def connect(self, func):
        self.handler = func

    def collide(self, mx, my):
        if self.rect[0] <= mx <= self.rect[0] + self.rect[2]:
            if self.rect[1] <= my <= self.rect[1] + self.rect[3]:
                return True
        return False

    def render(self):
        super(ClickableDrawable, self).render()
        if self.pushed:
            self.surf.fill(pygame.Color((180, 180, 180)))
        elif self.collided:
            pass
            self.surf.fill(pygame.Color((220, 220, 220)))
        else:
            self.surf.fill(pygame.Color((255, 255, 255)))

    def update(self):
        super(ClickableDrawable, self).update()
        if self.collide(*mouse.get_pos()) and not self.collided:
            self.collided = True
            self.updated = True
        if not self.collide(*mouse.get_pos()) and self.collided:
            self.collided = False
            self.updated = True
        if self.collided and mouse.get_pressed(3)[0] and not self.pushed:
            self.pushed = True
            self.updated = True
        if self.collided and self.pushed and not mouse.get_pressed(3)[0]:
            self.pushed = False
            self.clicked = True
            self.updated = True
        if self.clicked and self.handler is not None:
            self.handler()
            self.clicked = False


class TextLabel(Drawable):
    def __init__(self, x, y, size_x, size_y):
        super(TextLabel, self).__init__(x, y, size_x, size_y)
        self.text = "No Text"
        self.background_color = None
        self.text_color = None

    def set_style(self, bg_color=None, text_color=None):
        self.background_color = bg_color
        self.text_color = text_color
        self.updated = True

    def set_text(self, text):
        self.text = text
        self.updated = True

    def render(self):
        super(TextLabel, self).render()
        if self.background_color is not None:
            self.surf.fill(self.background_color)
        lines = self.text.split('\n')
        l, r = 0, 100
        while r - l > 1:
            m = (l + r) // 2
            font = pygame.font.SysFont("arial", m)
            max_height = 0
            max_width = 0
            for elem in lines:
                text = font.render(str(elem), False, Color("black"))
                max_height = max(text.get_height(), max_height)
                max_width = max(text.get_width(), max_width)
            width = max_width + 10
            height = max_height * len(lines)
            if width > self.rect[2] or height > self.rect[3]:
                r = m
            else:
                l = m
        font = pygame.font.SysFont("arial", l)
        for i, line in enumerate(lines):
            if self.text_color is not None:
                text = font.render(str(line), True, self.text_color)
            else:
                text = font.render(str(line), True, Color("black"))
            text_h = text.get_height()
            self.surf.blit(text, ((self.rect[2] - text.get_width()) // 2, max_height * i))


class Button(ClickableDrawable):
    def __init__(self, x, y, size_x, size_y):
        super(Button, self).__init__(x, y, size_x, size_y)
        self.label = TextLabel(x, y, size_x, size_y)

    def set_text(self, text):
        self.label.set_text(text)

    def render(self):
        super(Button, self).render()
        self.label.render()

    def set_rect(self, rect):
        super(Button, self).set_rect(rect)
        self.label.set_rect(rect)

    def draw(self, screen: pygame.Surface):
        if self.label.updated or self.updated:
            self.label.render()
        super(Button, self).draw(screen)
        self.label.draw(screen)
