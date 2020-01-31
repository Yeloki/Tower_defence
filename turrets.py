from math import atan, degrees
from time import time

from pygame import Color, Surface
from pygame import image, transform
from pygame.draw import circle
from pygame.locals import *

from other import distance, rot_center, Vector

inferno1 = transform.scale(image.load('images/3.jpg'), (40, 40))
inferno2 = transform.scale(image.load('images/4.jpg'), (40, 40))
inferno3 = transform.scale(image.load('images/2.jpg'), (40, 40))
inferno4 = transform.scale(image.load('images/5.jpg'), (40, 40))
laser_tower = list()
inferno1.set_colorkey(Color(255, 255, 255))
inferno2.set_colorkey(Color(255, 255, 255))
inferno3.set_colorkey(Color(255, 255, 255))
inferno4.set_colorkey(Color(255, 255, 255))
image = transform.scale(image.load('images/1.jpg'), (80, 80))
image.set_colorkey(Color(255, 255, 255))
for i in range(359, -1, -1):
    laser_tower.append(rot_center(image, i))

del image


# inferno = [inferno1, inferno2, inferno3, inferno4]

class InfernoTower:
    radius_size = 20
    # damage
    damage = 120

    damage_update_cost = 20
    damage_update_value = 60
    i = 1  # count of updates (damage)
    max_upgrade_damage_count = 10

    # range
    range_of_attack = 200
    j = 1  # count of updates (range)
    range_update_cost = 10
    range_update_value = 25
    max_upgrade_range_count = 10

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.triggered = False
        self.target_id = -1

    def update(self, screen, enemies) -> (None, (Vector, Color)):
        surface = Surface((self.range_of_attack * 2, self.range_of_attack * 2), SRCALPHA)
        if self.triggered:
            circle(surface, Color(0, 255, 0, 25), (self.range_of_attack, self.range_of_attack), self.range_of_attack)
        colors = ((Color(255, 255, 255), Color(255, 255, 255)),
                  (Color(50, 50, 255), Color(0, 242, 255)),
                  (Color(50, 255, 50), Color(100, 242, 0)),
                  (Color(255, 50, 50), Color(246, 242, 0)))
        if 1 <= self.i + self.j <= 5:
            surface.blit(inferno1, (self.range_of_attack - self.radius_size, self.range_of_attack - self.radius_size))
            screen.blit(surface, (self.x - self.range_of_attack, self.y - self.range_of_attack))
            color_key = 0

        elif 6 <= self.i + self.j <= 12:
            surface.blit(inferno2, (self.range_of_attack - self.radius_size, self.range_of_attack - self.radius_size))
            screen.blit(surface, (self.x - self.range_of_attack, self.y - self.range_of_attack))
            color_key = 1

        elif 13 <= self.i + self.j <= 19:
            surface.blit(inferno3, (self.range_of_attack - self.radius_size, self.range_of_attack - self.radius_size))
            screen.blit(surface, (self.x - self.range_of_attack, self.y - self.range_of_attack))
            color_key = 2
        else:
            surface.blit(inferno4, (self.range_of_attack - self.radius_size, self.range_of_attack - self.radius_size))
            screen.blit(surface, (self.x - self.range_of_attack, self.y - self.range_of_attack))
            color_key = 3

        if self.target_id == -1 or self.target_id not in enemies:
            return
        return Vector(*self.pos(), *enemies[self.target_id].pos()), colors[color_key]

    # def description(self):
    #     return ''

    def upgrade(self, type_of_characteristics):
        if type_of_characteristics == 0 and self.i != self.max_upgrade_damage_count:
            self.damage += self.damage_update_value
            self.damage_update_cost += 20 * self.i
            self.i += 1
        if type_of_characteristics == 1 and self.j != self.max_upgrade_range_count:
            self.range_of_attack += self.range_update_value
            self.range_update_cost += 20 * self.j
            self.j += 1

    def range(self):
        return self.range_of_attack

    def disable_trigger(self):
        self.triggered = False

    def pos(self):
        return self.x, self.y

    def set_target(self, enemy_id):
        self.target_id = enemy_id

    def enable_trigger(self):
        self.triggered = True

    def shoot(self, enemies):
        if self.target_id == -1 or self.target_id not in enemies:
            return
        if distance(enemies[self.target_id].pos(), self.pos()) >= self.range_of_attack:
            self.target_id = -1
            return
        # enemies[self.target_id].get_damage(self.damage // 60)
        enemies[self.target_id].burn(0.5, self.damage / 60)

    def get_characteristics(self):
        out = [self.i, self.j]
        return tuple(zip(('damage:\n' + str(self.damage), 'range:\n' + str(self.range_of_attack)), out))

    def get_costs_of_upgrades(self):
        out = [self.damage_update_cost, self.range_update_cost]
        out2 = [self.i, self.j]
        return tuple(zip(('Upgrade damage\nCost:' + str(self.damage_update_cost), 'Upgrade range\nCost: ' + str(
            self.range_update_cost)), out, out2))

    def characteristics(self):
        out = [self.i, self.j]
        return tuple(zip((self.damage_update_cost, self.range_update_cost), out))


