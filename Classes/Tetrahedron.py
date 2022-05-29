from Classes.Point import Point
from Classes.Triangle import Triangle
from Classes.Lines import Line
from math import isclose

class Tetrahedron:
    def __init__(self, p1 : Point, p2: Point, p3: Point, p4: Point):
        self.points = [p1, p2, p3, p4]


    def __eq__(self, other: "Tetrahedron") -> bool:
        if all([any([p1 == p2 for p1 in self.points]) for p2 in other.points]):
            return True
        else:
            return False

    def __getitem__(self, item):
        return self.points[item]

    def __ne__(self, other: "Tetrahedron") -> bool:
        if any([p1 != p2 for p1, p2 in zip(self.points, other.points)]):
            return False
        else:
            return True

    def volume(self):
        L1 = Line(self.points[0], self.points[1])
        L2 = Line(self.points[0], self.points[2])
        L3 = Line(self.points[0], self.points[3])
        return sum(L1.triple_prod(L2, L3))

    def center(self) -> Point:
        triangles = []
        for i in range(len(self.points)):
            triangles.append(Triangle(self.points[i % 4], self.points[(i+1) % 4], self.points[(i+2) % 4]))
        S1, S2, S3, S4 = map(lambda x: x.square(), triangles)
        x1, y1, z1 = self.points[0]
        x2, y2, z2 = self.points[1]
        x3, y3, z3 = self.points[2]
        x4, y4, z4 = self.points[3]
        denom = S1 + S2 + S3 + S4
        x = (S1 * x1 + S2 * x2 + S3 * x3 + S4 * x4) / denom
        y = (S1 * y1 + S2 * y2 + S3 * y3 + S4 * y4) / denom
        z = (S1 * z1 + S2 * z2 + S3 * z3 + S4 * z4) / denom
        # x = sum(p[0] for p in self.points) / 4
        # y = sum(p[1] for p in self.points) / 4
        # z = sum(p[2] for p in self.points) / 4
        return Point([x, y, z])

    def __repr__(self) -> str:
        return f'{self.points[0].idd}/{self.points[1].idd}/{self.points[2].idd}/{self.points[3].idd}'

    def __str__(self) -> str:
        return self.__repr__()


