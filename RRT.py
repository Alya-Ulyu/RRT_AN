import numpy as np
import pygame
from RRT_config import *
import random

def step(position, screen, nodes):
    x_node = random.randint(0, HEIGHT)
    y_node = random.randint(0, HEIGHT)
    pygame.draw.circle(screen, YELLOW, (x_node, y_node), NODE_STEP)
    nodes = np.append(nodes, [x_node, y_node])
    print(nodes.reshape(len(nodes)//2, 2))
    return nodes
