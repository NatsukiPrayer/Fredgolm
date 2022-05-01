import numpy as np

from classes.Point import Point
from classes.Triangel import Triangle
from classes.Vector import Vector
from classes.Line import Line
from typing import Iterator
from math import acos, log, tan


class Frame:
    points: list[Point]
    lines: list[Line]
    name: str
    basis: list[Vector]
    central_point: Point
    square: float
    idx: str

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point, index=None):
        self.points = [p1, p2, p3, p4]
        self.lines = [Line(p1, p2), Line(p2, p3), Line(p3, p4), Line(p4, p1)]
        self.name = p1.name + p2.name + p3.name + p4.name
        self.idx = index
        self.central_point = self.__central_point()
        self.central_point.name = 'O'
        self.basis = self.__basis()

    def __central_point(self):
        return sum(self.points) / 4

    def __basis(self):
        TP = Line((self.points[0] + self.points[1]) / 2, (self.points[2] + self.points[3]) / 2).to_vector()
        QR = Line((self.points[1] + self.points[2]) / 2, (self.points[0] + self.points[3]) / 2).to_vector()
        n = TP * QR
        self.square = n.norm()
        n_e = n + self.central_point
        t1 = (TP + self.central_point)
        t2 = (t1 * n_e)
        return [n_e.normalize(), t1.normalize(), t2.normalize()]

    def lines_iter(self) -> Iterator[Line]:
        return self.lines.__iter__()

    def points_iter(self) -> Iterator[Point]:
        return self.points.__iter__()

    def __integral(self, line: Line, op):
        high_log = lambda x: log(abs((1 + tan(x / 2)) / (1 - tan(x / 2))))
        triangle = Triangle(line.start, line.end, op)
        try:
            np.seterr(all='raise')
            height = triangle.get_height(op.name)
        except:
            return 0
        intersect = triangle.get_height_intersect(op.name)
        HA = Line(intersect, triangle.points[0])
        HB = Line(intersect, triangle.points[1])
        AB = Line(triangle.points[0], triangle.points[1])
        amin = self.__angle_calculation(AB, HB, height, triangle)
        amax = self.__angle_calculation(AB, HA, height, triangle)
        return height * (high_log(amax) - high_log(amin))

    def __angle_calculation(self, v1: Line, v2: Line, height: float, triangle: Triangle):
        if v1.len() * v2.len() * v1.to_vector().arcos_angle_between(v2.to_vector()) > 0:
            return acos(height / triangle.lines[1].len())
        else:
            return -acos(height / triangle.lines[1].len())

    def __eq__(self, other):
        return self.idx == other.idx

    def integral_summ(self, other: "Frame"):
        if self == other:
            return sum(self.__integral(line, self.central_point) for line in self.lines_iter())
        else:
            return other.square / np.sqrt(
                sum([val ** 2 for val in (self.central_point - other.central_point).values]))

    def max_diameter(self) -> float:
        return max(x.len() for x in (self.lines + [Line(p1, p2) for p1, p2 in zip(self.points[:2], self.points[2:])]))

    def calk_k(self, other: "Frame", func):
        if self == other:
            return 0  # self.integral_summ(other)
        else:
            norm = Vector(other.central_point - self.central_point).norm()
            # denominator = np.pi * 4 * np.sqrt(sum([np.power(p, 2) for p in sub_points])) * other.square
            denominator = np.pi * 4 * norm
            numerator = func(self.central_point, other.central_point) * other.square
            return numerator / denominator
