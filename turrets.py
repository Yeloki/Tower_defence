from pygame import Color, Surface
from pygame.draw import circle, aaline
from pygame.locals import *

from other import distance


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

    def update(self, screen, enemies) -> None:
        surface = Surface((self.range_of_attack * 2, self.range_of_attack * 2), SRCALPHA)
        if self.triggered:
            circle(surface, Color(0, 0, 0, 50), (self.range_of_attack, self.range_of_attack), self.range_of_attack)
        circle(surface, Color(0, 0, 255, 255), (self.range_of_attack, self.range_of_attack), self.radius_size)
        screen.blit(surface, (self.x - self.range_of_attack, self.y - self.range_of_attack))
        if self.target_id == -1 or self.target_id not in enemies:
            return
        aaline(screen, Color(255, 50, 50), self.pos(), enemies[self.target_id].pos())
        # circle(screen, Color(0, 0, 255), (int(self.x), int(self.y)), self.range_of_attack)

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
        enemies[self.target_id].get_damage(self.damage // 60)  # it's mean that this tower
        # can damage enemies with damage per second ( damage // 60)

    def get_characteristics(self):
        out = []
        return 'damage:\n' + str(self.damage),\
               'range:\n' + str(self.range_of_attack)

    def get_costs_of_upgrades(self):
        out = []
        return 'Upgrade damage.\nCost:' + str(self.damage_update_cost), \
               'Upgrade range.\nCost: ' + str(self.range_update_cost)

    def characteristics(self):
        return self.damage_update_cost, self.range_update_cost


def prototype(screen, pos: (int, int), r, turret_range, collision: bool):
    surface = Surface((turret_range * 2, turret_range * 2), SRCALPHA)
    circle(surface, Color(0, 0, 0, 50), (turret_range, turret_range), turret_range)
    circle(surface, Color(0, 255, 0) if not collision else Color(255, 0, 0), (turret_range, turret_range), r)
    screen.blit(surface, (pos[0] - turret_range, pos[1] - turret_range))


TOWERS = {'InfernoTower': InfernoTower}
