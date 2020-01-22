from pygame import Color
from pygame.draw import circle


class InfernoTower:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.r = 20
        self.r_of_attack = 200
        self.target_id = -1

    def update(self, screen) -> None:
        circle(screen, Color(0, 0, 255), (int(self.x), int(self.y)), self.r)
        # circle(screen, Color(0, 0, 255), (int(self.x), int(self.y)), self.r_of_attack)

    def range(self):
        return self.r_of_attack

    def pos(self):
        return self.x, self.y

    def set_target(self, enemy_id):
        self.target_id = enemy_id

    def shoot(self, enemies):
        if self.target_id == -1 or self.target_id not in enemies:
            return
        enemies[self.target_id].get_damage(1)
