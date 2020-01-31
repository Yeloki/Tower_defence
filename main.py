from os import environ

from pygame import Color
from pygame.locals import *

from game import Game
from gui import *
from map_creator import MapCreator

# from test import *

environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

game_state = 0
running = True

# print(STATUSES)
# BASIC PARAMS AND THEIR VALUES
screen_width = 1024
screen_height = 720
minimal_screen_width = 320
minimal_screen_height = 240
screen = pygame.display.set_mode((screen_width, screen_height), flags=RESIZABLE | DOUBLEBUF | HWSURFACE)
clock = pygame.time.Clock()


def terminate():
    global running
    running = False


def menu() -> int:
    global screen, screen_width, screen_height
    background = pygame.image.load('images/menu_background.jpg')
    out_state = 0
    objects = list()

    x = 10
    name = PercentLabel(x, 2, 20, 10)
    easy_game = PushButton(x, 14, 20, 10)
    medium_game = PushButton(x, 26, 20, 10)
    hard_game = PushButton(x, 38, 20, 10)
    map_creator = PushButton(x, 50, 20, 10)
    user_leves = PushButton(x, 62, 20, 10)
    settings = PushButton(x, 74, 20, 10)
    # exit_btn = PushButton(x, 86, 20, 10)
    exit_btn = PushButton(x, 74, 20, 10)
    easy_game.background_color, easy_game.text_color = Color(255, 255, 255), Color(0, 0, 0)
    medium_game.background_color, medium_game.text_color = Color(255, 255, 255), Color(0, 0, 0)
    hard_game.background_color, hard_game.text_color = Color(255, 255, 255), Color(0, 0, 0)
    map_creator.background_color, map_creator.text_color = Color(255, 255, 255), Color(0, 0, 0)
    user_leves.background_color, user_leves.text_color = Color(255, 255, 255), Color(0, 0, 0)
    settings.background_color, settings.text_color = Color(255, 255, 255), Color(0, 0, 0)
    exit_btn.background_color, exit_btn.text_color = Color(255, 255, 255), Color(0, 0, 0)
    name.text_color = Color(255, 255, 255)
    easy_game.alpha = 200
    medium_game.alpha = 200
    hard_game.alpha = 200
    map_creator.alpha = 200
    user_leves.alpha = 200
    settings.alpha = 200
    exit_btn.alpha = 200

    easy_game.text = 'Easy mode'
    medium_game.text = 'Medium mode'
    hard_game.text = 'Hard mode'
    map_creator.text = 'Map creator'
    user_leves.text = 'User leves'
    settings.text = 'Settings'
    exit_btn.text = 'Exit'
    name.text = 'Onslaught'

    easy_game.handler = 1
    medium_game.handler = 2
    hard_game.handler = 3
    # impossible
    map_creator.handler = 5
    user_leves.handler = 6
    settings.handler = None
    exit_btn.handler = 8

    objects.append(easy_game)
    objects.append(medium_game)
    objects.append(hard_game)
    objects.append(map_creator)
    objects.append(user_leves)
    # objects.append(settings)
    objects.append(exit_btn)
    objects.append(name)

    for elem in objects:
        elem.resize(screen)
    while out_state == 0 or out_state is None:
        screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), flags=DOUBLEBUF | HWSURFACE)
                objects_resize(objects, screen)
            if event.type == QUIT:
                return 8
            if event.type == KEYDOWN:
                if event.key == K_F4 and event.mod in (512, 256):
                    return 8
            out_state = emit_event_to_objects(objects, event)
        updater(objects, screen)

        pygame.display.flip()
    return out_state


def death_screen():
    global screen, screen_width, screen_height
    background = pygame.image.load('images/GAME_OVER.jpg')
    flag = True
    while flag:
        screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                return 8
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                flag = False
        pygame.display.flip()
    return 0


while running:
    if game_state == 0:
        game_state = menu()
    if game_state in (1, 2, 3, 4):  # New game
        game = Game(game_state, 'levels/common.txt')
        game_state, screen = game.start(pygame.display.set_mode((1024, 720), flags=DOUBLEBUF | HWSURFACE))
        del game
    if game_state == 5:  # Map creator
        mp = MapCreator()
        game_state, screen = mp.start(pygame.display.set_mode((1024, 720), flags=DOUBLEBUF | HWSURFACE))
    if game_state == 6:  # challenges
        game = Game(1, 'levels/user_level.txt')
        game_state, screen = game.start(pygame.display.set_mode((1024, 720), flags=DOUBLEBUF | HWSURFACE))
        del game
    if game_state == 7:  # settings
        pass
    if game_state == 8:  # for exit
        terminate()
    if game_state == 9:  # death screen
        game_state = death_screen()
