import numpy as np
from collections import deque
import pandas as pd
import pygame


def euclidean_distance(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    distance = np.linalg.norm(point2 - point1)
    return distance


def marking(button, pos, x_pos0, y_pos0):
    '''
    This function paints the square in the desired color
    :param button: int, the number of the mouse button that was pressed (1 - left, 3 - right)
    :param pos: array, int, the x and y coordinates of the cursor when the mouse button is pressed
    :param x_pos0: int, the x coordinate required for mashing the previous square
    :param y_pos0: int, the y coordinate required for mashing the previous square
    :return: int, int, the x and y coordinates needed to erase the previous square
    '''
    for i in grid:
        if abs(pos[0] - i) <= 50:
            x_pos = i - 50
        if abs(pos[1] - i) <= 50:
            y_pos = i - 50

    rect = pygame.Rect((x_pos0, y_pos0, 48, 48))
    square = pygame.Rect((x_pos, y_pos, 48, 48))
    if button == 1:
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, RED, square)
    elif button == 2:
        pygame.draw.rect(screen, BLACK, square)
    elif button == 3:
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, GREEN, square)
    pygame.display.flip()

    return x_pos, y_pos


def dijkstra(x, y, size_W=12):
    global W
    global queue
    step = 2

    W[x][y] = 1

    queue = dijkstra_bypass(x, y, size_W)
    while step < np.size(W):
        step += 1
        for i in range(len(queue)):
            x, y = queue.pop()
            queue = dijkstra_bypass(x, y)
    if W[x_end, y_end] == 99:
        return True
    else:
        return False


def dijkstra_bypass(x, y, size_W=12):
    global W
    global queue
    col = row = size_W
    ways_straight = [-1, 0], [0, -1], [1, 0], [0, 1]
    ways_diagonal = [-1, -1], [1, -1], [1, 1], [-1, 1]
    for i in enumerate(ways_straight):
        if 0 <= (x + i[1][0]) < row and 0 <= (y + i[1][1]) < col and (
                W[x + i[1][0], y + i[1][1]] == 0 or W[x + i[1][0], y + i[1][1]] > W[x][y] + 1):
            if W[x + i[1][0]][y + i[1][1]] != -1:
                W[x + i[1][0], y + i[1][1]] = W[x][y] + 1
                queue.appendleft([x + i[1][0], y + i[1][1]])
    for i in enumerate(ways_diagonal):
        if 0 <= (x + i[1][0]) < row and 0 <= (y + i[1][1]) < col and (
                W[x + i[1][0], y + i[1][1]] == 0 or W[x + i[1][0], y + i[1][1]] > W[x][y] + 1.41):
            if W[x + i[1][0]][y + i[1][1]] != -1:
                W[x + i[1][0], y + i[1][1]] = W[x][y] + 2 ** 0.5
                queue.appendleft([x + i[1][0], y + i[1][1]])
    return queue


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
grid = np.array([0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600], int)

red = [0, 0]
green = [0, 0]
black = [0, 0]

pygame.init()
win_size = (600, 600)
screen = pygame.display.set_mode(win_size)
pygame.display.set_caption("Wave Way")

screen.fill(BLACK)
x = 0
y = 0
while x < 600:
    while y < 600:
        square = pygame.Rect((x, y, 48, 48))
        pygame.draw.rect(screen, WHITE, square)
        y += 50
    x += 50
    y = 0

pygame.display.flip()

W = np.zeros((12, 12))
queue = deque()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 1:
                W[red[1] // 50, red[0] // 50] = 0
                red = marking(1, pos, red[0], red[1])
                W[red[1] // 50, red[0] // 50] = 1
                print('RED: ', red[0] // 50, red[1] // 50 + 1)
            if event.button == 2:
                black = marking(2, pos, black[0], black[1])
                W[black[1] // 50, black[0] // 50] = -1
                print('BLACK: ', black[0] // 50, black[1] // 50)
            if event.button == 3:
                W[green[1] // 50, green[0] // 50] = 0
                green = marking(3, pos, green[0], green[1])
                W[green[1] // 50, green[0] // 50] = 99
                print('GREEN: ', green[0] // 50, green[1] // 50)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                x, y = map(int, np.where(W == 1))
                x_end, y_end = map(int, np.where(W == 99))
                no_way = dijkstra(x, y, len(W))

                for i in range(len(W)):
                    for j in range(len(W)):
                        if W[i][j] != -1:
                            W[i][j] += euclidean_distance((i, j), (x, y))

                if no_way:
                    print('No way')
                else:
                    df = pd.DataFrame(W)
                    pd.set_option('display.max_rows', None)
                    pd.set_option('display.max_columns', None)
                    pd.set_option('display.width', None)
                    print('РњРђРўР РР¦Рђ: ', '\n', df)

                    while W[x_end, y_end] > 4:
                        fumigation = np.array([99] * 8, float)

                        environment = np.array([[+ 1, 0],
                                                [- 1, 0],
                                                [0, + 1],
                                                [0, - 1],
                                                [- 1, - 1],
                                                [- 1, + 1],
                                                [+ 1, - 1],
                                                [+ 1, + 1]])

                        for j, i in enumerate(environment):
                            if 0 <= x_end + i[0] < 12 and 0 <= y_end + i[1] < 12:
                                fumigation[j] = (W[x_end + i[0], y_end + i[1]])

                        fumigation[fumigation == -1] = 99
                        direction = []
                        direction.append(environment[np.where(fumigation == np.min(fumigation))[0][0]])
                        for i in direction:
                            x_end += i[0]
                            y_end += i[1]
                            square = pygame.Rect((y_end * 50, x_end * 50, 48, 48))

                        pygame.draw.rect(screen, BLUE, square)
                    pygame.display.flip()