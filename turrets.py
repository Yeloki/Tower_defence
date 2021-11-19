from math import atan, degrees
from time import time

from pygame import Color, Surface
from pygame.draw import circle
from pygame.locals import *

from consts import inferno1, inferno2, inferno3, inferno4, laser_tower, LANGUAGE
from other import distance, Vector


class InfernoTower:
    radius_size = 20
    range_of_attack = 130

    def __init__(self, x, y) -> None:
        # damage
        self.damage = 240

        self.damage_update_cost = 40
        self.number_of_damage_improvements = 1  # count of updates (damage)
        self.damage_update_value = 120
        self.max_upgrade_damage_count = 30

        # range
        self.number_of_improvements_of_range_of_attack = 1  # count of updates (range)
        self.range_update_cost = 10
        self.range_update_value = 15
        self.max_upgrade_range_count = 10
        # burn
        self.burning_time = 3
        self.burning_update_cost = 20
        self.number_of_burning_improvements = 1  # count of updates (damage)
        self.burning_update_value = 1
        self.max_upgrade_burning_count = 10

        self.summary_tower_cost = COSTS[ALL_TOWERS[0]]
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
        if 1 <= self.number_of_damage_improvements + self.number_of_improvements_of_range_of_attack <= 5:
            surface.blit(inferno1, (self.range_of_attack - self.radius_size, self.range_of_attack - self.radius_size))
            screen.blit(surface, (self.x - self.range_of_attack, self.y - self.range_of_attack))
            color_key = 0

        elif 6 <= self.number_of_damage_improvements + self.number_of_improvements_of_range_of_attack <= 12:
            surface.blit(inferno2, (self.range_of_attack - self.radius_size, self.range_of_attack - self.radius_size))
            screen.blit(surface, (self.x - self.range_of_attack, self.y - self.range_of_attack))
            color_key = 1

        elif 13 <= self.number_of_damage_improvements + self.number_of_improvements_of_range_of_attack <= 19:
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
        if type_of_characteristics == 0:
            if self.number_of_damage_improvements != self.max_upgrade_damage_count:
                self.damage += self.damage_update_value
                self.summary_tower_cost += self.damage_update_cost
                self.damage_update_cost += 30 * self.number_of_damage_improvements
                self.number_of_damage_improvements += 1

        if type_of_characteristics == 1:
            if self.number_of_improvements_of_range_of_attack != self.max_upgrade_range_count:
                self.range_of_attack += self.range_update_value
                self.summary_tower_cost += self.range_update_cost
                self.range_update_cost += 20 * self.number_of_improvements_of_range_of_attack
                self.number_of_improvements_of_range_of_attack += 1
        if type_of_characteristics == 2:
            if self.number_of_burning_improvements != self.max_upgrade_burning_count:
                self.burning_time += self.burning_update_value
                self.summary_tower_cost += self.burning_update_cost
                self.burning_update_cost += 20 * self.number_of_burning_improvements
                self.number_of_burning_improvements += 1

    def range(self):
        return self.range_of_attack

    def disable_trigger(self):
        self.triggered = False

    def pos(self):
        return self.x, self.y

    def sell(self):
        return self.summary_tower_cost // 2

    def set_target(self, enemy_id):
        self.target_id = enemy_id

    def enable_trigger(self):
        self.triggered = True

    def shoot(self, enemies):
        if self.target_id == -1 or self.target_id not in enemies:
            return
        if distance(enemies[self.target_id].pos(), self.pos()) >= self.range_of_attack:
            enemies[self.target_id].burn(self.burning_time / 10, self.damage / 60)
            self.target_id = -1
            return
        # enemies[self.target_id].get_damage(self.damage // 60)
        enemies[self.target_id].burn_flag = True
        enemies[self.target_id].get_damage(self.damage / 60)

    def get_characteristics(self):
        out = [self.number_of_damage_improvements,
               self.number_of_improvements_of_range_of_attack,
               self.number_of_burning_improvements]
        out2 = [self.max_upgrade_damage_count,
                self.max_upgrade_range_count,
                self.max_upgrade_burning_count]
        if LANGUAGE == 'ENGLISH':
            return tuple(zip(('damage:\n' + str(self.damage),
                              'range:\n' + str(self.range_of_attack),
                              'burning time:\n' + str(self.burning_time / 10)
                              ), out, out2))
        else:
            return tuple(zip(('Урон:\n' + str(self.damage),
                              'Дальность атаки:\n' + str(self.range_of_attack),
                              'Время горения:\n' + str(self.burning_time / 10)
                              ), out, out2))

    def get_costs_of_upgrades(self):
        out = [self.damage_update_cost,
               self.range_update_cost,
               self.burning_update_cost]
        out2 = [self.number_of_damage_improvements,
                self.number_of_improvements_of_range_of_attack,
                self.number_of_burning_improvements]
        out3 = [self.max_upgrade_damage_count,
                self.max_upgrade_range_count,
                self.max_upgrade_burning_count]
        if LANGUAGE == 'ENGLISH':
            return tuple(zip(('Upgrade damage\nCost:' + str(self.damage_update_cost),
                              'Upgrade range\nCost: ' + str(self.range_update_cost),
                              'Upgrade burning\ntime\nCost: ' + str(self.burning_update_cost)
                              ), out, out2, out3))
        elif LANGUAGE == 'RUSSIAN':
            return tuple(zip(('Увеличить урон\nСтоимость:' + str(self.damage_update_cost),
                              'Увеличить\nдальность атаки\nСтоимость: ' + str(self.range_update_cost),
                              'Увеличить время\nгорения\nСтоимость: ' + str(self.burning_update_cost)
                              ), out, out2, out3))

    def characteristics(self):
        out = [self.number_of_damage_improvements,
               self.number_of_improvements_of_range_of_attack,
               self.number_of_burning_improvements]

        out2 = [self.max_upgrade_damage_count,
                self.max_upgrade_range_count,
                self.max_upgrade_burning_count]

        return tuple(zip((self.damage_update_cost,
                          self.range_update_cost,
                          self.burning_update_cost
                          ), out, out2))


