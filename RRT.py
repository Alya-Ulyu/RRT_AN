import numpy as np
import pygame
from RRT_config import *
import random


def step(x, y, x_end, y_end, screen, nodes):
    x_node, y_node = 0, 0
    find = False
    x_node_r = random.randint(0, HEIGHT)
    y_node_r = random.randint(0, HEIGHT)
    # pygame.draw.circle(screen, VIOLET, (x_node_y, y_node_y), NODE_STEP)

    nodes = np.reshape(nodes, (-1, 2))
    minimum_distance = ((x_node_r - x) ** 2 + (y_node_r - y) ** 2) ** 0.5
    x1, y1 = x, y
    for i in nodes:
        # print(i[0],i[1])
        distance_to_node = ((x_node_r - i[0]) ** 2 + (y_node_r - i[1]) ** 2) ** 0.5
        if distance_to_node < minimum_distance:
            minimum_distance = distance_to_node
            x1, y1 = i[0], i[1]

    # Рандомные точки проверяются на дальность, если слишком далеко, то они выкладываются на ACCESSIBILITY_RADIUS
    difference_x = x_node_r - x1
    difference_y = y_node_r - y1
    vector_length = (difference_x ** 2 + difference_y ** 2) ** 0.5
    if vector_length > ACCESSIBILITY_RADIUS:
        unit_vector_x = difference_x / vector_length
        unit_vector_y = difference_y / vector_length
        vector_length = (unit_vector_x ** 2 + unit_vector_y ** 2) ** 0.5
        while vector_length < ACCESSIBILITY_RADIUS:
            x_node += unit_vector_x
            y_node += unit_vector_y
            vector_length = (x_node ** 2 + y_node ** 2) ** 0.5
        pygame.draw.circle(screen, YELLOW, ((x1 + x_node), (y1 + y_node)), NODE_STEP)
        x_posed, y_posed = x1 + x_node, y1 + y_node
        nodes = np.append(nodes, [x1 + x_node, y1 + y_node])
    else:
        pygame.draw.circle(screen, YELLOW, (x_node_r, y_node_r), NODE_STEP)
        x_posed, y_posed = x_node_r, y_node_r
        nodes = np.append(nodes, [x_node_r, y_node_r])
    # print(nodes.reshape(len(nodes) // 2, 2))
    pygame.draw.aaline(screen, WHITE, (x_posed, y_posed), (x1, y1), 3)

    if ((x_posed - x_end) ** 2 + (y_posed - y_end) ** 2) ** 0.5 <= ACCESSIBILITY_RADIUS_end: # нашел
        find = True
        pygame.draw.aaline(screen, WHITE, (x_posed, y_posed), (x_end, y_end), 5)
    # edges = np.append(edges, [np.index(x_posed, y_posed), np.index(x1, y1)])
    nodes = np.reshape(nodes, (-1, 2))
    print(nodes)
    key = np.where(np.isclose(nodes, [x1, y1]))[0][0]
    value = np.where(np.isclose(nodes, [x_posed, y_posed]))[0][0]
    for name in sorted(edges.keys()):
        if name == key:
            edges[key] = value
        else:
            edges[key] = value
    print(edges)
    return nodes, find

