
from pygame.locals import *

from .geometry.base import *
import json


class Base:

    def __init__(self, config):
        triggered = False
        self.x, self.y = config['x'], config['y']
        self.width = config['width']
        self.height = config['height']

    def update(self, screen, hp):
        surf = pygame.Surface((150, 100), SRCALPHA)
        if base_texture is not None:
            surf.blit(base_texture, (0, 0))
        else:
            pygame.draw.rect(surf, pygame.Color(255, 255, 255),
                             pygame.Rect(0, 0, self.width, self.height))
        for i in range(hp):
            if i < 5:
                surf.blit(hp_texture, (15 + 24 * i, 21))
            else:
                surf.blit(hp_texture, (15 + 24 * (i - 5), 55))
        screen.blit(surf, (self.x, self.y))


class GameMap:
    line_width = 25

    def __init__(self, path_to_map=LEVELS / "base.json"):
        self.background = pygame.image.load(TEXTURES / "base.png")

        level = json.load(open(path_to_map, 'r'))["level"]
        self.map = list()
        self.points = list()

        self.base = Base(level["base"])

    def update(self, screen, base_hp):
        screen_width, screen_height = screen.get_width(), screen.get_height()
        screen.blit(pygame.transform.scale(self.background, (screen_width, screen_height)), (0, 0))
        for seg in self.map:
            draw_better_line(screen, seg.point1(), seg.point2(), pygame.Color(0, 62, 141),
                             self.line_width)
        for dot in self.dots:
            pygame.draw.circle(screen, pygame.Color(0, 62, 141), [*dot], self.line_width)
        if base_hp > 0:
            self.base.update(screen, base_hp)
