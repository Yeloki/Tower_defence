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
screen = pygame.display.set_mode((screen_width, screen_height), flags=DOUBLEBUF)
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
    name = PercentLabel(30, 2, 40, 12)
    easy_game = PushButton(x, 14, 20, 10)
    medium_game = PushButton(x, 26, 20, 10)
    hard_game = PushButton(x, 38, 20, 10)
    map_creator = PushButton(x, 50, 20, 10)
    user_level = PushButton(x, 62, 20, 10)
    settings = PushButton(x, 74, 20, 10)
    exit_btn = PushButton(x, 86, 20, 10)

    easy_game.style = blue_btn
    medium_game.style = blue_btn
    hard_game.style = blue_btn
    map_creator.style = blue_btn
    user_level.style = blue_btn
    settings.style = blue_btn
    exit_btn.style = blue_btn

    easy_game.clicked_style = blue_clicked_btn
    medium_game.clicked_style = blue_clicked_btn
    hard_game.clicked_style = blue_clicked_btn
    map_creator.clicked_style = blue_clicked_btn
    user_level.clicked_style = blue_clicked_btn
    settings.clicked_style = blue_clicked_btn
    exit_btn.clicked_style = blue_clicked_btn

    name.text_color = Color(200, 200, 255)
    easy_game.alpha = 200
    medium_game.alpha = 200
    hard_game.alpha = 200
    map_creator.alpha = 200
    user_level.alpha = 200
    settings.alpha = 200
    exit_btn.alpha = 200
    if LANGUAGE == 'ENGLISH':
        easy_game.text = 'Easy mode'
        medium_game.text = 'Medium mode'
        hard_game.text = 'Hard mode'
        map_creator.text = 'Map redactor'
        user_level.text = "User's level"
        settings.text = 'Settings'
        exit_btn.text = 'Exit'
        name.text = 'Tower Defence'
    elif LANGUAGE == 'RUSSIAN':
        easy_game.text = 'Низкая\nсложность'
        medium_game.text = 'Средняя\nсложность'
        hard_game.text = 'Высокая\nсложность'
        map_creator.text = 'Редактор\nкарты'
        user_level.text = "Пользовательский\nуровень"
        settings.text = 'Настройки'
        exit_btn.text = 'Выйти'
        name.text = 'Tower Defence'

    easy_game.handler = 1
    medium_game.handler = 2
    hard_game.handler = 3
    # impossible
    map_creator.handler = 5
    user_level.handler = 6
    settings.handler = 7
    exit_btn.handler = 8

    objects.append(easy_game)
    objects.append(medium_game)
    objects.append(hard_game)
    objects.append(map_creator)
    objects.append(user_level)
    objects.append(settings)
    objects.append(exit_btn)
    objects.append(name)

    for elem in objects:
        elem.set_rect(screen)
    while out_state == 0 or out_state is None:
        screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                return 8
            if event.type == KEYDOWN:
                if event.key == K_F4 and event.mod in (512, 256):
                    return 8
            out_state = emit_event_to_objects(objects, event)
        updater(objects, screen)

        pygame.display.flip()
    return out_state


def settings_menu():
    global screen, screen_width, screen_height
    x = 5
    objects = list()

    name = PercentLabel(x, 2, 20, 10)
    russian = PushButton(x, 14, 20, 10)
    english = PushButton(x, 26, 20, 10)
    save_changes = PushButton(60, 90, 20, 10)
    discard_changes = PushButton(80, 90, 20, 10)
    current_language = LANGUAGE

    if LANGUAGE == 'ENGLISH':
        name.text = 'change\nlanguage'
        russian.text = 'Русский'
        english.text = 'English'
        save_changes.text = 'Save changes\n& exit'
        discard_changes.text = 'Discard changes'
    elif LANGUAGE == 'RUSSIAN':
        name.text = 'Выбрать\nязык'
        russian.text = 'Русский'
        english.text = 'English'
        save_changes.text = 'Сохранить изменения\nи выйти'
        discard_changes.text = 'Отменить\nизменения'
    if LANGUAGE == 'RUSSIAN':
        russian.style = green_btn
        english.style = blue_btn

        russian.clicked_style = green_clicked_btn
        english.clicked_style = blue_clicked_btn
    elif LANGUAGE == 'ENGLISH':
        russian.style = blue_btn
        english.style = green_btn

        russian.clicked_style = blue_clicked_btn
        english.clicked_style = green_clicked_btn

    save_changes.style = blue_btn
    discard_changes.style = blue_btn
    save_changes.clicked_style = blue_clicked_btn
    discard_changes.clicked_style = blue_clicked_btn

    name.text_color = Color(200, 200, 255)
    russian.alpha = 200
    english.alpha = 200
    save_changes.alpha = 200
    discard_changes.alpha = 200

    russian.handler = 1
    english.handler = 2
    save_changes.handler = 3
    discard_changes.handler = 4

    objects.append(russian)
    objects.append(english)
    objects.append(name)
    objects.append(save_changes)
    objects.append(discard_changes)
    for elem in objects:
        elem.set_rect(screen)
    background = pygame.image.load('images/menu_background.jpg')
    while True:
        screen.blit(pygame.transform.scale(background, (screen_width, screen_height)), (0, 0))
        state = None
        for event in pygame.event.get():
            state = emit_event_to_objects(objects, event)
            if event.type == QUIT:
                return 8
            if event.type == KEYDOWN:
                if event.key == K_F4 and event.mod in (512, 256):
                    return 8
                if event.key == K_ESCAPE:
                    return 0
        if state == 1:
            current_language = 'RUSSIAN'
            objects[0].set_style(green_btn)
            objects[0].set_clicked_style(green_clicked_btn)
            objects[1].set_style(blue_btn)
            objects[1].set_clicked_style(blue_clicked_btn)
        if state == 2:
            current_language = 'ENGLISH'
            objects[1].set_style(green_btn)
            objects[1].set_clicked_style(green_clicked_btn)
            objects[0].set_style(blue_btn)
            objects[0].set_clicked_style(blue_clicked_btn)
        if state == 3 and current_language != LANGUAGE:
            file = open('config', 'w')
            file.write('LANGUAGE ' + current_language)
            file.close()
            return 8

        if state == 4 or state == 3:
            return 0
        updater(objects, screen)
        pygame.display.flip()


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
        game_state, screen = game.start(screen)
    if game_state == 5:  # Map creator
        mp = MapCreator()
        game_state, screen = mp.start(screen)
    if game_state == 6:  # user level
        game = Game(1, 'levels/user_level.txt')
        game_state, screen = game.start(screen)
    if game_state == 7:  # settings
        game_state = settings_menu()
    if game_state == 8:  # for exit
        terminate()
    if game_state == 9:  # death screen
        game_state = death_screen()

pygame.quit()
