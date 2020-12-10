import pygame
from pygame import transform
from .gui import BasePercentRect


class BaseExplosion(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, surface):
        ln = len(self.frames)
        self.cur_frame = (self.cur_frame + 1) % ln
        self.image = self.frames[self.cur_frame]
        surface.blit(self.image, self.rect)
        return self.cur_frame == ln - 1


class Texture(BasePercentRect):
    def __init__(self, x, y, width, height, path):
        super(Texture, self).__init__(x, y, width, height)
        self.img = pygame.image.load(path)

    def render(self, screen_width, screen_height):
        super(Texture, self).render(screen_width, screen_height)
        self.surf.blit(pygame.transform.scale(self.img, (screen_width, screen_height)), (0, 0))


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    rot_image = transform.rotate(image, angle)
    rot_rect = image.get_rect().copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image
