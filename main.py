from Classes.Point import Point
from Classes.Lines import Line
from Classes.Game import Game
from Classes.Triangle import Triangle
from math import pi, sin, cos
from settings import *

# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    r = 90000
    rs = r ** (1/2)
    points = [[WORKING_SPACE_WIDTH_HALF, WORKING_SPACE_HEIGHT_HALF]] + \
             [[cos(i*pi/8) * rs + WORKING_SPACE_WIDTH_HALF,
               sin(i*pi/8) * rs + WORKING_SPACE_HEIGHT_HALF] for i in range(0, 16)]
    circle = [Point(point) for point in points]
    with open('Mikhail.gg', 'w') as f:
        f.write('\n'.join(map(str, circle)))
    c2 = (600**3 / 3 + 600**6 / (5 * (1 + 600**3 / 3))) / (1 - 600**3 / 3 - 600**6 / (5 * (1 + 600**3 / 3)))
    c1 = 600 * (1 + c2) / (1 + 600**3 / 3)
    analyt_sol = lambda x: 1 + x**2 * c1 + c2
    print(c1, '\n', c2)
    Window = Game()
    Window.run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
