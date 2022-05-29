from Classes.Point import Point
from Classes.Lines import Line
from Classes.Game import Game
from Classes.Triangle import Triangle
from math import pi, sin, cos
from settings import *

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    r = 1
    rs = r ** (1/2)
    x = lambda teth, phi: rs * sin(teth) * cos(phi)
    y = lambda teth, phi: rs * sin(teth) * sin(phi)
    z = lambda teth: rs * cos(teth)

    points = [[1, 1, 1]]
    points2 = [[x(j*pi/6, i*pi/3) + 1,
               y(j*pi/6, i*pi/3) + 1,
               z(j*pi/6) + 1] for i in range(0, 6) for j in range(0, 6)]
    temp = []
    for i in range(0, 6):
        micro_temp = []
        for j in range(0, 6):
            micro_temp.append([x(j * pi / 6, i * pi / 3) + 1,
              y(j * pi / 6, i * pi / 3) + 1,
              z(j * pi / 6) + 1])
        temp.append(micro_temp)

    Mikha = points + points2
    circle = [Point(point) for point in Mikha]
    with open('Mikhail_BIG_1.gg', 'w') as f:
        f.write('\n'.join(map(str, circle)))
    Window = Game()
    Window.run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
