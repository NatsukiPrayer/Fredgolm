from numpy import real
from Classes.Point import Point
from math import isclose
import numpy as np
from typing import Union

class Line:
    def __init__(self, p1: Point, p2: Point) -> None:
        self.points = [p1, p2]
        p3 = p1 - p2
        self.length = sum([i**2 for i in p3]) ** (1 / 2)

    def __getitem__(self, item: int) -> Point:
        return self.points[item]

    def invert(self) -> "Line":
        return Line(self.points[1], self.points[0])

    def direction(self) -> Point:
        direc = self.points[1] - self.points[0]
        return Point([c / np.linalg.norm(direc.coord) * -1 for c in direc.coord])

    def cos_angle_between(self, l2: "Line") -> float:
        v1_u = (self.points[1] - self.points[0]).coordinates
        v2_u = (l2.points[1] - l2.points[0]).coordinates
        v1_u = v1_u / np.linalg.norm(v1_u)
        v2_u = v2_u / np.linalg.norm(v2_u)
        return np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)

    def arcos_angle_between(self, l2: "Line") -> float:
        return np.arccos(self.cos_angle_between(l2))

    @staticmethod
    def is_close(line: "Line", intersect_p: Point, tol = 1e-9) -> bool:
        if isclose(
                line.length,
                line[0].distance(intersect_p) + line[1].distance(intersect_p),
                abs_tol=tol,
        ):
            return True
        return False

    def isect_line_plane_v3_4d(self, triangle, epsilon=1e-6, **kwargs):
        flag = False
        if triangle.id == '13/0/1':
            print()
            flag = True
        p_no = np.array(triangle.get_4d())[:3]
        p0 = np.array(self.points[0].coordinates)
        p1 = np.array(self.points[1].coordinates)

        u = p1 - p0
        # if isclose(u @ p_no, 0, abs_tol=1e-3):
        #     return any([self.intersect(line) for line in triangle.lines()])

        dot = np.dot(p_no, u)

        if abs(dot) > epsilon:
            # Calculate a point on the plane
            # (divide can be omitted for unit hessian-normal form).
            p_co = np.array(triangle.points[0].coordinates)

            w = p0 - p_co
            fac = -1 * np.dot(p_no, w) / dot
            u = u * fac
            intersect_p = Point(list(p0 + u))
            if 0 < fac < 1:
                if triangle.is_in(intersect_p):
                    print('<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>')
                    print(triangle.id)
                    return True
        return False

    def intersect(self, other: "Line") -> bool:
        x1, y1, z1 = self.points[0]
        x2, y2, z2 = self.points[1]
        x3, y3, z3 = other.points[0]
        x4, y4, z4 = other.points[1]
        res = np.linalg.det(np.array([[x2 - x1, y2 - y1, z2 - z1],
                                [x3 - x1, y3 - y1, z3 - z1],
                                [x4 - x1, y4 - y1, z4 - z1]]))
        if res == 0:
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
                self[0][2] + res * (self[1][2] - self[0][2])
            ]
            intersect_p = Point(coord)

            return Line.is_close(self, intersect_p) and Line.is_close(other, intersect_p)
        return False

    def same_surf(self):
        pass

    def triple_prod(self, v1: "Line", v2: "Line") -> float:
        cross = np.array((v1[1] - v1[0]).coordinates) @ np.array((v2[1] - v2[0]).coordinates)
        return np.dot(np.array((self[1] - self[0]).coordinates), cross)

    def isBetween(self, c: Point) -> bool:
        # compare versus epsilon for floating point values, or != 0 if using integers
        b = self.points[1]
        a = self.points[0]
        ba = [b - a for b, a in zip(b.coord, a.coord)]
        ca = [c - a for c, a in zip(c.coord, a.coord)]
        if abs(np.cross(ba, ca)) > 10 ** (-9):
            return False

        if np.dot(ba, ca) < 0:
            return False

        if np.dot(ba, ca) > Line(a, b).length:
            return False

        return True


    def __eq__(self, other: "Line") -> bool:
        return all([any([l1 == l2 for l2 in other.points]) for l1 in self.points])

    def __repr__(self) -> str:
        return str(self.points)

    def __str__(self) -> str:
        return self.__repr__()

