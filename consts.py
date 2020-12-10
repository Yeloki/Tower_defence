import os

import pygame
import pathlib
from config_worker import *

LEVELS = pathlib.Path(os.path.join(os.path.abspath(os.curdir), "levels"))
TEXTURES = pathlib.Path(os.path.join(os.path.abspath(os.curdir), "images"))

USED_FONT = "arial"

pygame.init()

NUMS = dict()
size = 18

font = pygame.font.SysFont(USED_FONT, size)

for i in range(101):
    NUMS[i] = font.render(str(i), False, pygame.Color(255, 255, 255))

STATUSES = {'ENEMY_STATUS_A_LIFE': 0,
            'ENEMY_STATUS_DIED': 1,
            'ENEMY_STATUS_TO_GET_TO_BASE': 2}

RESIZE_K = 2
MINIMAL_SCREEN_WIDTH = 320  # 640, if RESIZE_K == 2
MINIMAL_SCREEN_HEIGHT = 240  # 480, if RESIZE_K == 2

WIDTH = 512
HEIGHT = 360
LANGUAGE = get_lang()
