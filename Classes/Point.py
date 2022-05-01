from logging import exception


class Point:
    def __init__(self, coord):
        self.coord = coord
        self.related = []

    def __sub__(self, other):
        if len(self.coord) == len(other.coord):
            return Point([i - j for i, j in zip(self.coord, other)])
        else:
            raise Exception("Different dimensions")

    def __eq__(self, other):
        if self.coord == other:
            return True
        else:
            return False

    def __add__(self, other):
        if len(self.coord) == len(other.coord):
            return Point([i + j for i, j in zip(self.coord, other)])
        else:
            raise Exception("Different dimensions")

    def __getitem__(self, item):
        try:
            self.coord[item]
        except Exception as e:
            raise e
        else:
            return self.coord[item]

    def __ne__(self, other):
        if self.coord != other:
            return False
        else:
            return True

    def clean(self):
        new_related = []
        for p in self.related:
            if p not in new_related:
                new_related.append(p)
        self.related = new_related

    def __repr__(self):
        return ' '.join(map(str, self.coord))

    def __str__(self):
        return self.__repr__()

    def __mul__(self, other):
        if type(other) == Point:
            return sum([coord1 * coord2 for coord1, coord2 in zip(self.coord, other.coord)])
        else:
            return Point([coord * other for coord in self.coord])

    # def __pow__(self, power, modulo=None):
    #     res = Point([1, 1])
    #     for i in range(0, power-1):
    #         res = self * res
    #     return res

    def distance(self, other: "Point"):
        res = self - other
        return (res[0] ** 2 + res[1] ** 2) ** (1 / 2)
