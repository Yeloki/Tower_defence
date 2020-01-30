from random import randint

from pygame import image, transform

from gui import PixelLabel
from other import distance

STATUSES = dict()
buffer = open('CONSTS', 'r')
for key, val in map(lambda x: (x.split()[0], int(x.split()[1])), buffer.readlines()):
    STATUSES[key] = val
buffer.close()
from other import rot_center

enemy = []
images = (transform.scale(image.load('images/enemy1.png'), (40, 40)),
          transform.scale(image.load('images/enemy2.png'), (40, 40)),
          transform.scale(image.load('images/enemy3.png'), (40, 40)),
          transform.scale(image.load('images/enemy4.png'), (40, 40)))
for j in range(4):
    enemy.append([])
    for i in range(359, -1, -1):
        enemy[j].append(rot_center(images[j], i))


class Enemy:
    r_size = 1
    i = 0
    wave = 1
    max_hp = 0
    abs_r_size = None
    game_map = None
    image = None
    alpha = 0
    last_image = None
    current_status = 'ENEMY_STATUS_A_LIFE'

    def __init__(self, game_map: list, wave=1, difficult=1) -> None:
        self.game_map = game_map
        self.wave = wave
        self.hp = 100 + (wave - 1) * (difficult * 7)
        self.max_hp = self.hp
        self.x, self.y = game_map[self.i].begin()
        self.speed = 1.8 + (difficult - 1) * 0.7

    def resize(self, screen):
        self.abs_r_size = self.r_size * 20

    def update(self, screen) -> int:
        if self.abs_r_size is None:
            self.resize(screen)
        if self.hp <= 0:
            return STATUSES['ENEMY_STATUS_DIED']

        text = int((self.hp / self.max_hp) * 100)
        lb = PixelLabel(int(self.x), int(self.y - self.abs_r_size * 1.5))
        lb.fix = 2
        lb.text = text
        # circle(screen, Color(0, 255, 0), (int(self.x), int(self.y)), self.abs_r_size)
        screen.blit(enemy[self.wave % 4][(self.alpha + 90 + randint(-5, 5)) % 360],
                    (int(self.x) - 20 + randint(-1, 1), int(self.y) - 20 + randint(-1, 1)))
        lb.update(screen)
        # print(self.alpha)
        return STATUSES[self.current_status]

    def move(self) -> None:
        # height, width = screen.get_height(), screen.get_width()
        from math import atan, degrees
        if distance((self.x, self.y), self.game_map[self.i].end()) <= self.speed:
            if self.i + 1 == len(self.game_map):
                self.current_status = 'ENEMY_STATUS_TO_GET_TO_BASE'
            else:
                self.i += 1
        self.x += self.speed * (self.game_map[self.i].len_x / self.game_map[self.i].len())
        self.y += self.speed * (self.game_map[self.i].len_y / self.game_map[self.i].len())
        self.alpha = int(degrees(atan((self.game_map[self.i].begin()[1] - self.game_map[self.i].end()[1]) /
                                      (self.game_map[self.i].begin()[0] - self.game_map[self.i].end()[0]))))

    def pos(self):
        return self.x, self.y

    def get_damage(self, damage) -> None:
        self.hp -= damage
        return
