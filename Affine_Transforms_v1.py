import numpy as np


def matrix(x=0, y=0):
    mat_moving = np.array([[1, 0, -x],
                           [0, 1, -y],
                           [0, 0, 1]])
    return mat_moving


camera1 = np.array([3, 3, 1])
camera2 = np.array([5, 5, 1])
x1, y1 = camera1[:2]
x2, y2 = camera2[:2]
theta = np.pi/4

mat_r = np.array([[ np.cos(theta), np.sin(theta), 0],
                  [-np.sin(theta), np.cos(theta), 0],
                  [0, 0, 1]])


# mat_moving = np.array([[1, 0, -x],
#                        [0, 1, -y],
#                        [0, 0, 1]])


mat_do = np.dot(matrix(x1, y1), camera1)
mat_posle = np.dot(matrix(x2, y2), camera2)

mat_moving = camera2 - camera1
mat = np.dot(mat_r, mat_moving)

print(mat_do)
print(mat_posle)
print(mat_moving)
print(mat)



