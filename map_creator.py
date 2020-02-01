from copy import deepcopy

import pygame
from pygame import transform, draw, Color, image
from pygame.locals import *

from gui import draw_better_line, MapCreatorMenu
from other import Vector, distance, near_point_on_vector


class MapCreator:
    class Base:
        triggered = False
        base_texture = None
        x, y = 0, 0
        base_size = 150, 100

        def __init__(self, x, y, from_load=False):
            if from_load:
                self.x, self.y = x, y
            else:
                self.x, self.y = x - self.base_size[0] // 2, y - self.base_size[1] // 2

        def pos(self):
            return self.x, self.y

        def set_pos(self, x, y):
            self.x, self.y = x, y

        def collide(self, mouse_pos):
            return mouse_pos[0] in range(self.x, self.base_size[0] + self.x) and \
                   mouse_pos[1] in range(self.y, self.base_size[1] + self.y)

        @staticmethod
        def prototype(screen, pos, color_flag):
            draw.rect(screen, Color(0, 255, 0) if not color_flag else Color(255, 0, 0), Rect(pos[0] - 75,
                                                                                             pos[1] - 50, 150, 100))

        def get_for_save(self):
            return (self.x, self.y, *self.base_size)

        def enable_trigger(self):
            self.triggered = True

        def disable_trigger(self):
            self.triggered = False

        def get_near_point_to_point(self, point):
            x_s, y_s = self.base_size  # x sie and y size
            points = [near_point_on_vector(point, Vector(self.x, self.y, self.x + x_s, self.y)),
                      near_point_on_vector(point, Vector(self.x + x_s, self.y, self.x + x_s, self.y + y_s)),
                      near_point_on_vector(point, Vector(self.x + x_s, self.y + y_s, self.x, self.y + y_s)),
                      near_point_on_vector(point, Vector(self.x, self.y + y_s, self.x, self.y))]
            min_dist = min(distance(point, i_point) for i_point in points)
            return {distance(point, i_point): i_point for i_point in points}[min_dist]

        def update(self, screen):
            if self.base_texture is not None:
                if self.base_size is not None:
                    screen.blit(transform.scale(self.base_texture, self.base_size[:2]), (self.base_size[2:]))
                    if self.triggered:
                        draw.rect(screen, Color(0, 255, 0, 100), Rect(self.x, self.y, *self.base_size), 5)
            else:
                draw.rect(screen, Color(255, 255, 255), Rect(self.x, self.y, *self.base_size))
                if self.triggered:
                    draw.rect(screen, Color(0, 255, 0, 100), Rect(self.x, self.y, *self.base_size), 3)

    class Dot:
        triggered = False

        def collision_with_cursor(self, cur_pos):
            return distance(self.pos(), cur_pos) <= self.radius

        def __init__(self, x=0, y=0, r=25):
            self.x = x
            self.y = y
            self.radius = r

        def enable_trigger(self):
            self.triggered = True

        def disable_trigger(self):
            self.triggered = False

        def pos(self):
            return self.x, self.y

        def move(self, x, y):
            self.x, self.y = x, y

        @staticmethod
        def prototype(screen, pos, is_collision):
            draw.circle(screen, Color(0, 255, 0) if not is_collision else Color(255, 0, 0), pos, 25)

        def update(self, screen):
            draw.circle(screen, Color(0, 62, 141), self.pos(), self.radius)
            if self.triggered:
                draw.circle(screen, Color(0, 255, 0, 100), self.pos(), self.radius + 5, 5)

    background = image.load('images/game_background.jpg')
    mouse_button_pressed = False

    def __init__(self):
        self.changes_stack = list()
        self.dot_id = 0
        self.base_size = None
        self.filename = None
        self.menu = None
        self.base = None
        self.line_width = 25
        self.focus_on = -1
        self.dots = dict()
        self.current_pos = (-1, -1)

    def load(self, name):
        self.changes_stack.append((deepcopy(self.dots), deepcopy(self.base), deepcopy(self.dot_id)))
        print(self.changes_stack)

        file = open('levels/' + name + '.txt', 'r').readlines()
        self.base = self.Base(*tuple(map(int, file[0].split()))[:-2], True)
        file = tuple(map(lambda x: tuple(map(int, x.split())), file[1:-1]))
        self.dots = {i: self.Dot(*dot) for i, dot in enumerate(file)}
        self.dot_id = len(file)

    def save(self, name):
        try:
            if self.base is None or len(tuple(self.dots.items())) < 1:
                raise Exception
            file = open('levels/' + name + '.txt', 'w')
            if self.base is None:
                file.write(' '.join(map(str, (*tuple(self.dots.items())[-1][1].pos(), 150, 100))) + '\n')
            else:
                file.write(' '.join(map(str, self.base.get_for_save())) + '\n')
            for _, dot in self.dots.items():
                file.write(str(dot.x) + ' ' + str(dot.y) + '\n')
            pos = tuple(self.dots.items())[-1][1].pos()
            file.write(' '.join(map(str, map(int, self.base.get_near_point_to_point(pos)))) + '\n')
        except Exception as err:
            print(err)
        else:
            print('success')

    def update_map(self, screen):
        screen_width, screen_height = screen.get_width(), screen.get_height()
        screen.blit(transform.scale(self.background, (screen_width, screen_height)), (0, 0))
        surf = pygame.Surface((screen.get_width(), screen.get_height()), SRCALPHA)
        # for vec in (Vector(*self.dots[i].pos(), *self.dots[i + 1].pos()) for i in range(len(self.dots) - 1)):
        #     draw_better_line(surf, vec.begin(), vec.end(), Color(0, 62, 141, 100), self.line_width)
        last_dot = None
        for dot_id, dot in self.dots.items():
            if last_dot is None:
                last_dot = dot
                continue
            vec = Vector(*last_dot.pos(), *dot.pos())
            draw_better_line(surf, vec.begin(), vec.end(), Color(0, 62, 141, 100), self.line_width)
            last_dot = dot
        if len(tuple(self.dots.items())) >= 1 and self.base is not None:
            pos = tuple(self.dots.items())[-1][1].pos()
            vec = Vector(*pos, *map(int, self.base.get_near_point_to_point(pos)))
            draw_better_line(surf, vec.begin(), vec.end(), Color(0, 62, 141, 100), self.line_width)
            self.Dot(*vec.end()).update(screen)
        for _, dot in self.dots.items():
            dot.update(surf)

        if self.base is not None:
            self.base.update(surf)
        screen.blit(surf, (0, 0))

    def set_point(self, pos):
        self.changes_stack.append((deepcopy(self.dots), deepcopy(self.base), deepcopy(self.dot_id)))
        self.dots[self.dot_id] = self.Dot(*pos)
        self.dot_id += 1

    def set_base(self, pos):
        self.changes_stack.append((deepcopy(self.dots), deepcopy(self.base), deepcopy(self.dot_id)))
        self.base = self.Base(*pos)

    def align_to_grid(self):
        self.changes_stack.append((deepcopy(self.dots), deepcopy(self.base), deepcopy(self.dot_id)))
        if self.base is not None:
            self.base.x = round(self.base.x / 20) * 20
            self.base.y = round(self.base.y / 20) * 20
        for point_id, point in self.dots.items():
            point.x = round(point.x / 20) * 20
            point.y = round(point.y / 20) * 20

    def collision(self, pos, screen) -> bool:
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        x, y = pos
        if x in range(self.menu.rect[0], self.menu.rect[2] + self.menu.rect[0] + 1) and \
                y in range(self.menu.rect[1], self.menu.rect[3] + self.menu.rect[1] + 1):
            return True
        if x not in range(0, screen_width + 1) or y not in range(0, screen_height + 1):
            return True
        return False

    def base_collision(self, pos, screen):
        rect = *pos, 150, 100
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        if rect[0] - rect[2] // 2 < 0 or rect[0] + rect[2] // 2 > screen_width:
            return True
        if rect[1] - rect[3] // 2 < 0 or rect[1] + rect[3] // 2 > screen_height - self.menu.rect[3]:
            return True
        return False

    def roll_back_changes(self):
        if len(self.changes_stack) >= 1:
            self.dots, self.base, self.dot_id = self.changes_stack[-1]
            del self.changes_stack[-1]
            print('rolled back success')

    def start(self, screen):
        out_state = 0
        self.menu = MapCreatorMenu()
        want_to_place_type = None
        want_to_place_flag = False

        while out_state == 0 or out_state is None:
            state = None
            for event in pygame.event.get():
                state = self.menu.event_handler(event) if event.type in (MOUSEBUTTONUP,
                                                                         MOUSEBUTTONDOWN,
                                                                         MOUSEMOTION) else None
                if event.type == QUIT:
                    return 8, screen
                if event.type == KEYDOWN:
                    if event.key == K_F4 and event.mod in (512, 256):
                        return 8, screen
                    if event.key == pygame.K_z and event.mod in [128, 64]:
                        self.roll_back_changes()

                    if event.key == K_ESCAPE:
                        return 0, screen
                    if event.key == K_BACKSPACE and self.focus_on != -1:
                        if self.focus_on == 'base':
                            self.base = None
                        else:
                            del self.dots[self.focus_on]
                        self.focus_on = -1
                if event.type == MOUSEMOTION:
                    self.current_pos = event.pos
                if event.type == MOUSEBUTTONDOWN:
                    self.mouse_button_pressed = True
                    if self.focus_on != -1:
                        if self.focus_on == 'base':
                            self.base.disable_trigger()
                        else:
                            self.dots[self.focus_on].disable_trigger()
                    flag = True
                    if self.base is not None:
                        if self.base.collide(event.pos):
                            self.focus_on = 'base'
                            flag = False
                    for dot_id, dot in self.dots.items():
                        if dot.collision_with_cursor(event.pos):
                            self.focus_on = dot_id
                            flag = False
                            break
                    if flag:
                        collision_x = event.pos[0] in range(self.menu.rect[0],
                                                            self.menu.rect[2] + self.menu.rect[0] + 1)
                        collision_y = event.pos[1] in range(self.menu.rect[1],
                                                            self.menu.rect[3] + self.menu.rect[1] + 1)
                        if not (collision_x and collision_y):
                            self.focus_on = -1
                    if self.focus_on != -1:
                        if self.focus_on == 'base':
                            self.base.enable_trigger()
                        else:
                            self.dots[self.focus_on].enable_trigger()
                if event.type == MOUSEBUTTONUP and self.mouse_button_pressed:
                    self.mouse_button_pressed = False
                    if want_to_place_flag:
                        if not self.collision(event.pos, screen):
                            if want_to_place_type == 'point':
                                self.set_point(event.pos)
                            if want_to_place_type == 'base':
                                self.set_base(event.pos)
                        want_to_place_flag = False
            # end event-loop

            if state == 1:
                want_to_place_flag = True
                want_to_place_type = 'point'
            if state == 2:
                want_to_place_flag = True
                want_to_place_type = 'base'
            if state == 3:
                self.save('user_level')
            if state == 4:
                self.load('user_level')
            if state == 5:
                self.align_to_grid()
            if state == 6:
                self.dots.clear()
                self.base = None
            self.update_map(screen)
            self.menu.update(screen, (self.base is not None))
            if want_to_place_flag:
                if want_to_place_type == 'point':
                    self.Dot.prototype(screen, self.current_pos, self.collision(self.current_pos, screen))
                if want_to_place_type == 'base':
                    self.Base.prototype(screen, self.current_pos, self.base_collision(self.current_pos, screen))
            pygame.display.flip()
        return out_state
