import random
import sqlite3

import numpy
import pygame
import pygame_gui
from Classes.Point import Point
from Classes.Lines import Line
from Classes.Triangle import Triangle
import numpy as np

class Game:
    def __init__(self) -> None:
        self.points = []
        self.lines = []
        self.triangles = []

        pygame.init()
        pygame.display.set_caption('Triangulation')
        self.window = pygame.display.set_mode((800, 600))

        self.background = pygame.Surface((800, 600))

        self.background.fill(pygame.Color('#000000'))
        pygame.draw.rect(self.background, 'grey', rect=(0, 0, 700, 600), width=700)

        self.manager = pygame_gui.UIManager((800, 600))
        self.optimize_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 25), (100, 50)),
                                                 text='Optimize',
                                                 manager = self.manager)
        self.redraw_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 75), (100, 50)),
                                                 text='Redraw',
                                                 manager = self.manager)
        self.save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 125), (100, 50)),
                                                 text='Save',
                                                 manager = self.manager)
        self.load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 175), (100, 50)),
                                                        text='Load',
                                                        manager=self.manager)
        self.colorize_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 225), (100, 50)),
                                                        text='Related',
                                                        manager=self.manager)
        self.clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 275), (100, 50)),
                                                        text='Clear',
                                                        manager=self.manager)
        self.calc_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 325), (100, 50)),
                                                         text='Calc',
                                                         manager=self.manager)
        self.flip_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 375), (100, 50)),
                                                        text='Flip',
                                                        manager=self.manager)
        self.line_center_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 425), (100, 50)),
                                                          text='Lines center',
                                                          manager=self.manager)
        self.height_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 475), (100, 50)),
                                                               text='Height',
                                                               manager=self.manager)

        self.menu = None

    def new_point(self, pos = None) -> None:
        if pos == None:
            pos = pygame.mouse.get_pos()
        if pos[0] < 700:
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
            for j in range(i, len(self.triangles)):
                if self.triangles[j].is_related(self.triangles[i]):
                    for p in self.triangles[i].points:
                        if p not in self.triangles[j].points:
                            outer_p = p
                    if Line(self.triangles[j].center, outer_p).length >= self.triangles[i].R():
                        self.flip(self.triangles[i], self.triangles[j])
        print('=========================Done!=========================')
        #yield True

    def run(self) -> None:
        clock = pygame.time.Clock()
        is_running = True
        #opt = self.optimize()

        while is_running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
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
                        self.calc(0, 600)
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


                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.redraw()

    def redraw(self, from_scracth = False) -> None:
        if from_scracth == True:
            for p in self.points:
                p.clean()
            self.lines = []
            self.background = pygame.Surface((800, 600))
            self.background.fill(pygame.Color('#000000'))
            pygame.draw.rect(self.background, 'grey', rect=(0, 0, 700, 600), width=700)
            for point in self.points:
                pygame.draw.circle(self.background, 'black', point.coord, 4)
                for related_p in point.related:
                    NewLine = Line(point, related_p)
                    if NewLine not in self.lines:
                        if all([not line.intersect(NewLine) for line in self.lines]):
                            self.lines.append(NewLine)
                            pygame.draw.aaline(self.background, 'black',
                                             point.coord, related_p.coord, 1)

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
        N = len(self.triangles) ** (1 / 2).__floor__()
        A, f = self.find_A(a, b, N)
        calcul = np.linalg.solve(A, f)
        c2 = (600 ** 3 / 3 + 600 ** 6 / (5 * (1 - 600 ** 3 / 3))) / (
                    1 - 600 ** 3 / 3 - 600 ** 6 / (5 * (1 - 600 ** 3 / 3)))
        c1 = 600 * (1 + c2) / (1 - 600 ** 3 / 3)
        analyt_sol = [1 + x ** 2 * c1 + c2 for x in range(0, 600, int(600/N))]
        delta = sum([np.linalg.norm(analyt_sol[i] - calcul[i]) for i in range(0, N)]) / sum(
            [np.linalg.norm(analyt_sol[i]) for i in range(0, N)])
        print('delta = ', delta)

    def find_A(self, a: float, b: float, N: int, K=lambda x, y: x*x + y*y, f=lambda x: 1) -> list:
        A = []
        for i in range(0, len(self.triangles)):
            temp = []
            for j in range(0, len(self.triangles)):
                temp.append(np.linalg.norm(K(self.triangles[i].center, self.triangles[j].center)) * self.triangles[j].area())
            A.append(temp)
        A = np.array(A) + np.eye(len(A))
        f_vec = [1 for i in range(N)]
        return [A, f_vec]
