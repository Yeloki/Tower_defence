import pygame
from pygame import Color

COLORS = Color('black'), Color('green')


def near_cords(x, y, SIZE):
    if x == 0 and y == 0:
        return [(x + 1, y), (x + 1, y + 1), (x, y + 1)]
    elif x == SIZE[0] - 1 and y == 0:
        return [(x - 1, y), (x - 1, y + 1), (x, y + 1)]
    elif x == SIZE[0] - 1 and y == SIZE[1] - 1:
        return [(x - 1, y), (x - 1, y - 1), (x, y - 1)]
    elif x == 0 and y == SIZE[1] - 1:
        return [(x, y - 1), (x + 1, y - 1), (x + 1, y)]
    elif x == 0:
        return [(x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1)]
    elif x == SIZE[0] - 1:
        return [(x, y + 1), (x - 1, y + 1), (x - 1, y), (x - 1, y - 1), (x, y - 1)]
    elif y == 0:
        return [(x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1), (x - 1, y)]
    elif y == SIZE[1] - 1:
        return [(x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y)]
    else:
        return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1), (x, y + 1), (x - 1, y + 1),
                (x - 1, y)]


class Cell:
    def __init__(self, state=0) -> None:
        self.state = state

    def set(self, other: int) -> None:
        self.state = other

    def get(self):
        return self.state

    def invert(self):
        self.state = not self.state

    def draw(self, surf, x, y, sizex, sizey):
        pygame.draw.rect(surf, COLORS[self.state], (x + 1, y + 1, sizex - 2, sizey - 2), 0)


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 30
        self.board = [[Cell() for x in range(width)] for y in range(height)]
        self.left = 10
        self.top = 10
        self.state = 0

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, surf) -> None:
        for i, line in enumerate(self.board):
            for j, elem in enumerate(line):
                rect = [self.left + j * self.cell_size,
                        self.top + i * self.cell_size,
                        self.cell_size, self.cell_size]
                pygame.draw.rect(surf, Color('white'), rect, 1)
                elem.draw(surf, *rect)

    def get_click(self, mouse_pos: tuple) -> None:
        cell_pos = self.get_cell(mouse_pos)
        # print(cell_pos)
        if cell_pos is not None:
            self.on_click(cell_pos)

    def on_click(self, cell_pos: tuple) -> None:
        self[cell_pos[0], cell_pos[1]].invert()

    def get_cell(self, mouse_pos: tuple) -> (tuple or None):
        flag1 = self.width * self.cell_size < mouse_pos[0] - self.left
        flag2 = self.height * self.cell_size < mouse_pos[1] - self.top
        flag3 = mouse_pos[0] < self.left or mouse_pos[1] < self.top
        if flag1 or flag2 or flag3:
            return None
        else:
            return (mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size

    def __getitem__(self, items) -> Cell:
        # print(items)
        return self.board[items[1]][items[0]]


SIZE = 700, 700
pygame.init()
screen = pygame.display.set_mode(SIZE)
fps = 1000
clock = pygame.time.Clock()
MYEVENTTYPE = 30
time = 200


class Life:
    def __init__(self, size=10):
        self.size = size
        self.board = Board(size, size)
        self.board.set_view(0, 0, min(SIZE) // size)
        pass

    def next_move(self):
        new = Board(self.size, self.size)
        new.set_view(0, 0, min(SIZE) // self.size)
        for y in range(self.size):
            for x in range(self.size):
                n = sum([self.board[x1, y1].get() for x1, y1 in near_cords(x, y, (self.size, self.size))])
                # print(n)
                if n == 3 and not self.board[x, y].get():
                    new[x, y].set(1)
                if (n == 3 or n == 2) and self.board[x, y].get():
                    new[x, y].set(1)
        self.board = new
        del new

    def change(self, mouse_pos: tuple) -> None:
        self.board.get_click(mouse_pos)

    def render(self, surface: type(screen)) -> None:
        self.board.render(surface)


life = Life(50)
game_flag = False
edit_flag = True
pygame.time.set_timer(MYEVENTTYPE, time)
while True:
    screen.fill(Color('black'))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit(0)
        if event.type == pygame.KEYDOWN:
            # print(event.key)
            if event.key == 32:  # Space
                game_flag = not game_flag
                edit_flag = not edit_flag
        if event.type == pygame.MOUSEBUTTONDOWN:
            # print(event.button)
            if event.button == 1 and edit_flag:
                life.change(event.pos)
            if event.button == 4:
                time -= 5 if time > 30 else 0
            if event.button == 5:
                time += 5 if time < 500 else 0
        print(time)
        if game_flag and event.type == MYEVENTTYPE:
            pygame.time.set_timer(MYEVENTTYPE, time)
            life.next_move()
    life.render(screen)
    clock.tick(fps)
    pygame.display.flip()
