from Classes.Point import Point
from Classes.Lines import Line
from Classes.Game import Game
from Classes.Triangle import Triangle
from math import pi, sin, cos
from settings import *

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    r = 9
    rs = r ** (1/2)
    points = [[0, 0]] + \
             [[cos(i*pi/8) * rs,
               sin(i*pi/8) * rs] for i in range(0, 16)]
    circle = [Point(point) for point in points]
    with open('Mikhail.gg', 'w') as f:
        f.write('\n'.join(map(str, circle)))
    Window = Game()
    Window.run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
