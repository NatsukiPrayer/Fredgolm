import math
import sys
import os

from classes.Point import Point
from classes.Scene import Scene
import numpy as np
import matplotlib.pyplot as plt
from classes.Vector import Vector


def find_fi(k, f):
    return np.linalg.solve(k, f)


def get_result(k, f, scene, file, num):
    len_scene = len(scene)
    res = find_fi(k, f)[:len_scene]
    ax = plt.axes(projection='3d')
    points = [x.central_point for x in scene]
    zline = [point.values[2] for point in points]
    xline = [point.values[0] for point in points]
    yline = [point.values[1] for point in points]
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.scatter3D(xline, yline, zline, c=res, s=75 * 450 / len_scene, cmap=plt.cm.get_cmap("turbo"))
    plt.show()
    plt.plot(res)
    plt.show()
    with open(f'results/out_{num}_{file[:-4]}.txt', 'w') as f:
        f.write(str(len_scene) + '\n')
        for num in res:
            try:
                f.write(str(num[0]) + '\n')
            except:
                f.write(str(num) + '\n')

def func(p1, p2):
    return (np.exp(-1j * Vector(p1 - p2).norm())) / Vector(p1 - p2).norm()

def func1(p1, p2):
    return 1

def main():
    file = r'C:\Users\alone\PycharmProjects\diplom\save2.txt'

    scene = Scene(file)
    k = scene.calculate_all_k(n_proc=15, func=func1)
    f = np.array([[1.0]] * len(scene))  # + [[0.0]])
    get_result(k, f, scene, file, '1')

if __name__ == "__main__":
    main()
