from time import time

from pygame.constants import *

from enemy import Enemy
from gui import *
from other import Vector

STATUSES = dict()
buffer = open('CONSTS', 'r')
for key, val in map(lambda x: (x.split()[0], int(x.split()[1])), buffer.readlines()):
    STATUSES[key] = val
buffer.close()


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
    enemy_id = 0
    all_turrets = dict()
    all_enemies_on_map = dict()
    current_wave = 0  # for up enemy hp
    time_between_waves = 20  # can be changed in settings
    current_time = time()
    pause_flag = False
    turrets_id = 0
    game_map = None
    difficult = 0
    focus_on = -1
    menu = None

    def __init__(self, difficult, path_to_map) -> None:
        self.difficult = difficult
        self.base_hp = 12 - difficult * 2
        self.game_map = GameMap(path_to_map)

    def load_map(self):
        pass

    def update(self, screen) -> None:
        pass

    def detected_enemy(self):
        pass

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

    def start(self, screen) -> (int, pygame.Surface):
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        tick = 30
        tick_time = 1
        self.menu = GameMenu()
        out_state = 0
        pygame.time.set_timer(tick, tick_time)
        field = screen_width, int(screen_height * 85 / 100)
        print(field)
        while out_state == 0 or out_state is None:
            screen.fill(pygame.Color(255, 0, 0))

            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    screen_width, screen_height = event.size
                    screen = pygame.display.set_mode((screen_width, screen_height),
                                                     flags=DOUBLEBUF | HWSURFACE)
                    objects_resize((self.menu,), screen)
                if event.type == QUIT:
                    return 8, screen
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        self.pause_flag = True
                    if event.key == K_F4 and event.mod in (512, 256):
                        return 8, screen
                    if event.key == K_SPACE:
                        print('send')
                        self.all_enemies_on_map[self.enemy_id] = Enemy(self.game_map.get_map())
                        self.enemy_id = (self.enemy_id + 1) % 100000
                if event.type == tick:
                    pygame.time.set_timer(tick, tick_time)
                    self.move_enemies()
            self.game_map.update(screen, self.base_hp)
            self.menu.update(screen)
            self.update_enemies(screen)
            pygame.display.flip()
        return out_state, screen
