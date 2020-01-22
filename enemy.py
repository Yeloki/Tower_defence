from pygame import Color
from pygame.draw import circle

from other import distance

STATUSES = dict()
buffer = open('CONSTS', 'r')
for key, val in map(lambda x: (x.split()[0], int(x.split()[1])), buffer.readlines()):
    STATUSES[key] = val
buffer.close()


class Enemy:
    r_size = 1
    i = 0
    abs_r_size = None
    game_map = None
    current_status = 'ENEMY_STATUS_A_LIFE'

    def __init__(self, game_map: list, wave=0, difficult=1) -> None:
        self.game_map = game_map
        self.hp = 50 + (wave - 1) * (difficult * 2)
        self.x, self.y = game_map[self.i].begin()
        self.speed = 1.8 + (difficult - 1) * 0.7

    def resize(self, screen):
        self.abs_r_size = self.r_size * 20

    def update(self, screen) -> int:
        if self.abs_r_size is None:
            self.resize(screen)
        if self.hp <= 0:
            return STATUSES['ENEMY_STATUS_DIED']
        circle(screen, Color(0, 255, 0), (int(self.x), int(self.y)), self.abs_r_size)
        return STATUSES[self.current_status]

    def move(self) -> None:
        # height, width = screen.get_height(), screen.get_width()
        if distance((self.x, self.y), self.game_map[self.i].end()) <= self.speed:
            if self.i + 1 == len(self.game_map):
                self.current_status = 'ENEMY_STATUS_TO_GET_TO_BASE'
            else:
                self.i += 1
        self.x += self.speed * (self.game_map[self.i].len_x / self.game_map[self.i].len())
        self.y += self.speed * (self.game_map[self.i].len_y / self.game_map[self.i].len())

    def pos(self):
        return self.x, self.y

    def get_damage(self, damage) -> None:
        self.hp -= damage
        return
