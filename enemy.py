from pygame import Color
from pygame.draw import circle
from other import Vector


class Enemy:
    r_size = 1
    i = 0
    abs_r_size = None
    game_map = None

    def __init__(self, game_map: list, wave=0, difficult=1) -> None:
        self.game_map = [Vector(*game_map[i], *game_map[i + 1]) for i in range(len(game_map))]
        self.hp = 10 + (wave - 1) * (difficult * 2)
        self.x, self.y = game_map[self.i][0]
        self.speed = 1 + (difficult - 1) * 0.5

    def resize(self, screen):
        self.abs_r_size = self.r_size * 10

    def update(self, screen) -> None:
        if self.abs_r_size is None:
            self.resize(screen)
        circle(screen, Color(0, 0, 0), (int(self.x), int(self.y)), self.abs_r_size)

    def move(self, screen=None) -> None:
        height, width = screen.get_height(), screen.get_width()
        import math
        self.x += self.speed * self.game_map[self.i].len

    def take_damage(self, damage) -> bool:
        self.hp -= damage
        return self.hp <= 0
