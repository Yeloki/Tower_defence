from time import time

from pygame.constants import *

from gui import *


class GameMap:
    x_size = 0
    y_size = 0
    graph = list()
    base = None
    base_size = None
    background = pygame.image.load('images/background_v4.jpg')

    def __init__(self, path_to_map):
        file = open(path_to_map, 'r').readlines()
        self.x_size, self.y_size = map(int, file[0].split()[:-1])
        self.base_size = tuple(map(int, file[1].split()))
        for line in file[2:]:
            self.graph.append(tuple(map(int, line.split())))
        print(self.graph)

    def update(self, screen):
        screen_width, screen_height = screen.get_width(), screen.get_height()
        screen.blit(pygame.transform.scale(self.background, (screen_width, screen_height)), (0, 0))
        for i_point in range(len(self.graph) - 1):
            pygame.draw.line(screen, pygame.Color('white'), self.graph[i_point], self.graph[i_point + 1], 50)
        if self.base is not None:
            screen.blit(pygame.transform.scale(self.base, self.base_size[:2]), (self.base_size[2:]))
        else:
            pygame.draw.rect(screen, pygame.Color(0, 0, 0), pygame.Rect(*self.base_size))


class Game:
    all_turrets = list()
    all_enemies_on_map = list()
    current_wave = 0  # for up enemy hp
    time_between_waves = 20  # can be changed in settings
    current_time = time()
    pause_flag = False
    turrets_id = 0
    game_map = None
    difficult = 0
    focus_on = -1

    def __init__(self, difficult, path_to_map) -> None:
        self.difficult = difficult
        self.game_map = GameMap(path_to_map)

    def load_map(self):
        pass

    def start(self, screen) -> (int, pygame.Surface):
        screen_width, screen_height = screen.get_width(), screen.get_height()
        menu = GameMenu()
        out_state = 0
        field = screen_width, int(screen_height * 85 / 100)
        print(field)
        while out_state == 0 or out_state is None:
            screen.fill(pygame.Color(255, 0, 0))

            for event in pygame.event.get():
                if event.type == VIDEORESIZE:
                    screen_width, screen_height = event.size
                    screen = pygame.display.set_mode((screen_width, screen_height),
                                                     flags=DOUBLEBUF | HWSURFACE)
                    objects_resize((menu,), screen)
                if event.type == QUIT:
                    return 8, screen
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        self.pause_flag = True
                    if event.key == K_F4 and event.mod in (512, 256):
                        return 8, screen
            self.game_map.update(screen)
            menu.update(screen)
            pygame.display.flip()
        return out_state, screen
