from Classes.Point import Point
from Classes.Lines import Line
import numpy as np
from math import log, tan, acos

class Triangle:

    def __init__(self, p1: Point, p2: Point, p3: Point) -> "Triangle":
        self.points = [p1, p2, p3]
        #self.diameter = 2 * ((p1[0]*(p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])))
        #Cx = (p1[0]**2 + p1[1]**2) * (p2[1] - p3[1]) + (p2[0]**2 + p2[1]**2) * \
        #     (p3[1] - p1[1]) + (p3[0]**2 + p3[1]**2) * (p1[1] - p2[1])
        #Cy = (p1[0]**2 + p1[1]**2) * (p3[0] - p2[0]) + (p2[0]**2 + p2[1]**2) * \
        #     (p1[0] - p3[0]) + (p3[0]**2 + p3[1]**2) * (p1[0] - p2[0])
        x = round((p1[0] + p2[0] + p3[0]) / 3, 2)
        y = round((p1[1] + p2[1] + p3[1]) / 3, 2)
        self.center = Point([x, y])
        self.color = 0

    def points_check(self, other: "Triangle") -> list[bool]:
        return [any([p1 == p2 for p2 in other.points]) for p1 in self.points]

    def lines(self) -> list[Line]:
        return [Line(self.points[0], self.points[1]),
                Line(self.points[1], self.points[2]),
                Line(self.points[2], self.points[0])]

    def get_height_intersect(self, p: Point, height_len=False) -> Point:
        lines = self.lines()
        if p not in self.points:
            raise ValueError("No such points in triangle")
        base = next(l for l in lines if p not in l)
        side_point = base[0]
        side = next(l for l in lines if p in l and side_point in l)
        cos = base.cos_angle_between(side.invert() if side[1] not in base else side)
        h = (base.direction() * cos * side.length) + base[0]
        if height_len:
            return [h, Line(p, h).length]
        else:
            return h

    def __angle_calculation(self, v1: Line, v2: Line, height: float) -> float:
        g = self.lines()[1].length
        gg = height / self.lines()[1].length
        if v1.length * v2.length * v1.arcos_angle_between(v2) > 0:
            return acos(height / self.lines()[1].length)
        else:
            return -acos(height / self.lines()[1].length)

    def integral(self) -> float:
        op = self.points[2]
        high_log = lambda x: log(abs((1 + tan(x / 2)) / (1 - tan(x / 2))))
        triangle = self
        try:
            np.seterr(all='raise')
            intersect, height = triangle.get_height_intersect(op, height_len=True)
        except:
            return 0
        intersect = triangle.get_height_intersect(op)
        HA = Line(intersect, triangle.points[0])
        HB = Line(intersect, triangle.points[1])
        AB = Line(triangle.points[0], triangle.points[1])
        amin = self.__angle_calculation(AB, HB, height)
        amax = self.__angle_calculation(AB, HA, height)
        return height * (high_log(amax) - high_log(amin))


    def R(self) -> float:
        return Line(self.points[0], self.points[1]).length * \
               Line(self.points[1], self.points[2]).length * \
               Line(self.points[2], self.points[0]).length / (4 * self.square())

    def __eq__(self, other: "Triangle") -> bool:
        if all(self.points_check(other)):
            return True
        else:
            return False

    def is_related(self, other: "Triangle") -> bool:
        if self != other:
            if sum(self.points_check(other)) == 2:
                return True
            else:
                return False
        return False

    def square(self) -> float:
        l1 = Line(self.points[0], self.points[1]).length
        l2 = Line(self.points[1], self.points[2]).length
        l3 = Line(self.points[2], self.points[0]).length
        s = sum([l1, l2, l3])/2
        return (s * (s - l1) * (s - l2) * (s - l3))**(1/2)


    def is_in(self, point: Point) -> bool:
        if point in self.points:
            return False
        p0y = self.points[0][1]
        p1y = self.points[1][1]
        p2y = self.points[2][1]
        p0x = self.points[0][0]
        p1x = self.points[1][0]
        p2x = self.points[2][0]
        px = point[0]
        py = point[1]
        area = self.area()
        s = 1 / (2 * area) * (p0y * p2x - p0x * p2y + (p2y - p0y) * px + (p0x - p2x) * py)
        t = 1 / (2 * area) * (p0x * p1y - p0y * p1x + (p0y - p1y) * px + (p1x - p0x) * py)

        if s > 0 and t > 0 and 1-s-t > 0:
            return True
        else:
            return False

    def area(self) -> float:
        p0y = self.points[0][1]
        p1y = self.points[1][1]
        p2y = self.points[2][1]
        p0x = self.points[0][0]
        p1x = self.points[1][0]
        p2x = self.points[2][0]
        return 0.5 * (-p1y * p2x + p0y * (-p1x + p2x) + p0x * (p1y - p2y) + p1x * p2y)

    def __repr__(self) -> str:
        return ' '.join(map(str, self.points))

    def __str__(self) -> str:
        return self.__repr__()

    