def prototype(screen, pos: (int, int), r, turret_range, collision: bool):
    surface = Surface((turret_range * 2, turret_range * 2), SRCALPHA)
    circle(surface, Color(0, 255, 0, 50), (turret_range, turret_range), turret_range)
    circle(surface, Color(0, 255, 0) if not collision else Color(255, 0, 0), (turret_range, turret_range), r)
    screen.blit(surface, (pos[0] - turret_range, pos[1] - turret_range))


class LaserTower:
    radius_size = 20
    range_of_attack = 200

    def __init__(self, x, y):
        # damage
        self.damage = 60
        self.damage_update_cost = 20
        self.damage_update_value = 60
        self.number_of_damage_improvements = 1  # count of updates (damage)
        self.max_upgrade_damage_count = 30

        # range
        self.number_of_improvements_of_range_of_attack = 1  # count of updates (range)
        self.range_update_cost = 10
        self.range_update_value = 25
        self.max_upgrade_range_count = 10

        # rate
        self.rate = 12
        self.number_of_improvements_of_rate = 1  # count of updates (rate)
        self.rate_update_cost = 10
        self.rate_upgrade_value = 4
        self.max_upgrade_rate_count = 30

        # freeze
        self.freezing_time = 3
        self.freezing_update_cost = 20
        self.number_of_freezing_improvements = 1  # count of updates (damage)
        self.freezing_update_value = 1
        self.max_upgrade_freezing_count = 10

        self.summary_tower_cost = COSTS[ALL_TOWERS[1]]
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

        if type_of_characteristics == 0:
            if self.number_of_damage_improvements != self.max_upgrade_damage_count:
                self.damage += self.damage_update_value
                self.summary_tower_cost += self.damage_update_cost
                self.damage_update_cost += 20 * self.number_of_damage_improvements
                self.number_of_damage_improvements += 1

        if type_of_characteristics == 1:
            if self.number_of_improvements_of_range_of_attack != self.max_upgrade_range_count:
                self.range_of_attack += self.range_update_value
                self.summary_tower_cost += self.range_update_cost
                self.range_update_cost += 20 * self.number_of_improvements_of_range_of_attack
                self.number_of_improvements_of_range_of_attack += 1

        if type_of_characteristics == 2:
            if self.number_of_improvements_of_rate != self.max_upgrade_rate_count:
                self.rate += self.rate_upgrade_value
                self.summary_tower_cost += self.rate_update_cost
                self.rate_update_cost += 20 * self.number_of_improvements_of_rate
                self.number_of_improvements_of_rate += 1

        if type_of_characteristics == 3:
            if self.number_of_freezing_improvements != self.max_upgrade_freezing_count:
                self.freezing_time += self.freezing_update_value
                self.summary_tower_cost += self.freezing_update_cost
                self.freezing_update_cost += 20 * self.number_of_freezing_improvements
                self.number_of_freezing_improvements += 1

    def shoot(self, enemies):
        if self.target_id == -1 or self.target_id not in enemies:
            return
        if distance(enemies[self.target_id].pos(), self.pos()) >= self.range_of_attack:
            self.target_id = -1
            return
        if time() - self.last_shoot_time >= 10 / self.rate:
            self.last_shoot_time = time()
            self.shoot_flag = True
            enemies[self.target_id].get_damage(self.damage)
            enemies[self.target_id].freeze(self.freezing_time / 10)

    def get_characteristics(self):
        out = [self.number_of_damage_improvements,
               self.number_of_improvements_of_range_of_attack,
               self.number_of_improvements_of_rate,
               self.number_of_freezing_improvements]
        out2 = [self.max_upgrade_damage_count,
                self.max_upgrade_range_count,
                self.max_upgrade_rate_count,
                self.max_upgrade_freezing_count]
        if LANGUAGE == 'ENGLISH':
            return tuple(zip(('damage:\n' + str(self.damage),
                              'range:\n' + str(self.range_of_attack),
                              'rate:\n' + str(self.rate / 10),
                              'freezing time:\n' + str(self.freezing_time / 10)
                              ), out, out2))
        elif LANGUAGE == 'RUSSIAN':
            return tuple(zip(('Урон:\n' + str(self.damage),
                              'Далность\nатаки:\n' + str(self.range_of_attack),
                              'Выстрелов в\nсекунду:\n' + str(self.rate / 10),
                              'Время\nзаморозки:\n' + str(self.freezing_time / 10)
                              ), out, out2))

    def get_costs_of_upgrades(self):
        out = [self.damage_update_cost,
               self.range_update_cost,
               self.rate_update_cost,
               self.freezing_update_cost]
        out2 = [self.number_of_damage_improvements,
                self.number_of_improvements_of_range_of_attack,
                self.number_of_improvements_of_rate,
                self.number_of_freezing_improvements]
        out3 = [self.max_upgrade_damage_count,
                self.max_upgrade_range_count,
                self.max_upgrade_rate_count,
                self.max_upgrade_freezing_count]
        if LANGUAGE == 'ENGLISH':
            return tuple(zip(('Upgrade damage\nCost:' + str(self.damage_update_cost),
                              'Upgrade range\nCost: ' + str(self.range_update_cost),
                              'Upgrade rate\nCost: ' + str(self.rate_update_cost),
                              'Upgrade freezing\ntime\nCost: ' + str(self.freezing_update_cost)
                              ), out, out2, out3))
        elif LANGUAGE == 'RUSSIAN':
            return tuple(zip(('Увеличить урон\nСтоимость: ' + str(self.damage_update_cost),
                              'Увеличить\nдальность\nатаки\nСтоимость: ' + str(self.range_update_cost),
                              'Увеличить\nскорострельность\nСтоимость: ' + str(self.rate_update_cost),
                              'Увеличить время\nзаморозки\nСтоимость: ' + str(self.freezing_update_cost)
                              ), out, out2, out3))

    def characteristics(self):
        out = [self.number_of_damage_improvements,
               self.number_of_improvements_of_range_of_attack,
               self.number_of_improvements_of_rate,
               self.number_of_freezing_improvements]

        out2 = [self.max_upgrade_damage_count,
                self.max_upgrade_range_count,
                self.max_upgrade_rate_count,
                self.max_upgrade_freezing_count]

        return tuple(zip((self.damage_update_cost,
                          self.range_update_cost,
                          self.rate_update_cost,
                          self.freezing_update_cost
                          ),
                         out, out2))

    def sell(self):
        return self.summary_tower_cost // 2

    def update(self, screen, enemies) -> (None, (Vector, Color)):
        surface = Surface((self.range_of_attack * 2, self.range_of_attack * 2), SRCALPHA)
        if self.triggered:
            circle(surface, Color(0, 255, 0, 25), (self.range_of_attack, self.range_of_attack),
                   self.range_of_attack)
        colors = Color(117, 4, 157), Color(255, 212, 255)
        if self.target_id != -1 and self.target_id in enemies:
            try:
                vec = Vector(*self.pos(), *enemies[self.target_id].pos())
                if vec.begin()[0] - vec.end()[0] == 0 and \
                        vec.begin()[1] - vec.end()[1] < 0:
                    self.angle = 180 % 360
                else:
                    k = 0

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


if LANGUAGE == 'ENGLISH':
    TOWERS = {'InfernoTower': InfernoTower, 'LaserTower': LaserTower}
    COSTS = {'InfernoTower': 20, 'LaserTower': 30}
    ALL_TOWERS = ['InfernoTower', 'LaserTower']
elif LANGUAGE == 'RUSSIAN':
    TOWERS = {'ОгненнаяБашня': InfernoTower, 'ЛазернаяБашня': LaserTower}
    COSTS = {'ОгненнаяБашня': 20, 'ЛазернаяБашня': 30}
    ALL_TOWERS = ['ОгненнаяБашня', 'ЛазернаяБашня']