def prototype(screen, pos: (int, int), r, turret_range, collision: bool):
    surface = Surface((turret_range * 2, turret_range * 2), SRCALPHA)
    circle(surface, Color(0, 255, 0, 50), (turret_range, turret_range), turret_range)
    circle(surface, Color(0, 255, 0) if not collision else Color(255, 0, 0), (turret_range, turret_range), r)
    screen.blit(surface, (pos[0] - turret_range, pos[1] - turret_range))


class LaserTower:
    radius_size = 20
    # damage

    damage = 60
    damage_update_cost = 20
    damage_update_value = 60
    i = 1  # count of updates (damage)
    max_upgrade_damage_count = 10

    # range
    range_of_attack = 200
    j = 1  # count of updates (range)
    range_update_cost = 10
    range_update_value = 25
    max_upgrade_range_count = 10

    rate = 1
    h = 1  # count of updates (rate)
    rate_update_cost = 10
    rate_upgrade_value = 1
    max_upgrade_rate_count = 10

    def __init__(self, x, y):
        self.shoot_flag = False
        self.last_shoot_time = time()
        self.angle = 0
        self.triggered = False
        self.target_id = -1
        self.x, self.y = x, y

    def pos(self):
        return self.x, self.y

    def range(self):
        return self.range_of_attack

    def disable_trigger(self):
        self.triggered = False

    def set_target(self, enemy_id):
        self.target_id = enemy_id

    def enable_trigger(self):
        self.triggered = True

    def upgrade(self, type_of_characteristics):
        if type_of_characteristics == 0 and self.i != self.max_upgrade_damage_count:
            self.damage += self.damage_update_value
            self.damage_update_cost += 20 * self.i
            self.i += 1
        if type_of_characteristics == 1 and self.j != self.max_upgrade_range_count:
            self.range_of_attack += self.range_update_value
            self.range_update_cost += 20 * self.j
            self.j += 1
        if type_of_characteristics == 2 and self.h != self.max_upgrade_rate_count:
            self.rate += self.rate_upgrade_value
            self.rate_update_cost += 20 * self.h
            self.h += 1

    def shoot(self, enemies):
        if self.target_id == -1 or self.target_id not in enemies:
            return
        if distance(enemies[self.target_id].pos(), self.pos()) >= self.range_of_attack:
            self.target_id = -1
            return
        if time() - self.last_shoot_time >= 1 / self.rate:
            self.last_shoot_time = time()
            self.shoot_flag = True
            enemies[self.target_id].get_damage(self.damage)
            enemies[self.target_id].freeze(0.3)

    def get_characteristics(self):
        out = [self.i, self.j, self.h]
        return tuple(zip(('damage:\n' + str(self.damage),
                          'range:\n' + str(self.range_of_attack),
                          'rate:\n' + str(self.rate)
                          ), out))

    def get_costs_of_upgrades(self):
        out = [self.damage_update_cost, self.range_update_cost, self.rate_update_cost]
        out2 = [self.i, self.j, self.h]
        return tuple(zip(('Upgrade damage\nCost:' + str(self.damage_update_cost),
                          'Upgrade range\nCost: ' + str(self.range_update_cost),
                          'Upgrade rate\nCost: ' + str(self.rate_update_cost)
                          ), out, out2))

    def characteristics(self):
        out = [self.i, self.j, self.h]
        return tuple(zip((self.damage_update_cost,
                          self.range_update_cost,
                          self.rate_update_cost
                          ), out))

    # def description(self):
    #     return ''

    def update(self, screen, enemies) -> (None, (Vector, Color)):
        surface = Surface((self.range_of_attack * 2, self.range_of_attack * 2), SRCALPHA)
        if self.triggered:
            circle(surface, Color(0, 255, 0, 25), (self.range_of_attack, self.range_of_attack),
                   self.range_of_attack)
        colors = Color(117, 4, 157), Color(255, 212, 255)
        if self.target_id != -1 and self.target_id in enemies:
            try:
                k = 0
                vec = Vector(*self.pos(), *enemies[self.target_id].pos())
                tan = (vec.begin()[1] - vec.end()[1]) / (vec.begin()[0] - vec.end()[0])
                if ((vec.begin()[1] - vec.end()[1]) > 0 and (vec.begin()[0] - vec.end()[0]) > 0) or \
                        ((vec.begin()[1] - vec.end()[1]) <= 0 < (vec.begin()[0] - vec.end()[0])):
                    k = -180
                self.angle = (90 + int(degrees(atan(tan))) + k) % 360
            except ZeroDivisionError:
                self.angle = 0
        surface.blit(laser_tower[self.angle],
                     (self.range_of_attack - 2 * self.radius_size, self.range_of_attack - 2 * self.radius_size))
        screen.blit(surface, (self.x - self.range_of_attack, self.y - self.range_of_attack))

        if self.target_id == -1 or self.target_id not in enemies or not self.shoot_flag:
            return
        self.shoot_flag = False
        return Vector(*self.pos(), *enemies[self.target_id].pos()), colors


TOWERS = {'InfernoTower': InfernoTower, 'LaserTower': LaserTower}
COSTS = {'InfernoTower': 20, 'LaserTower': 30}
