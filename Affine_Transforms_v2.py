import numpy as np


def matrix(x=0, y=0):
    '''
    матрица переноса
    '''
    mat_moving = np.array([[1, 0, -x],
                           [0, 1, -y],
                           [0, 0, 1]])
    return mat_moving


camera1 = np.array([3, 2, 1])  # начальное положение робота с камеры
camera2 = np.array([4, 4, 1])  # конечное положение робота с камеры
x1, y1 = camera1[:2]
x2, y2 = camera2[:2]
theta_1 = np.pi / 6  # начальный угол робота с камеры
theta_2 = 0  # конечный угол робота с камеры

theta = theta_1 + theta_2

mat_r = np.array([[np.cos(theta), np.sin(theta), 0],
                  [-np.sin(theta), np.cos(theta), 0],
                  [0, 0, 1]])

mat_do = np.dot(matrix(x1, y1), camera1)
mat_posle = np.dot(matrix(x2, y2), camera2)

mat_moving = camera2 - camera1
mat = np.dot(mat_r, mat_moving)

print(' x: ', mat[0], '\n', 'y: ', mat[1], '\n', 'angle: ', (theta_2 - theta_1) * 180 / np.pi, '\n', 'way: ',
      np.sqrt(mat[0] ** 2 + mat[1] ** 2))
