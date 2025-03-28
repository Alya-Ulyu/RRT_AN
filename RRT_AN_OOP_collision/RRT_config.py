import numpy as np

# Размер окна
WIDTH, HEIGHT = 600, 600

# Размер точек
NODE_RADIUS = 10
NODE_STEP = 5

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Размер препятствия
OBSTACLES_RADIUS = 10

# Радиус доступности
ACCESSIBILITY_RADIUS = 30
ACCESSIBILITY_RADIUS_end = 50

# Массивы точек пути
nodes = np.array([])
edges = np.array([])

# Словарь с родительскими нодами:
edges = {}
