from pygame import Color, Surface
from pygame.draw import circle, aaline
from pygame.locals import *

from other import distance


class InfernoTower:
    r = 20
    r_of_attack = 200

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.triggered = True
        self.target_id = -1

    def update(self, screen, enemies) -> None:
        surface = Surface((self.r_of_attack * 2, self.r_of_attack * 2), SRCALPHA)
        if self.triggered:
            circle(surface, Color(0, 0, 0, 50), (self.r_of_attack, self.r_of_attack), self.r_of_attack)
        circle(surface, Color(0, 0, 255, 255), (self.r_of_attack, self.r_of_attack), self.r)
        screen.blit(surface, (self.x - self.r_of_attack, self.y - self.r_of_attack))
        if self.target_id == -1 or self.target_id not in enemies:
            return
        aaline(screen, Color(255, 50, 50), self.pos(), enemies[self.target_id].pos())
        # circle(screen, Color(0, 0, 255), (int(self.x), int(self.y)), self.r_of_attack)

    def range(self):
        return self.r_of_attack

    def pos(self):
        return self.x, self.y

    def set_target(self, enemy_id):
        self.target_id = enemy_id

    def event_handler(self):
        pass

    def enable_trigger(self):
        pass

    def disable_trigger(self):
        pass

    def load_costs_of_upgrades(self):
        pass

    def upgrade_damage(self):
        pass

    def upgrade_range(self):
        pass

    def shoot(self, enemies):
        if self.target_id == -1 or self.target_id not in enemies:
            return
        if distance(enemies[self.target_id].pos(), self.pos()) >= self.r_of_attack:
            self.target_id = -1
            return
        enemies[self.target_id].get_damage(2)


def prototype(screen, pos: (int, int), r, range, collision: bool):
    surface = Surface((range * 2, range * 2), SRCALPHA)
    circle(surface, Color(0, 0, 0, 50), (range, range), range)
    circle(surface, Color(0, 255, 0) if not collision else Color(255, 0, 0), (range, range), r)
    screen.blit(surface, (pos[0] - range, pos[1] - range))


TOWERS = {'InfernoTower': InfernoTower}
