import pygame
from os import environ
from pygame.locals import *


class App:
    def __init__(self):
        environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.FPS = 60
        self.running = True
        self.screen_width = 1024
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), flags=RESIZABLE | DOUBLEBUF)
        self.clock = pygame.time.Clock()

    def terminate(self):
        self.running = False

    def set_caption(self, cap):
        pygame.display.set_caption(cap)

    def update(self):
        pass

    def draw(self):
        self.screen.fill(Color("black"))

    def logic(self):
        pass

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
            self.logic()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
            pygame.display.flip()
