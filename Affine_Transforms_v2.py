import numpy as np


def matrix(x=0, y=0, theta=0):
    '''
    матрица переноса и поворота системы координат
    '''
    mat_conv = np.array([[np.cos(theta), -np.sin(theta), x],
                         [np.sin(theta), np.cos(theta), y],
                         [0, 0, 1]])
    return mat_conv


# начальное положение робота с камеры
vector_1 = np.array([3, 2, 1])
x1, y1 = vector_1[:2]
theta_1 = np.pi / 6

# конечное положение робота с камеры
vector_2 = np.array([4, 4, 1])
x2, y2 = vector_2[:2]
theta_2 = theta_1 - np.pi / 6  # pi/6 - угол на который повернулся робот (в системе координат робота)

mat_before = matrix(x1, y1, theta_1)
mat_after = matrix(x2, y2, theta_2)

# перенос и поворот системы координат
mat = np.dot(np.linalg.inv(mat_before), mat_after)

print(mat_before)
print()
print(mat_after)
print()
print(mat)
print(' x: ', mat[0, 2], '\n', 'y: ', mat[1, 2], '\n', 'angle: ', (theta_2 - theta_1) * 180 / np.pi, '\n', 'way: ',
      np.sqrt(mat[0, 2] ** 2 + mat[1, 2] ** 2))
