import pygame

from other import rot_center

used_font = 'bahnschrift'
# used_font = 'calibri'
# used_font = 'consolas'
pygame.init()

STATUSES = dict()
hp_texture = pygame.image.load('images/cpu.png')
base_texture = pygame.transform.scale(pygame.image.load('images/base.png'), (150, 100))
boom_map = pygame.transform.scale(pygame.image.load('images/boom.png'), (240, 240))
boom_map2 = pygame.transform.scale(pygame.image.load('images/base_explosion.png'), (1350, 900))
# boom_map2 = pygame.transform.scale(pygame.image.load('images/base_explosion.png'), (1024 * 9, 720 * 9))
buffer = open('CONSTS', 'r')
for key, val in map(lambda x: (x.split()[0], int(x.split()[1])), buffer.readlines()):
    STATUSES[key] = val
buffer.close()

NUMS = dict()
size = 18
font = pygame.font.SysFont(used_font, size)
for i in range(101):
    NUMS[i] = font.render(str(i), 1, pygame.Color(255, 255, 255))

inferno1 = pygame.transform.scale(pygame.image.load('images/3.jpg'), (40, 40))
inferno2 = pygame.transform.scale(pygame.image.load('images/4.jpg'), (40, 40))
inferno3 = pygame.transform.scale(pygame.image.load('images/2.jpg'), (40, 40))
inferno4 = pygame.transform.scale(pygame.image.load('images/5.jpg'), (40, 40))
laser_tower = list()
inferno1.set_colorkey(pygame.Color(255, 255, 255))
inferno2.set_colorkey(pygame.Color(255, 255, 255))
inferno3.set_colorkey(pygame.Color(255, 255, 255))
inferno4.set_colorkey(pygame.Color(255, 255, 255))
image = pygame.transform.scale(pygame.image.load('images/1.jpg'), (80, 80))
image.set_colorkey(pygame.Color(255, 255, 255))
for i in range(359, -1, -1):
    laser_tower.append(rot_center(image, i))

enemy = []
images = (pygame.transform.scale(pygame.image.load('images/enemy1.png'), (40, 40)),
          pygame.transform.scale(pygame.image.load('images/enemy2.png'), (40, 40)),
          pygame.transform.scale(pygame.image.load('images/enemy3.png'), (40, 40)),
          pygame.transform.scale(pygame.image.load('images/enemy4.png'), (40, 40)))
for j in range(4):
    enemy.append([])
    for i in range(359, -1, -1):
        enemy[j].append(rot_center(images[j], i))
red_btn = pygame.image.load('images/red_btn.png')
yellow_btn = pygame.image.load('images/yellow_btn.png')
green_btn = pygame.image.load('images/green_btn.png')
blue_btn = pygame.image.load('images/blue_btn.png')

red_clicked_btn = pygame.image.load('images/red_clicked_btn.png')
yellow_clicked_btn = pygame.image.load('images/yellow_clicked_btn.png')
green_clicked_btn = pygame.image.load('images/green_clicked_btn.png')
blue_clicked_btn = pygame.image.load('images/blue_clicked_btn.png')

# red_btn.set_colorkey(pygame.Color(255, 255, 255))
# yellow_btn.set_colorkey(pygame.Color(255, 255, 255))
# green_btn.set_colorkey(pygame.Color(255, 255, 255))
# blue_btn.set_colorkey(pygame.Color(255, 255, 255))
# del image, font, i, j, font, size, images, buffer, key, val