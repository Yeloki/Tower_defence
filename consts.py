import os

import pygame

from other import rot_center

used_font = "arial"
# pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
# pygame.mixer.init()

# laser = pygame.mixer.Sound(os.path.join(os.path.abspath(os.curdir), 'sounds', 'laser.wav'))
# base_boom = pygame.mixer.Sound(os.path.join(os.path.abspath(os.curdir), 'sounds', 'base_boom.aif'))
#
# btn_click = pygame.mixer.Sound(os.path.join(os.path.abspath(os.curdir), 'sounds', 'button.aif'))
#
# build_tower = pygame.mixer.Sound(os.path.join(os.path.abspath(os.curdir), 'sounds', 'build.wav'))
#
# burning = pygame.mixer.Sound(os.path.join(os.path.abspath(os.curdir), 'sounds', 'burning.wav'))

hp_texture = pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'cpu.png'))
base_texture = pygame.transform.scale(
    pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'base.png')), (150, 100))
boom_map = pygame.transform.scale(
    pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'boom.png')), (240, 240))
boom_map2 = pygame.transform.scale(
    pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'base_explosion.png')), (1350, 900))
STATUSES = {'ENEMY_STATUS_A_LIFE': 0,
            'ENEMY_STATUS_DIED': 1,
            'ENEMY_STATUS_TO_GET_TO_BASE': 2}

NUMS = dict()
size = 18
font = pygame.font.SysFont(used_font, size)
for i in range(101):
    NUMS[i] = font.render(str(i), False, pygame.Color(255, 255, 255))

inferno1 = pygame.transform.scale(
    pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', '3.jpg')), (40, 40))
inferno2 = pygame.transform.scale(
    pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', '4.jpg')), (40, 40))
inferno3 = pygame.transform.scale(
    pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', '2.jpg')), (40, 40))
inferno4 = pygame.transform.scale(
    pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', '5.jpg')), (40, 40))
laser_tower = list()
inferno1.set_colorkey(pygame.Color(255, 255, 255))
inferno2.set_colorkey(pygame.Color(255, 255, 255))
inferno3.set_colorkey(pygame.Color(255, 255, 255))
inferno4.set_colorkey(pygame.Color(255, 255, 255))

image = pygame.transform.scale(pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', '1.jpg')), (80, 80))
image.set_colorkey(pygame.Color(255, 255, 255))
for i in range(359, -1, -1):
    laser_tower.append(rot_center(image, i))

enemy = []
images = (
    pygame.transform.scale(
        pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'enemy1.png')), (40, 40)),
    pygame.transform.scale(
        pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'enemy2.png')), (40, 40)),
    pygame.transform.scale(
        pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'enemy3.png')), (40, 40)),
    pygame.transform.scale(
        pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'enemy4.png')), (40, 40))
)

for j in range(4):
    enemy.append([])
    for i in range(359, -1, -1):
        enemy[j].append(rot_center(images[j], i))

red_btn = pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'red_btn.png'))
green_btn = pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'green_btn.png'))
blue_btn = pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'blue_btn.png'))

red_clicked_btn = pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'red_clicked_btn.png'))
green_clicked_btn = pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'green_clicked_btn.png'))
blue_clicked_btn = pygame.image.load(os.path.join(os.path.abspath(os.curdir), 'images', 'blue_clicked_btn.png'))

LANGUAGE = open(os.path.join(os.path.abspath(os.curdir), 'config')).readline().split()[1]
