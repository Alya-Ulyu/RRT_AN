import pygame
from RRT_config import *
import RRT

cr, cl, x, y, x_end, y_end = [0] * 6

# Создаем окно
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RRT")

# Флаг для рисовки стенки
flStartDraw = False
# Флаг блокировки (пока происходит RRT - ничего нельзя делать)
flCalculations = False

# Цикл RRT
running = True
while running:
    # Ввод процесса (события)
    for event in pygame.event.get():

        # Выход из проги:
        if event.type == pygame.QUIT:
            running = False

        # Ввод стенки:
        if flCalculations == False:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                flStartDraw = True
            elif event.type == pygame.MOUSEMOTION:
                if flStartDraw:
                    pos = event.pos
                    pygame.draw.circle(screen, BLUE, pos, OBSTACLES_RADIUS)
                    pygame.display.update()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
                flStartDraw = False

            # Ввод начальной и конечной точек:
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()

                if event.button == 1:
                    cr += 1
                    if cr > 1:
                        pygame.draw.circle(screen, BLACK, (x, y), 10)
                    x, y = position[0], position[1]
                    nodes = ([x, y])
                    pygame.draw.circle(screen, RED, (position[0], position[1]), 10)

                elif event.button == 3:
                    cl += 1
                    if cl > 1:
                        pygame.draw.circle(screen, BLACK, (x_end, y_end), 10)
                    x_end, y_end = position[0], position[1]
                    pygame.draw.circle(screen, GREEN, (position[0], position[1]), 10)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flCalculations = True
                    for i in range(10000):
                        nodes, flag = RRT.step(x, y, x_end, y_end, screen, nodes)
                        if flag:
                            break
                    flCalculations = False


    pygame.display.update()

pygame.quit()
