from Classes.Point import Point

class Tetrahedron:
    def __init__(self, p1 : Point, p2: Point, p3: Point, p4: Point):
        self.points = [p1, p2, p3, p4]
