from os import environ

from pygame import Color
from pygame.locals import *

from game import Game
from gui import *

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
    background = pygame.image.load('images/background.jpg')
    out_state = 0
    objects = list()

    x = 70
    name = Label(x, 2, 20, 10)
    easy_game = PushButton(x, 14, 20, 10)
    medium_game = PushButton(x, 26, 20, 10)
    hard_game = PushButton(x, 38, 20, 10)
    map_creator = PushButton(x, 50, 20, 10)
    challenges = PushButton(x, 62, 20, 10)
    settings = PushButton(x, 74, 20, 10)
    exit_btn = PushButton(x, 86, 20, 10)

    easy_game.background_color, easy_game.text_color = Color(255, 255, 255), Color(0, 0, 0)
    medium_game.background_color, medium_game.text_color = Color(255, 255, 255), Color(0, 0, 0)
    hard_game.background_color, hard_game.text_color = Color(255, 255, 255), Color(0, 0, 0)
    map_creator.background_color, map_creator.text_color = Color(255, 255, 255), Color(0, 0, 0)
    challenges.background_color, challenges.text_color = Color(255, 255, 255), Color(0, 0, 0)
    settings.background_color, settings.text_color = Color(255, 255, 255), Color(0, 0, 0)
    exit_btn.background_color, exit_btn.text_color = Color(255, 255, 255), Color(0, 0, 0)

    easy_game.alpha = 200
    medium_game.alpha = 200
    hard_game.alpha = 200
    map_creator.alpha = 200
    challenges.alpha = 200
    settings.alpha = 200
    exit_btn.alpha = 200

    easy_game.text = 'Easy mode'
    medium_game.text = 'Medium mode'
    hard_game.text = 'Hard mode'
    map_creator.text = 'Map creator'
    challenges.text = 'Challenges'
    settings.text = 'Settings'
    exit_btn.text = 'Exit'
    name.text = 'Onslaught'

    easy_game.handler = lambda: 1
    medium_game.handler = lambda: 2
    hard_game.handler = lambda: 3
    map_creator.handler = lambda: None
    challenges.handler = lambda: None
    settings.handler = lambda: None
    exit_btn.handler = lambda: 8

    objects.append(easy_game)
    objects.append(medium_game)
    objects.append(hard_game)
    objects.append(map_creator)
    objects.append(challenges)
    objects.append(settings)
    objects.append(exit_btn)
    objects.append(name)

    for elem in objects:
        elem.resize(screen)
    result = list()
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


def game(level_of_difficult):
    """
    This function draw all game interface and objects
    :param level_of_difficult: level of difficult of new game
    :return: next game state
    """
    pass


while running:
    if game_state == 0:
        game_state = menu()
    if game_state in (1, 2, 3, 4):  # New game
        game = Game(game_state, 'levels/common.txt')
        game_state, screen = game.start(pygame.display.set_mode((1024, 720), flags=DOUBLEBUF | HWSURFACE))

    if game_state == 5:  # Map creator
        pass
    if game_state == 6:  # challenges
        pass
    if game_state == 7:  # settings
        pass
    if game_state == 8:  # for exit
        terminate()
