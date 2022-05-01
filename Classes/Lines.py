from numpy import real
from Classes.Point import Point
from math import isclose
import numpy as np

class Line:
    def __init__(self, p1: Point, p2: Point):
        self.points = [p1, p2]
        p3 = p1 - p2
        self.length = sum([i**2 for i in p3]) ** (1 / 2)

    def __getitem__(self, item):
        return self.points[item]

    def direction(self):
        direc = self.points[1] - self.points[0]
        return Point([c / np.linalg.norm(direc.coord) for c in direc.coord])

    def cos_angle_between(self, l2):
        v1_u = (self.points[1] - self.points[0]).coord
        v2_u = (l2.points[1] - l2.points[0]).coord
        v1_u = v1_u / np.linalg.norm(v1_u)
        v2_u = v2_u / np.linalg.norm(v2_u)
        return np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)

    @staticmethod
    def is_close(line, intersect_p, tol = 1e-9):
        if isclose(
                line.length,
                line[0].distance(intersect_p) + line[1].distance(intersect_p),
                rel_tol=tol,
        ):
            return True
        return False


    def intersect(self, other):
        if any([x == y for x in self.points for y in other.points]):
            return False
        denom = (other[1][1] - other[0][1]) * (self[1][0] - self[0][0]) - (
            other[1][0] - other[0][0]
        ) * (self[1][1] - self[0][1])
        if denom == 0:
            return False

        numer = (other[1][0] - other[0][0]) * (self[0][1] - other[0][1]) - (
            other[1][1] - other[0][1]
        ) * (self[0][0] - other[0][0])
        res = numer / denom

        coord = [
            self[0][0] + res * (self[1][0] - self[0][0]),
            self[0][1] + res * (self[1][1] - self[0][1]),
        ]
        intersect_p = Point(coord)

        return Line.is_close(self, intersect_p) and Line.is_close(other, intersect_p)

    def __eq__(self, other: "Line") -> bool:
        return all([any([l1 == l2 for l2 in other.points]) for l1 in self.points])

    def __repr__(self):
        return str(self.points)

    def __str__(self):
        return self.__repr__()

