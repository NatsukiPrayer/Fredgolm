import math

import matplotlib.pyplot as plt
import pygame
import pygame_gui
from Classes.Point import Point
from Classes.Lines import Line
from Classes.Triangle import Triangle
import numpy as np
from math import pi, cos, sin
from settings import *
import numpy as np


# colors is now a list of length 10
# Containing:
# [<Color red>, <Color #f13WINDOW_HEIGHT>, <Color #e36500>, <Color #d58e00>, <Color #c7b000>, <Color #a4bWINDOW_WIDTH>, <Color #72aa00>, <Color #459c00>, <Color #208e00>, <Color green>]

class Game:
    def __init__(self) -> None:
        self.points = []
        self.lines = []
        self.triangles = []

        pygame.init()
        pygame.display.set_caption('Triangulation')
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.background.fill(pygame.Color('#000000'))
        pygame.draw.rect(self.background, 'grey', rect=(0, 0, WINDOW_WIDTH * 7//8, WINDOW_HEIGHT), width=WINDOW_WIDTH * 7//8)

        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.optimize_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 25), (100, 50)),
                                                 text='Optimize',
                                                 manager = self.manager)
        self.redraw_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 75), (100, 50)),
                                                 text='Redraw',
                                                 manager = self.manager)
        self.save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 125), (100, 50)),
                                                 text='Save',
                                                 manager = self.manager)
        self.load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 175), (100, 50)),
                                                        text='Load',
                                                        manager=self.manager)
        self.colorize_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 225), (100, 50)),
                                                        text='Related',
                                                        manager=self.manager)
        self.clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 275), (100, 50)),
                                                        text='Clear',
                                                        manager=self.manager)
        self.calc_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 325), (100, 50)),
                                                         text='Calc',
                                                         manager=self.manager)
        self.flip_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 375), (100, 50)),
                                                        text='Flip',
                                                        manager=self.manager)
        self.line_center_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 425), (100, 50)),
                                                          text='Lines center',
                                                          manager=self.manager)
        self.height_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 475), (100, 50)),
                                                               text='Height',
                                                               manager=self.manager)
        self.mpl_draw_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 525), (100, 50)),
                                                          text='mpl_draw',
                                                          manager=self.manager)

        self.menu = None

        self.projection_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
        self.angle_x = self.angle_y = self.angle_z = DEFAULT_ANGLE
        self.rot_x = np.array(
            [[1, 0, 0], [0, cos(self.angle_x), -sin(self.angle_x)], [0, sin(self.angle_x), cos(self.angle_x)]])
        self.rot_y = np.array(
            [[cos(self.angle_y), 0, sin(self.angle_y)], [0, 1, 0], [-sin(self.angle_y), 0, cos(self.angle_y)]])
        self.rot_z = np.array(
            [[cos(self.angle_z), -sin(self.angle_z), 0], [sin(self.angle_z), cos(self.angle_z), 0], [0, 0, 1]])

    def new_point(self, pos = None) -> None:
        if pos == None:
            pos = pygame.mouse.get_pos()
        if pos[0] < WINDOW_WIDTH * 7//8:
            NewPoint = Point(list(pos))
            if NewPoint not in self.points:
                self.points.append(NewPoint)
                pygame.draw.circle(self.background, 'black', pos, 4)
                for line in self.lines:
                    if Line.is_close(line, NewPoint, tol=1e-3):
                        line[0].related.remove(line[1])
                        line[1].related.remove(line[0])
                        NewPoint.related.append(line[0])
                        NewPoint.related.append(line[1])
                        self.points[self.points.index(line[0])].related.append(NewPoint)
                        self.points[self.points.index(line[0])].clean()

                        self.points[self.points.index(line[1])].related.append(NewPoint)
                        self.points[self.points.index(line[1])].clean()

                        self.lines.remove(line)
                        break

                for point in self.points[:-1]:
                    NewLine = Line(point, NewPoint)
                    if all([not line.intersect(NewLine) for line in self.lines]):
                        self.lines.append(NewLine)
                        NewPoint.related.append(point)
                        point.related.append(NewPoint)
                        pygame.draw.aaline(self.background, 'black', point.coord, NewPoint.coord, 1)

    def triangles_creation(self) -> None:
        self.triangles = []
        for point in self.points:
            for next_point in point.related:
                for next_next_point in next_point.related:
                    if point in next_next_point.related:
                        NewTriangle = Triangle(point, next_point, next_next_point)
                        if NewTriangle not in self.triangles:
                            self.triangles.append(NewTriangle)

        for t in self.triangles:
            for point in self.points:
                if t.is_in(point):
                    self.triangles.remove(t)
                    break

    def rel(self) -> None:
        print('===========================')
        for p in self.points:
            print(p.related)
        print('======LINES======')
        for l in self.lines:
            print(l)
        print('======TRIANGLES======')
        for t in self.triangles:
            print(t)
            print(t.center)
            print(len(self.triangles))

    def clear(self) -> None:
        self.points = []
        self.lines = []
        self.triangles = []
        self.redraw(from_scracth = True)

    def divide(self) -> None:
        min_square = min([t.square() for t in self.triangles])
        for t in self.triangles:
            diff = t.square() / min_square
            if diff > 3:
                self.new_point(t.center.coord)

    def line_center(self) -> None:
        existing_lines = self.lines.copy()
        min_edge = min([l.length for l in existing_lines])
        for line in existing_lines:
            if line.length / min_edge > 2:
                new = line.points[1] + line.points[0]
                self.new_point([c/2 for c in new.coord])

    def flip(self, t1: Triangle, t2: Triangle) -> bool:
        temp = []
        for share_p in t1.points:
            if share_p in t2.points:
                temp.append(share_p)
        rel_line = Line(temp[0], temp[1])
        for p1, p2 in zip(t1.points, t2.points):
            if p1 not in rel_line:
                self_p = p1
            if p2 not in rel_line:
                other_p = p2
        self.triangles.append(Triangle(other_p, self_p, rel_line[0]))
        self.triangles.append(Triangle(other_p, self_p, rel_line[1]))
        self.points[self.points.index(rel_line[0])].related.remove(rel_line[1])
        self.points[self.points.index(rel_line[1])].related.remove(rel_line[0])
        self.points[self.points.index(self_p)].related.append(other_p)
        self.points[self.points.index(other_p)].related.append(self_p)
        self.lines.remove(rel_line)
        self.lines.append(Line(self_p, other_p))
        self.triangles.remove(t1)
        self.triangles.remove(t2)
        return True

    def optimize(self) -> None:
        for i in range(len(self.triangles)):
            count = 0
            for j in range(i, len(self.triangles)):
                if count == 3:
                    break
                if self.triangles[j].is_related(self.triangles[i]):
                    count += 1
                    for p in self.triangles[i].points:
                        if p not in self.triangles[j].points:
                            outer_p = p
                    x = outer_p.coord[0]
                    y = outer_p.coord[1]
                    det = []
                    for p in self.triangles[i].points:
                        l = [(p[0] - x) ** 2 + (p[1] - y) ** 2, p[0] - x, p[1] - y]
                        det.append(l)
                    det = np.array(det)
                    if np.linalg.det(det) == 0:
                        self.flip(self.triangles[i], self.triangles[j])
        print('=========================Done!=========================')
        #yield True

    def run(self) -> None:
        clock = pygame.time.Clock()
        is_running = True
        #opt = self.optimize()

        while is_running:
            self.rot_x = np.array(
                [[1, 0, 0], [0, cos(self.angle_x), -sin(self.angle_x)], [0, sin(self.angle_x), cos(self.angle_x)]])
            self.rot_y = np.array(
                [[cos(self.angle_y), 0, sin(self.angle_y)], [0, 1, 0], [-sin(self.angle_y), 0, cos(self.angle_y)]])
            self.rot_z = np.array(
                [[cos(self.angle_z), -sin(self.angle_z), 0], [sin(self.angle_z), cos(self.angle_z), 0], [0, 0, 1]])
            clock.tick(60)
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.angle_y += ROTATE_SPEED
                if keys[pygame.K_d]:
                    self.angle_y -= ROTATE_SPEED
                if keys[pygame.K_w]:
                    self.angle_x += ROTATE_SPEED
                if keys[pygame.K_s]:
                    self.angle_x -= ROTATE_SPEED
                if keys[pygame.K_q]:
                    self.angle_z += ROTATE_SPEED
                if keys[pygame.K_e]:
                    self.angle_z -= ROTATE_SPEED
                if keys[pygame.K_r]:
                    self.angle_x = self.angle_y = self.angle_z = DEFAULT_ANGLE
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    self.new_point()
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if self.redraw_button.check_pressed():
                        self.redraw(from_scracth=True)
                    if self.optimize_btn.check_pressed():
                        #turns = next(opt)
                        #if turns:
                        #    opt = self.optimize()
                        self.divide()
                        self.redraw(True)
                    if self.save_button.check_pressed():
                        self.save(mode=1)
                    if self.load_button.check_pressed():
                        self.menu = pygame_gui.windows.UIFileDialog(pygame.Rect((400, 300), (100, 100)), self.manager)
                    if self.colorize_button.check_pressed():
                        self.rel()
                    if self.clear_button.check_pressed():
                        self.clear()
                    if self.menu is not None and event.ui_element == self.menu.ok_button:
                        path = self.menu.current_file_path
                        self.menu = None
                        self.load(path)
                    if self.calc_button.check_pressed():
                        self.calc(0, WINDOW_HEIGHT)
                    if self.flip_button.check_pressed():
                        self.optimize()
                        self.redraw(from_scracth = True)
                    if self.line_center_button.check_pressed():
                        self.line_center()
                        self.redraw(from_scracth = True)
                    if self.height_button.check_pressed():
                        newp = self.triangles[0].get_height_intersect(self.triangles[0].points[2])
                        self.new_point(newp.coord)
                        print(self.triangles[0].integral(self.triangles[0].points[2]))
                        self.redraw(from_scracth = True)
                    if self.mpl_draw_button.check_pressed():
                        self.angle_x += 100
                        print(self.points[0].project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix)[:2])

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.redraw()

    def redraw(self, from_scracth = True) -> None:
        if from_scracth == True:
            for p in self.points:
                p.clean()
            self.lines = []
            self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.background.fill(pygame.Color('#000000'))
            pygame.draw.rect(self.background, 'grey', rect=(0, 0, WINDOW_WIDTH * 7//8, WINDOW_HEIGHT), width=WINDOW_WIDTH * 7//8)
            for point in self.points:
                xy = point.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix)
                x = xy[0]
                y = xy[1]
                pygame.draw.circle(self.background, 'black', (x, y), 4)
                for related_p in point.related:
                    NewLine = Line(point, related_p)
                    if NewLine not in self.lines:
                        if all([not line.intersect(NewLine) for line in self.lines]):
                            self.lines.append(NewLine)
                            p_xy = point.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix)
                            p_x = p_xy[0]
                            p_y = p_xy[1]
                            rel_p_xy = related_p.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix)
                            rel_p_x = rel_p_xy[0]
                            rel_p_y = rel_p_xy[1]
                            pygame.draw.aaline(self.background, 'black', (p_x, p_y), (rel_p_x, rel_p_y), 1)

        self.triangles_creation()
        self.window.blit(self.background, (0, 0))
        self.manager.draw_ui(self.window)
        pygame.display.update()

    def save(self, mode = 0) -> None:
        if mode == 0:
            with open('save.gg', 'w') as f:
                f.write('\n'.join(map(str, self.points)))
        if mode == 1:
            lines = []
            for triangle in self.triangles:
                points = []
                for point in triangle.points:
                    points.append(f'{point.coord[0]:.6f} {point.coord[1]:.6f} 0.000000')
                points.append(points[-1] + '\n')
                lines.append(' '.join(points))
            with open('save2.txt', 'w') as f:
                f.write('1\n1\n0\n16\n4 4\n')
                for micro_line in lines:
                    f.write(micro_line)

    def load(self, path: str) -> None:
        with open(path, 'r') as f:
            self.points = []
            self.triangles = []
            self.lines = []
            for line in f.readlines():
                self.new_point(pos = tuple(map(float, line.split())))
                self.redraw(from_scracth=True)

    def calc(self, a: float, b: float) -> None:
        N = len(self.triangles)
        A, f = self.find_A(a, b, N)
        calcul = np.linalg.solve(A, f)
        #calcul_num = sorted([[calcul[i], i] for i in range(len(self.triangles))],
                            #key = lambda x: x[0])
        # red = Color("blue")
        # colors = list(red.range_to(Color("red"), math.ceil(calcul_num[-1][0] - calcul_num[0][0])))
        # colors_rgb = [c.rgb for c in colors]
        # colors_rgb_255 = [(c[0] * 255, c[1] * 255, c[2] * 255) for c in colors_rgb]

        #print(calcul_num)
        min_calcul = abs(min(calcul))
        max_calcul = max(calcul) + min_calcul
        for i in range(len(calcul)):
            kal = (calcul[i] + min_calcul) / max_calcul
            pygame.draw.circle(self.background, (kal * 255, 0, (1-kal) * 255), self.triangles[i].center.coord, 4)
        #c2 = (WINDOW_HEIGHT ** 3 / 3 + WINDOW_HEIGHT ** 6 / (5 * (1 - WINDOW_HEIGHT ** 3 / 3))) / (
        #            1 - WINDOW_HEIGHT ** 3 / 3 - WINDOW_HEIGHT ** 6 / (5 * (1 - WINDOW_HEIGHT ** 3 / 3)))
        #c1 = WINDOW_HEIGHT * (1 + c2) / (1 - WINDOW_HEIGHT ** 3 / 3)
        #analyt_sol = [1 + x ** 2 * c1 + c2 for x in range(0, WINDOW_HEIGHT, int(WINDOW_HEIGHT/N))]
        #delta = sum([np.linalg.norm(analyt_sol[i] - calcul[i]) for i in range(0, N)]) / sum(
        #    [np.linalg.norm(analyt_sol[i]) for i in range(0, N)])


    def core(self, p1: Point, p2: Point):
        return 1/(pi * 90000) * (1/ abs(p1 - p2))

    def find_A(self, a: float, b: float, N: int, f=None) -> list:
        if f is None:
            f = self.core
        A = []
        for i in range(0, len(self.triangles)):
            temp = []
            for j in range(0, len(self.triangles)):
                if j == i:
                    #temp.append(self.triangles[j].integral() * self.triangles[j].area())
                    temp.append(0)
                else:
                    temp.append(self.core(self.triangles[i].center, self.triangles[j].center) * self.triangles[j].area())
            A.append(temp)
        A = np.array(A) + np.eye(len(A))
        q = Point([0, 0])
        pygame.draw.circle(self.background, 'black', q.coord, 10)
        f_vec = [f(i.center, q) for i in self.triangles]
        return [A, f_vec]


