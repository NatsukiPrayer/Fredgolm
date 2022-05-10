from logging import exception
import numpy as np
from typing import Union

class Point:
    def __init__(self, coord: list[float]) -> None:
        if len(coord) < 3:
            for i in range(len(coord), 3):
                coord.append(0)
        self.coordinates = coord
        self.coord = self.coordinates[:2]
        self.related = []
        self.name = ''

    def project(self, rot_x: np.array, rot_y: np.array, rot_z: np.array, proj_matrix: np.array, scale = 100) -> np.array:
        np_coord = np.array(self.coordinates)
        rotate_x = rot_x @ np_coord
        rotate_y = rot_y @ rotate_x
        rotate_z = rot_z @ rotate_y
        return (proj_matrix @ rotate_z) * scale

    def inv_project(self, coordinates: list[float], rot_x: np.array,
                    rot_y: np.array, rot_z: np.array, scale = 100) -> np.array:
        np_coord = np.array(coordinates)
        rev_rotate_z = np.linalg.inv(rot_z) @ np_coord
        rev_rotate_y = np.linalg.inv(rot_y) @ rev_rotate_z
        rev_rotate_x = np.linalg.inv(rot_x) @ rev_rotate_y
        return list(rev_rotate_x)


    def __sub__(self, other: "Point") -> "Point":
        if len(self.coord) == len(other.coord):
            return Point([i - j for i, j in zip(self.coord, other)])
        else:
            raise Exception("Different dimensions")

    def __eq__(self, other: "Point") -> bool:
        if self.coord == other:
            return True
        else:
            return False

    def __add__(self, other: "Point") -> "Point":
        if len(self.coord) == len(other.coord):
            return Point([i + j for i, j in zip(self.coord, other)])
        else:
            raise Exception("Different dimensions")

    def __getitem__(self, item: int) -> float:
        try:
            self.coordinates[item]
        except Exception as e:
            raise e
        else:
            return self.coordinates[item]

    def __ne__(self, other: "Point") -> bool:
        if self.coord != other:
            return False
        else:
            return True

    def __abs__(self):
        return sum([c**2 for c in self.coord])**(1/2)

    def clean(self) -> None:
        new_related = []
        for p in self.related:
            if p not in new_related:
                new_related.append(p)
        self.related = new_related

    def __repr__(self) -> None:
        return ' '.join(map(str, self.coord))

    def __str__(self) -> str:
        return self.__repr__()

    def __mul__(self, other: Union[float, int, "Point"]) -> "Point":
        if isinstance(other, Point):
            return sum([coord1 * coord2 for coord1, coord2 in zip(self.coord, other.coord)])
        return Point([coord * other for coord in self.coord])

    def __rmul__(self, other: Union[float, int, "Point"]) -> "Point":
        return self * other

    # def __pow__(self, power, modulo=None):
    #     res = Point([1, 1])
    #     for i in range(0, power-1):
    #         res = self * res
    #     return res

    def distance(self, other: "Point"):
        res = self - other
        return (res[0] ** 2 + res[1] ** 2) ** (1 / 2)
