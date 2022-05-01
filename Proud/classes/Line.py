from classes.Point import Point
from classes.Vector import Vector
import numpy as np


class Line:
    start: Point
    end: Point
    name: str = None

    def __init__(self, point1: Point, point2: Point) -> None:
        self.start = point1
        self.end = point2
        if point1.name and point2.name:
            self.name = point1.name + point2.name


    def invert(self) -> "Line":
        return Line(self.end, self.start)

    def len(self) -> float:
        return np.sqrt(sum([(x - y) ** 2 for x, y in zip(self.start, self.end)]))

    def __str__(self) -> str:
        return f"{self.name}: {self.start} {self.end}"

    def to_vector(self) -> Vector:
        return Vector(self.end - self.start)
