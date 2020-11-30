import os
from time import time as global_time

from pygame.constants import *
from pygame.draw import aaline

from consts import base_texture, hp_texture, boom_map, boom_map2, STATUSES
from enemy import Enemy
from gui import *
from other import Segment
from other import distance, distance_to_segment
from turrets import TOWERS, prototype, COSTS, ALL_TOWERS


class BaseExplosion(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self, surface):
        ln = len(self.frames)
        self.cur_frame = (self.cur_frame + 1) % ln
        self.image = self.frames[self.cur_frame]
        surface.blit(self.image, self.rect)
        return self.cur_frame == ln - 1


class GameMap:
    class Base:
        triggered = False
        x, y = 0, 0

        def __init__(self, x, y):
            self.x, self.y = x, y

        def update(self, screen, hp):
            surf = pygame.Surface((150, 100), SRCALPHA)
            if base_texture is not None:
                surf.blit(base_texture, (0, 0))
            else:
                pygame.draw.rect(surf, pygame.Color(255, 255, 255), pygame.Rect(0, 0, 150, 100))
            for i in range(hp):
                if i < 5:
                    surf.blit(hp_texture, (15 + 24 * i, 21))
                else:
                    surf.blit(hp_texture, (15 + 24 * (i - 5), 55))
            screen.blit(surf, (self.x, self.y))

    x_size = 0
    y_size = 0
    line_width = 25
    game_map = list()
    background = pygame.image.load('images/game_background.jpg')

    def __init__(self, path_to_map):
        file = open(path_to_map, 'r').readlines()
        self.base = self.Base(*tuple(map(int, file[0].split()))[:2])
        file = tuple(map(lambda x: tuple(map(int, x.split())), file[1:]))
        self.dots = [i for i in file]
        self.game_map = [Segment(*file[i], *file[i + 1]) for i in range(len(file) - 1)]

    def get_map(self):
        return self.game_map

    def update(self, screen, base_hp):
        screen_width, screen_height = screen.get_width(), screen.get_height()
        screen.blit(pygame.transform.scale(self.background, (screen_width, screen_height)), (0, 0))
        for vec in self.game_map:
            draw_better_line(screen, vec.a(), vec.b(), pygame.Color(0, 62, 141),
                             self.line_width)
        for dot in self.dots:
            pygame.draw.circle(screen, pygame.Color(0, 62, 141), [*dot], self.line_width)
        if base_hp > 0:
            self.base.update(screen, base_hp)


