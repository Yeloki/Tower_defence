from pygame.constants import *

from enemy import Enemy
from gui import *
from other import Vector
from other import distance
from turrets import InfernoTower

STATUSES = dict()
buffer = open('CONSTS', 'r')
for key, val in map(lambda x: (x.split()[0], int(x.split()[1])), buffer.readlines()):
    STATUSES[key] = val
buffer.close()
del buffer


class GameMap:
    x_size = 0
    y_size = 0
    game_map = list()
    base = None
    base_size = None
    background = pygame.image.load('images/background_v4.jpg')

    def __init__(self, path_to_map):
        file = open(path_to_map, 'r').readlines()
        self.x_size, self.y_size = map(int, file[0].split()[:-1])
        self.base_size = tuple(map(int, file[1].split()))
        file = tuple(map(lambda x: tuple(map(int, x.split())), file[2:]))
        self.game_map = [Vector(*file[i], *file[i + 1]) for i in range(len(file) - 1)]
        print(file)

    def get_map(self):
        return self.game_map

    def update(self, screen, base_hp):
        screen_width, screen_height = screen.get_width(), screen.get_height()
        screen.blit(pygame.transform.scale(self.background, (screen_width, screen_height)), (0, 0))
        for vec in self.game_map:
            pygame.draw.line(screen, pygame.Color(255, 0, 0), vec.begin(), vec.end(), 50)
        if self.base is not None:
            screen.blit(pygame.transform.scale(self.base, self.base_size[:2]), (self.base_size[2:]))
        else:
            pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(*self.base_size))
            font = pygame.font.SysFont('Comic Sans MS', 32)
            text = font.render(str(base_hp), 1, pygame.Color(0, 0, 0))
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (self.base_size[0] + 5, self.base_size[1] + text_h))


class Game:
    # id
    focus_on = -1
    time = 20
    # next id of in-game objects
    enemy_id = 0
    turrets_id = 0

    fps = 60

    # objects case
    all_turrets = dict()
    all_enemies_on_map = dict()

    # waves params
    current_wave = 0  # for up enemy hp
    time_between_waves = 20 * 1000  # can be changed in settings

    # in-game objects
    menu = None
    game_map = None

    # flags
    pause_flag = False

    def __init__(self, difficult, path_to_map) -> None:
        self.difficult = difficult
        self.base_hp = 12 - difficult * 2
        self.game_map = GameMap(path_to_map)

    def load_map(self):
        pass

    def update(self, screen) -> None:
        pass

    def detected_enemy(self):
        a = distance
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
                delete.append(enemy_id)
                continue
            if status == STATUSES['ENEMY_STATUS_TO_GET_TO_BASE']:
                delete.append(enemy_id)
                self.base_hp -= 1
                continue
        for enemy_id in delete:
            del self.all_enemies_on_map[enemy_id]

    def update_turrets(self, screen):
        for turret_id, turret in self.all_turrets.items():
            turret.shoot(self.all_enemies_on_map)
            turret.update(screen)

    def next_wave_sender(self):
        print('send')
        self.all_enemies_on_map[self.enemy_id] = Enemy(self.game_map.get_map(), difficult=self.difficult)
        self.enemy_id = (self.enemy_id + 1) % 100000

    def start(self, screen) -> (int, pygame.Surface):
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        # states and other params
        out_state = 0
        state = None  # this param store value from self.menu.event_handler()
        # id for time-depends events
        tick = 30
        new_wave = 31

        tick_time = 10

        clock = pygame.time.Clock()
        pygame.time.set_timer(tick, tick_time)
        pygame.time.set_timer(new_wave, self.time_between_waves)

        self.menu = GameMenu()
        while out_state == 0 or out_state is None:  # main game-loop
            screen.fill(pygame.Color(255, 0, 0))

            for event in pygame.event.get():  # event handler cycle
                # if event.type == VIDEORESIZE: # screen resize, but disable in this version
                #     screen_width, screen_height = event.size
                #     screen = pygame.display.set_mode((screen_width, screen_height), flags=DOUBLEBUF | HWSURFACE)
                #     objects_resize((self.menu,), screen)
                state = self.menu.event_handler(event)
                if event.type == QUIT:
                    return 8, screen
                if event.type == KEYDOWN:  # hotkeys
                    if event.key == K_p:
                        self.pause_flag = True
                    if event.key == K_F4 and event.mod in (512, 256):
                        return 8, screen
                    if event.key == K_SPACE:
                        self.next_wave_sender()
                        pygame.time.set_timer(new_wave, self.time_between_waves)

                if event.type == tick:  # game tick event
                    pygame.time.set_timer(tick, tick_time)
                    self.time += 10

                if event.type == new_wave:  # next wave event
                    pygame.time.set_timer(new_wave, self.time_between_waves)
                    self.next_wave_sender()
            # print(state)
            self.move_enemies()
            self.detected_enemy()
            if state == 1:
                self.next_wave_sender()
                pygame.time.set_timer(new_wave, self.time_between_waves)
            if state == 2:
                self.all_turrets[self.turrets_id] = InfernoTower(100, 100)

            self.game_map.update(screen, self.base_hp)

            self.update_enemies(screen)
            self.update_turrets(screen)
            self.menu.update(screen)
            print(self.time) if self.time % 100 == 0 else None

            clock.tick(self.fps)
            pygame.display.flip()
        return out_state, screen
