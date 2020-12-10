import pygame
from os import environ
from consts import *
from pygame.locals import *
from source.graphic.sprites import Texture
from source.graphic.gui import Button, TextLabel

environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
game_state = 0
running = True

print(TEXTURES / "menu_background.jpg")

screen_width = WIDTH * RESIZE_K
screen_height = HEIGHT * RESIZE_K
screen = pygame.display.set_mode((screen_width, screen_height), flags=DOUBLEBUF)
pygame.display.set_caption('Tower Defence by FNC')
clock = pygame.time.Clock()


def resize_interface():
    pass


background = Texture(0, 0, screen_width, screen_height, str(TEXTURES / "menu_background.jpg"))
label = TextLabel(100, 100, 100, 50, text="Выглядит\nНормально", text_color=Color("red"),
                  background_color=Color("green"))
while running:
    background.draw(screen)
    label.draw(screen)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
            flag = False
    pygame.display.flip()
