import numpy as np
import pygame
from RRT_config import *
import random

def step(x, y , screen, nodes):
    x_node, y_node = 0, 0

    x_node_y = random.randint(0, HEIGHT)
    y_node_y = random.randint(0, HEIGHT)
    pygame.draw.circle(screen, YELLOW, (x_node_y, y_node_y), NODE_STEP)
    nodes = np.append(nodes, [x_node_y, y_node_y])
    # print(nodes.reshape(len(nodes)//2, 2))

    # Рандомные точки проверяются на дальность, если слишком далеко, то они выкладываются на ACCESSIBILITY_RADIUS
    difference_x = x_node_y - x
    difference_y = y_node_y - y
    vector_length = (difference_x ** 2 + difference_y ** 2) ** 0.5
    if vector_length > ACCESSIBILITY_RADIUS:
        unit_vector_x = difference_x / vector_length
        unit_vector_y = difference_y / vector_length
        vector_length = (unit_vector_x ** 2 + unit_vector_y ** 2) ** 0.5
        while vector_length < ACCESSIBILITY_RADIUS:
            x_node += unit_vector_x
            y_node += unit_vector_y
            vector_length = (x_node ** 2 + y_node ** 2) ** 0.5
    pygame.draw.circle(screen, VIOLET, (int(x + x_node), int(y + y_node)), NODE_STEP)

    return nodes
