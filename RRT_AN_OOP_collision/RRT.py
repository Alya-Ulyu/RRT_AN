import numpy as np
import pygame
from RRT_config import *
import random

ind = 0


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

    def __iter__(self):
        return self


def step(x, y, x_end, y_end, screen, nodes, c, obstaclesSurface):
    global ind
    # if c:
    #     nodes = np.append(nodes, Node(x, y))
    #     c = False
    nodes = np.append(nodes, Node(x, y))
    x_node, y_node = 0, 0
    find = False

    node = Node(random.randint(0, HEIGHT), random.randint(0, HEIGHT))

    # Страдание с ближайшей точкой
    minimum_distance = ((node.x - nodes[0].x) ** 2 + (node.y - nodes[0].y) ** 2) ** 0.5
    x_nearest, y_nearest = nodes[0].x, nodes[0].y
    for i in nodes:
        distance_to_node = ((node.x - i.x) ** 2 + (node.y - i.y) ** 2) ** 0.5
        if distance_to_node < minimum_distance:
            minimum_distance = distance_to_node
            x_nearest, y_nearest = i.x, i.y
            ind = np.where(nodes == i)

    flag_coll = collision([node.x, node.y], [x_nearest, y_nearest], obstaclesSurface)
    if flag_coll:
        # Рандомные точки проверяются на дальность, если слишком далеко, то они выкладываются на ACCESSIBILITY_RADIUS
        difference_x = node.x - x_nearest
        difference_y = node.y - y_nearest
        vector_length = (difference_x ** 2 + difference_y ** 2) ** 0.5
        if vector_length > ACCESSIBILITY_RADIUS:
            unit_vector_x = difference_x / vector_length
            unit_vector_y = difference_y / vector_length
            vector_length = (unit_vector_x ** 2 + unit_vector_y ** 2) ** 0.5
            while vector_length < ACCESSIBILITY_RADIUS:
                x_node += unit_vector_x
                y_node += unit_vector_y
                vector_length = (x_node ** 2 + y_node ** 2) ** 0.5
            pygame.draw.circle(screen, YELLOW, ((x_nearest + x_node), (y_nearest + y_node)), NODE_STEP)
            x_posed, y_posed = x_nearest + x_node, y_nearest + y_node
            node = Node(x_nearest + x_node, y_nearest + y_node)
            node.parent = nodes[ind]
            nodes = np.append(nodes, node)
        else:
            pygame.draw.circle(screen, YELLOW, (node.x, node.y), NODE_STEP)
            x_posed, y_posed = node.x, node.y
            node.parent = nodes[ind]
            nodes = np.append(nodes, node)
        # print(nodes.reshape(len(nodes) // 2, 2))
        pygame.draw.aaline(screen, WHITE, (x_posed, y_posed), (x_nearest, y_nearest), 3)

        if ((x_posed - x_end) ** 2 + (y_posed - y_end) ** 2) ** 0.5 <= ACCESSIBILITY_RADIUS_end:  # нашел
            # Записываем последнюю ноду в массив
            final_node = Node(x_end, y_end)
            final_node.parent = nodes[-1]
            nodes = np.append(nodes, final_node)
            find = True
            pygame.draw.aaline(screen, WHITE, (x_posed, y_posed), (x_end, y_end), 5)

    return nodes, find, c


def way(nodes, screen):
    path = np.array([])
    path = np.append(path, nodes[-1])
    while path[-1].parent is not None:
        path = np.append(path, path[-1].parent)
    path = [(node.x, node.y) for node in path]  # распаковка родительских нод

    pygame.draw.lines(screen, BLUE, False, path, 5)

    # for i in nodes:
    #     print(i.parent)


def normalize(vx, vy):
    norm = np.sqrt(vx * vx + vy * vy)
    if norm > 1e-6:
        vx /= norm
        vy /= norm
    return vx, vy


def dist(p1, p2):
    return np.hypot(p2[0] - p1[0], p2[1] - p1[1])


def collision(src, dst, obstacles):
    vx, vy = normalize(dst[0] - src[0], dst[1] - src[1])
    curr = [src[0], src[1]]
    while dist(curr, dst) > 1:
        intCurr = int(curr[0]), int(curr[1])
        try:
            if obstacles.get_at(intCurr) == (0, 255, 255):
                return False
        except Exception:
            pass
        curr[0] += vx
        curr[1] += vy
    return True

