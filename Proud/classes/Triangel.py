from classes.Point import Point
from classes.Line import Line
from classes.helpers import prod
from typing import Iterator


class Triangle:
    points: list[Point]
    lines: list[Line]
    name: str

    def __init__(self, p1: Point, p2: Point, p3: Point):
        self.points = [p1, p2, p3]
        self.lines = [Line(p1, p2), Line(p2, p3), Line(p3, p1)]
        self.name = p1.name + p2.name + p3.name

    def __str__(self):
        return f"{self.name}: {self.points}"

    def perimeter(self) -> float:
        return sum([x.len() for x in self.lines_iter()])

    def __area2(self, name) -> float:
        side = [l for l in self.lines if name in l.name]
        return (side[0].invert().to_vector() * side[1].to_vector()).norm()

    def get_height(self, name: str) -> float:
        if name not in self.points_names():
            raise ValueError("No such points in triangle")
        base = next(l for l in self.lines_iter() if name not in l.name)
        return self.__area2(name) / base.len()

    def get_height_intersect(self, name: str) -> Point:
        if name not in self.points_names():
            raise ValueError("No such points in triangle")
        base = next(l for l in self.lines if name not in l.name)
        base_vector = base.to_vector()
        side_point = base.start
        side = next(l for l in self.lines if name in l.name and side_point.name in l.name)
        cos = base_vector.cos_angle_between((side.invert() if side.name[0] == 'O' else side).to_vector())
        return (cos * side.len() * base_vector.normalize()).end + base.start

    def get_angle_cos(self, name: str) -> float:
        if name not in self.points_names():
            raise ValueError("No such points in triangle")
        sides_len = [line.len() for line in self.lines if name in line.name]
        sides_sum_2 = sum([side_len ** 2 for side_len in sides_len])
        op_side_len_2 = next(line.len() for line in self.lines if name not in line.name) ** 2
        return (sides_sum_2 - op_side_len_2) / (2 * prod(sides_len))

    def points_names(self):
        return [p.name for p in self.points].__iter__()

    def lines_names(self):
        return [l.name for l in self.lines].__iter__()

    def lines_iter(self) -> Iterator:
        return self.lines.__iter__()

    def points_iter(self) -> Iterator:
        return self.points.__iter__()