class Game:
    class Explosion(pygame.sprite.Sprite):
        def __init__(self, sheet, columns, rows, x, y):
            super().__init__()
            self.frames = []
            self.cut_sheet(sheet, columns, rows)
            self.cur_frame = 0
            self.image = self.frames[self.cur_frame]
            self.rect = self.rect.move(x - 20, y - 20)

        def cut_sheet(self, sheet, columns, rows):
            self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
            for j in range(rows):
                for i in range(columns):
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

        def update(self, surface):
            ln = len(self.frames)
            self.cur_frame = (self.cur_frame + 1) % ln
            self.image = self.frames[self.cur_frame]
            surface.blit(self.image, self.rect)
            return self.cur_frame == ln - 1

    def __init__(self, difficult, path_to_map) -> None:
        self.fps = 60
        self.money = 30
        self.mouse_button_pressed = False
        self.focus_on = None
        self.time = 20

        self.all_animations_key = 0

        self.enemy_id = 0
        self.turrets_id = 0
        self.wave_size = 10
        self.current_pos = (0, 0)
        self.wave_queue = dict()
        self.all_turrets = dict()
        self.all_animations = dict()
        self.all_enemies_on_map = dict()

        self.current_wave = 0
        self.time_between_waves = 20 * 1000

        self.menu = None
        self.game_map = None
        self.kills = 0
        self.pause_flag = False
        self.difficult = difficult
        self.base_hp = 12 - difficult * 2
        self.game_map = GameMap(path_to_map)

    def update_animation(self, screen):
        for_del = []
        for key, val in self.all_animations.items():
            if val.update(screen):
                for_del.append(key)
        for key in for_del:
            del self.all_animations[key]

    def add_explosion(self, pos):
        self.all_animations[self.all_animations_key] = self.Explosion(boom_map, 6, 6, *pos)
        self.all_animations_key = (self.all_animations_key + 1) % 100000

    def detected_enemy(self):
        busy = list()
        for enemy_id, enemy in self.all_enemies_on_map.items():
            for turret_id, turret in self.all_turrets.items():
                if distance(turret.pos(), enemy.pos()) < turret.range() and turret_id not in busy:
                    turret.set_target(enemy_id)
                    busy.append(turret_id)

    def move_enemies(self):
        for enemy_id, enemy in self.all_enemies_on_map.items():
            enemy.move()

    def update_enemies(self, screen):
        delete = []
        for enemy_id, enemy in self.all_enemies_on_map.items():
            status = enemy.update(screen)
            if status == STATUSES['ENEMY_STATUS_DIED']:
                self.money += self.all_enemies_on_map[enemy_id].wave
                self.kills += 1
                delete.append(enemy_id)
                self.add_explosion(enemy.pos())
                continue
            if status == STATUSES['ENEMY_STATUS_TO_GET_TO_BASE']:
                delete.append(enemy_id)
                self.base_hp -= 1
                continue
        for enemy_id in delete:
            del self.all_enemies_on_map[enemy_id]

    def update_turrets(self, screen):
        lines = []
        for turret_id, turret in self.all_turrets.items():
            turret.shoot(self.all_enemies_on_map)
            line = turret.update(screen, self.all_enemies_on_map)
            lines.append(line) if line is not None else None
        for line in lines:
            draw_better_line(screen, line[0].point1(), line[0].point2(), line[1][0], 2)
            aaline(screen, line[1][1], line[0].point1(), line[0].point2())

    def next_wave_sender(self):
        self.current_wave += 1
        if self.current_wave % 10 != 0:
            self.wave_queue[self.current_wave] = [0, self.wave_size]
        else:
            self.wave_queue[self.current_wave] = [0, 1]
        self.enemies_sender(self.current_wave)

    def enemies_sender(self, ev_id):
        self.wave_queue[ev_id][1] -= 1
        self.all_enemies_on_map[self.enemy_id] = Enemy(self.game_map.get_map(), wave=ev_id,
                                                       difficult=self.difficult)
        self.enemy_id = (self.enemy_id + 1) % 100000
        if self.wave_queue[ev_id][1] == 0:
            del self.wave_queue[ev_id]
            return
        self.wave_queue[ev_id][0] = global_time()

    def collision(self, pos, r, tower_type, screen) -> bool:
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        if self.money < COSTS[tower_type] or self.menu.rect is None:
            return True
        test = []
        for vec in self.game_map.get_map():
            test.append(distance_to_segment(pos, vec))
            if distance_to_segment(pos, vec) - self.game_map.line_width <= r:
                return True
        x, y = pos
        if x + r in range(self.menu.rect[0], self.menu.rect[2] + self.menu.rect[0] + 1) and \
                y + r in range(self.menu.rect[1], self.menu.rect[3] + self.menu.rect[1] + 1):
            return True
        if x not in range(r, screen_width - r + 1) or y not in range(r, screen_height - r + 1):
            return True
        if x + r in range(self.game_map.base.x, self.game_map.base.x + 150) and \
                y + r in range(self.game_map.base.y, self.game_map.base.y + 100):
            return True
        for _, turret in self.all_turrets.items():
            if distance(pos, (turret.x, turret.y)) <= r * 2:
                return True
        return False

    def build_tower(self, tower_type, pos):

        self.all_turrets[self.turrets_id] = TOWERS[tower_type](*pos)
        self.money -= COSTS[tower_type]
        self.turrets_id = (self.turrets_id + 1) % 100000

        pass

    def turret_upgrade(self, type_of_update):
        characteristics = self.all_turrets[self.focus_on].characteristics()[type_of_update]
        if self.money >= characteristics[0] and \
                characteristics[1] != characteristics[2]:
            self.money -= characteristics[0]
            self.all_turrets[self.focus_on].upgrade(type_of_update)

    def start(self, screen) -> (int, pygame.Surface):
        pygame.mixer.music.load(os.path.join(os.path.abspath(os.curdir), 'sounds', 'game.wav'))
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(100000)
        second = pygame.USEREVENT
        base_explosion = None
        clock = pygame.time.Clock()
        pygame.time.set_timer(second, 1000)
        self.menu = GameMenu()
        want_to_build_type = None
        want_to_build_flag = False
        while True:  # main game-loop
            screen.fill(pygame.Color(255, 0, 0))
            state = None
            for event in pygame.event.get():  # event handler cycle begin
                state = self.menu.event_handler(event)

                if event.type == QUIT:
                    return 8, screen
                if base_explosion is None:
                    if event.type == second:  # next wave event
                        pygame.time.set_timer(second, 1000)
                        self.time -= 1
                        if self.time == 0:
                            self.next_wave_sender()
                            self.time = 20

                if event.type == KEYDOWN:  # hot-keys
                    if event.key == K_c:  # cheat button (add money)
                        self.money += 10000
                    if event.key == K_F4 and event.mod in (512, 256):
                        return 8, screen
                    if event.key == K_ESCAPE:
                        return 0, screen
                    if base_explosion is None:
                        if event.key == K_SPACE:
                            self.next_wave_sender()
                            self.time = 20
                            pygame.time.set_timer(second, 1000)
                        if event.key == K_s and self.focus_on is not None:
                            self.money += self.all_turrets[self.focus_on].sell()
                            del self.all_turrets[self.focus_on]
                            self.focus_on = None

                if event.type == MOUSEMOTION:
                    self.current_pos = event.pos

                if event.type == MOUSEBUTTONDOWN:
                    self.mouse_button_pressed = True
                    if self.focus_on is not None:
                        self.all_turrets[self.focus_on].disable_trigger()
                    flag = True
                    for turret_id, turret in self.all_turrets.items():
                        if distance(event.pos, (turret.x, turret.y)) <= turret.radius_size:
                            self.focus_on = turret_id
                            flag = False
                            break
                    if flag:
                        print(*self.menu.rect)

                        collision_x = (self.menu.rect[0] <= event.pos[0] <= self.menu.rect[2] +
                                       self.menu.rect[0])

                        collision_y = (self.menu.rect[1] <= event.pos[1] <= self.menu.rect[3] +
                                       self.menu.rect[1])

                        if not (collision_x and collision_y):
                            self.focus_on = None
                    if self.focus_on is not None:
                        self.all_turrets[self.focus_on].enable_trigger()

                if event.type == MOUSEBUTTONUP and self.mouse_button_pressed:
                    self.mouse_button_pressed = False

                    if want_to_build_flag:
                        if not self.collision(event.pos, 20, want_to_build_type, screen):
                            self.build_tower(want_to_build_type, event.pos)
                        want_to_build_flag = False
                        want_to_build_type = None
            # event handler cycle end
            if base_explosion is None:
                wave_timers = tuple(self.wave_queue.items())
                for key, val in wave_timers:
                    if global_time() - val[0] >= 1:
                        self.enemies_sender(key)
                self.detected_enemy()
                self.move_enemies()

                # handling state that returns a menu
                if state == 1:
                    pygame.time.set_timer(second, 1000)
                    self.time = 20
                    self.next_wave_sender()
                if state == 2:
                    want_to_build_flag = True
                    want_to_build_type = ALL_TOWERS[0]
                if state == 3:
                    want_to_build_flag = True
                    want_to_build_type = ALL_TOWERS[1]
                if state in (5, 6, 7, 8, 9):  # reserved for upgrades
                    self.turret_upgrade(state - 5)

            self.game_map.update(screen, self.base_hp)
            self.update_enemies(screen)
            self.update_turrets(screen)
            self.update_animation(screen)
            self.menu.update(screen,
                             self.time,
                             self.money,
                             self.focus_on,
                             self.all_turrets,
                             self.kills,
                             self.current_wave)

            if want_to_build_flag:
                prototype(screen,
                          self.current_pos,
                          TOWERS[want_to_build_type].radius_size,
                          TOWERS[want_to_build_type].range_of_attack,
                          self.collision(self.current_pos,
                                         TOWERS[want_to_build_type].radius_size,
                                         want_to_build_type,
                                         screen))
            if self.base_hp <= 0 and base_explosion is None:
                base_explosion = BaseExplosion(boom_map2,
                                               9,
                                               9,
                                               self.game_map.base.x,
                                               self.game_map.base.y)
                for tower_id in [__ for __, _ in self.all_turrets.items()]:
                    self.add_explosion(self.all_turrets[tower_id].pos())
                    del self.all_turrets[tower_id]
                self.focus_on = None
                for enemy_id in [__ for __, _ in self.all_enemies_on_map.items()]:
                    self.add_explosion(self.all_enemies_on_map[enemy_id].pos())
                    del self.all_enemies_on_map[enemy_id]
            if base_explosion is not None:
                if base_explosion.update(screen):
                    return 9, screen

            # fps wait and flip the display
            clock.tick(self.fps)
            pygame.display.flip()
            # end game-loop
