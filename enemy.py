from random import randint
from time import time

from consts import enemy, STATUSES
from gui import PixelLabel
from other import distance


class Enemy:
    r_size = 1
    i = 0
    wave = 1
    max_hp = 0
    abs_r_size = None
    game_map = None
    image = None
    angle = 0
    last_image = None
    current_status = 'ENEMY_STATUS_A_LIFE'

    def __init__(self, game_map: list, wave=1, difficult=1) -> None:
        self.freeze_time = 0
        self.time_last_freeze = time()
        self.freeze_flag = False

        self.burn_flag = False
        self.burn_time = 0
        self.time_last_burn = time()
        self.burn_damage = 0

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
        text = int((self.hp / self.max_hp) * 100)
        if self.hp <= 0 or text == 0:
            return STATUSES['ENEMY_STATUS_DIED']

        lb = PixelLabel(int(self.x), int(self.y - self.abs_r_size * 1.5))
        lb.fix = 2
        lb.text = text
        enemy_type = 3 if self.burn_flag else 2 if self.freeze_flag else 0
        screen.blit(enemy[enemy_type][self.angle],
                    (int(self.x - 20 + randint(-1, 1) / 2), int(self.y - 20 + randint(-1, 1) / 2)))
        lb.update(screen)
        return STATUSES[self.current_status]

    def freeze(self, freeze_time):
        self.time_last_freeze = time()
        self.freeze_time = freeze_time
        self.freeze_flag = True
        self.burn_flag = False

    def burn(self, burn_time, burn_damage):
        self.time_last_burn = time()
        self.burn_time = burn_time
        self.burn_damage = burn_damage
        self.freeze_flag = False
        self.burn_flag = True

    def move(self) -> None:
        from math import atan, degrees
        if self.freeze_flag:
            speed = self.speed / 2
            if time() - self.time_last_freeze >= self.freeze_time:
                self.freeze_flag = False
        else:
            speed = self.speed
        if self.burn_flag:
            self.get_damage(self.burn_damage)
            if time() - self.time_last_burn >= self.burn_time:
                self.burn_flag = False
        print(self.i)
        print(speed)
        print(distance((self.x, self.y), self.game_map[self.i].end()))
        if distance((self.x, self.y), self.game_map[self.i].end()) <= speed * 2:
            if self.i + 1 == len(self.game_map):
                self.current_status = 'ENEMY_STATUS_TO_GET_TO_BASE'
            else:
                if distance((self.x, self.y), self.game_map[self.i].end()) > speed:
                    self.x += speed * (self.game_map[self.i].len_x / self.game_map[self.i].len())
                    self.y += speed * (self.game_map[self.i].len_y / self.game_map[self.i].len())
                self.i += 1

        self.x += speed * (self.game_map[self.i].len_x / self.game_map[self.i].len())
        self.y += speed * (self.game_map[self.i].len_y / self.game_map[self.i].len())
        print(self.i)
        if self.x < 0:
            print(self.game_map[self.i].begin(), self.game_map[self.i].end())

        print((self.game_map[self.i].len_x / self.game_map[self.i].len()))
        try:
            k = 0
            tan = (self.game_map[self.i].begin()[1] - self.game_map[self.i].end()[1]) / \
                  (self.game_map[self.i].begin()[0] - self.game_map[self.i].end()[0])
            if ((self.game_map[self.i].begin()[1] - self.game_map[self.i].end()[1]) > 0 and
                (self.game_map[self.i].begin()[0] - self.game_map[self.i].end()[0]) > 0) or \
                    ((self.game_map[self.i].begin()[1] - self.game_map[self.i].end()[1]) <= 0 < (
                            self.game_map[self.i].begin()[0] - self.game_map[self.i].end()[0])):
                k = -180
            self.angle = (90 + int(degrees(atan(tan))) + randint(-2, 2) + k) % 360
        except ZeroDivisionError:
            self.angle = randint(-2, 2) % 360

    def pos(self):
        return self.x, self.y

    def get_damage(self, damage) -> None:
        self.hp -= damage
        return
