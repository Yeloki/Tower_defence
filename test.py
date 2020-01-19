import pygame

size = 800, 600
# while True:
#     try:
#         size = tuple(map(int, input('Введите координаты:').split()))
#         if size[0] > 0 and size[1] > 0:
#             break
#         else:
#             raise Exception
#     except Exception:
#         print('Неверно указаны координаты.')
pygame.init()
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
pygame.draw.polygon(screen, pygame.Color(255, 255, 255), [[250, 110], [280, 150], [190, 190], [130, 130]])
pygame.draw.aalines(screen, pygame.Color(255, 255, 255), True, [[250, 110], [280, 150], [190, 190], [130, 130]])
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()
