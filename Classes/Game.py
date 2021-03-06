import math

import matplotlib.pyplot as plt
import pygame
import pygame_gui
from Classes.Point import Point
from Classes.Lines import Line
from Classes.Triangle import Triangle
from Classes.Tetrahedron import Tetrahedron
import numpy as np
from math import pi, cos, sin, isclose
from settings import *
import numpy as np


# colors is now a list of length 10
# Containing:
# [<Color red>, <Color #f13WINDOW_HEIGHT>, <Color #e36500>, <Color #d58e00>, <Color #c7b000>, <Color #a4bWINDOW_WIDTH>, <Color #72aa00>, <Color #459c00>, <Color #208e00>, <Color green>]

class Game:
    mstate = True

    def __init__(self) -> None:
        self.points = []
        self.lines = []
        self.triangles = []
        self.tetrahedron = []

        self.calculated = []
        self.calculated_3d = []
        self.q = Point([-3, -3, -3])
        self.fredgolm_flag = False
        self.fredgolm_flag_3d = False
        self.state = True

        pygame.init()
        pygame.display.set_caption('Triangulation')
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.background.fill(pygame.Color('#000000'))
        pygame.draw.rect(self.background, 'grey', rect=(0, 0, WINDOW_WIDTH * 7//8, WINDOW_HEIGHT), width=WINDOW_WIDTH * 7//8)

        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.optimize_btn = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 25), (200, 50)),
                                                 text='Optimize',
                                                 manager = self.manager)
        # self.redraw_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 75), (100, 50)),
        #                                          text='Redraw',
        #                                          manager = self.manager)
        self.save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 75), (200, 50)),
                                                 text='Save',
                                                 manager = self.manager)
        self.load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 125), (200, 50)),
                                                        text='Load',
                                                        manager=self.manager)
        self.rel_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 175), (200, 50)),
                                                        text='Related',
                                                        manager=self.manager)
        self.clear_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 225), (200, 50)),
                                                        text='Clear',
                                                        manager=self.manager)
        self.tri_calc_button = pygame_gui.elements.UIButton(
                                                        relative_rect=pygame.Rect((WINDOW_WIDTH * 7 // 8, 275), (200, 50)),
                                                        text='Tri fredgolm',
                                                        manager=self.manager)
        self.show_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 325), (200, 50)),
                                                         text='Show solution',
                                                         manager=self.manager)
        self.tetr_calc_button = pygame_gui.elements.UIButton(
                                                        relative_rect=pygame.Rect((WINDOW_WIDTH * 7 // 8, 375), (200, 50)),
                                                        text='Tetr fredgolm',
                                                        manager=self.manager)
        self.show_button_3d = pygame_gui.elements.UIButton(
                                                        relative_rect=pygame.Rect((WINDOW_WIDTH * 7 // 8, 425), (200, 50)),
                                                        text='Show solution 3d',
                                                        manager=self.manager)
        self.flip_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 475), (200, 50)),
                                                        text='Flip',
                                                        manager=self.manager)
        # self.line_center_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 425), (100, 50)),
        #                                                   text='Lines center',
        #                                                   manager=self.manager)
        # self.height_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH * 7//8, 475), (100, 50)),
        #                                                        text='Height',
        #                                                        manager=self.manager)

        # self.save_text_line_button = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
        #                                         relative_rect=pygame.Rect((WINDOW_WIDTH * 7 // 8, 575), (100, 50)),
        #                                         manager=self.manager)

        self.menu = None

        self.projection_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 0]])
        self.angle_x = self.angle_y = self.angle_z = DEFAULT_ANGLE
        self.rot_x = np.array(
            [[1, 0, 0], [0, cos(self.angle_x), -sin(self.angle_x)], [0, sin(self.angle_x), cos(self.angle_x)]])
        self.rot_y = np.array(
            [[cos(self.angle_y), 0, sin(self.angle_y)], [0, 1, 0], [-sin(self.angle_y), 0, cos(self.angle_y)]])
        self.rot_z = np.array(
            [[cos(self.angle_z), -sin(self.angle_z), 0], [sin(self.angle_z), cos(self.angle_z), 0], [0, 0, 1]])
        self.scale = 100

    def new_point(self, pos, isclicked = False) -> None:
        if isclicked:
            pos = [(pos[0] - WORKING_SPACE_WIDTH_HALF)/self.scale, (pos[1] - WORKING_SPACE_HEIGHT_HALF)/self.scale]
            NewPoint = Point(list(pos))
            NewPoint = Point(NewPoint.inv_project(NewPoint.coordinates, self.rot_x, self.rot_y, self.rot_z))
        else:
            NewPoint = Point(list(pos))

        if NewPoint not in self.points:
            NewPoint.idd = len(self.points)
            self.points.append(NewPoint)
            #pygame.draw.circle(self.background, 'black', pos, 4)
            # for line in self.lines:
            #     if Line.is_close(line, NewPoint, tol=1e-3):
            #         line[0].related.remove(line[1])
            #         line[1].related.remove(line[0])
            #         NewPoint.related.append(line[0])
            #         NewPoint.related.append(line[1])
            #         self.points[self.points.index(line[0])].related.append(NewPoint)
            #         self.points[self.points.index(line[0])].clean()
            #
            #         self.points[self.points.index(line[1])].related.append(NewPoint)
            #         self.points[self.points.index(line[1])].clean()
            #
            #         self.lines.remove(line)
            #         break

            for point in self.points[:-1]:
                NewLine = Line(NewPoint, point)
                if len(self.triangles) == 0:
                    self.lines.append(NewLine)
                    NewPoint.related.append(point)
                    point.related.append(NewPoint)
                    continue
                if not any([NewLine.isect_line_plane_v3_4d(t) for t in self.triangles]):
                    #if all([not line.intersect(NewLine) for line in self.lines]):
                    if point not in NewPoint.related:
                        self.lines.append(NewLine)
                        NewPoint.related.append(point)
                        point.related.append(NewPoint)

                # elif all([not line.intersect(NewLine) for line in self.lines]):
                #     self.lines.append(NewLine)
                #     NewPoint.related.append(point)
                #     point.related.append(NewPoint)
                #     pygame.draw.aaline(self.background, 'black', point.coord, NewPoint.coord, 1)
            self.triangles_creation()

    def triangles_creation(self) -> None:
        point = self.points[-1]
        for t in self.triangles:
            if t.is_in(point):
                self.triangles.remove(t)
        for next_point in point.related:
            for next_next_point in next_point.related:
                if point in next_next_point.related:
                    NewTriangle = Triangle(point, next_point, next_next_point)
                    if NewTriangle not in self.triangles:
                        self.triangles.append(NewTriangle)

    def tetrahedron_creation(self) -> None:
        for point in self.points:
            for next_point in point.related:
                for next_next_point in next_point.related:
                    if point in next_next_point.related:
                        for next_next_next_point in next_next_point.related:
                            if all([p in next_next_next_point.related for p in [point, next_point]]):
                                NewTetrahedron = Tetrahedron(point,
                                                             next_point,
                                                             next_next_point,
                                                             next_next_next_point)
                                if NewTetrahedron not in self.tetrahedron:
                                    self.tetrahedron.append(NewTetrahedron)

                            # x1, y1, z1 = point
                            # x2, y2, z2 = next_point
                            # x3, y3, z3 = next_next_point
                            # x4, y4, z4 = next_next_next_point
                            # res = np.linalg.det(np.array([[x1, x2, x3, x4],
                            #                               [y1, y2, y3, y4],
                            #                               [z1, z2, z3, z4],
                            #                               [1, 1, 1, 1]]))
                            # if abs(res) > 1e-4:
                            # # L1 = Line(point, next_point)
                            # # L2 = Line(point, next_next_point)
                            # # L3 = Line(point, next_next_next_point)
                            # # if not isclose(sum(L1.triple_prod(L2, L3)), 0, abs_tol=1e-3):
                            #     NewTetrahedron = Tetrahedron(point,
                            #                                  next_point,
                            #                                  next_next_point,
                            #                                  next_next_next_point)
                            #     if NewTetrahedron not in self.tetrahedron:
                            #         self.tetrahedron.append(NewTetrahedron)

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
        print('======TETRAHEDRONS===========')
        for tt in self.tetrahedron:
            print(tt)
            print(f'CENTER IS === {tt.center()}')
            print(f'VOLUME IS === {tt.volume()}')
        print(len(self.tetrahedron))


    def clear(self) -> None:
        for p in self.points:
            del p
        self.points = []
        self.lines = []
        self.triangles = []
        self.tetrahedron = []
        self.calculated = []
        self.calculated_3d = []
        self.fredgolm_flag = False
        self.fredgolm_flag_3d = False
        self.show_button.set_text('Show solution')
        self.show_button_3d.set_text('Show solution 3d')
        self.angle_x = self.angle_y = self.angle_z = DEFAULT_ANGLE

    def divide(self) -> None:
        centers = [t.center for t in self.triangles]
        for c in centers:
            self.new_point(c.coordinates)

        # min_square = min([t.square() for t in self.triangles])
        # for t in self.triangles:
        #     diff = t.square() / min_square
        #     if diff > 2:
        #         self.new_point(t.center.coordinates)

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
        flag = False
        for i in range(len(self.triangles)):
            for j in range(i, len(self.triangles)):
                FlaGG = False
                if self.triangles[j].is_related(self.triangles[i]):
                    for p in self.triangles[i].points:
                        if p not in self.triangles[j].points:
                            A = self.triangles[j].points[0] - p
                            B = self.triangles[j].points[1] - p
                            C = self.triangles[j].points[2] - p
                            res = np.linalg.det(np.array([[A[0], A[1], A[2]],
                                                       [B[0], B[1], B[2]],
                                                       [C[0], C[1], C[2]]]))
                            if isclose(res, 0, abs_tol=1e-3):
                                FlaGG = True
                    if not FlaGG:
                        continue
                    for p in self.triangles[i].points:
                        if p not in self.triangles[j].points:
                            index = self.triangles[i].points.index(p)
                    alpha = Line(self.triangles[i].points[index],
                                 self.triangles[i].points[(index+1)%3]).arcos_angle_between(
                        Line(self.triangles[i].points[index], self.triangles[i].points[(index+2)%3])
                    )

                    for p in self.triangles[j].points:
                        if p not in self.triangles[i].points:
                            index = self.triangles[j].points.index(p)
                    betha = Line(self.triangles[j].points[index],
                                 self.triangles[j].points[(index + 1) % 3]).arcos_angle_between(
                        Line(self.triangles[j].points[index], self.triangles[j].points[(index + 2) % 3])
                    )
                    if sin(alpha + betha) <= 0:
                        flag = True
                        self.flip(self.triangles[i], self.triangles[j])
        if flag:
            self.optimize()
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
                if self.state:
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
                    if keys[pygame.K_m]:
                        from time import sleep
                        if self.mstate:
                            next(self.gen)
                        self.mstate = False
                    if event.type == pygame.KEYUP:
                        print(event.key)
                        if event.key == 109:
                            self.mstate = True
                    if event.type == pygame.QUIT:
                        is_running = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        if event.button == 1:
                            pos = pygame.mouse.get_pos()
                            if pos[0] < WORKING_SPACE_WIDTH:
                                self.new_point(pos, isclicked=True)
                        elif event.button == 4:
                            if self.scale < 700:
                                self.scale += 7
                        elif event.button == 5:
                            if self.scale > 8:
                                self.scale -= 7
                if len(self.triangles) == 0:
                    self.tri_calc_button.disable()
                else:
                    self.tri_calc_button.enable()
                if len(self.tetrahedron) == 0:
                    self.tetr_calc_button.disable()
                else:
                    self.tetr_calc_button.enable()
                if len(self.calculated) == 0:
                    self.show_button.disable()
                else:
                    self.show_button.enable()
                if len(self.calculated_3d) == 0:
                    self.show_button_3d.disable()
                else:
                    self.show_button_3d.enable()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    # if self.redraw_button.check_pressed():
                    #     self.redraw(from_scracth=True)
                    if self.optimize_btn.check_pressed():
                        #turns = next(opt)
                        #if turns:
                        #    opt = self.optimize()
                        self.divide()
                        self.redraw(True)
                    if self.save_button.check_pressed():
                        self.save(mode=0)
                    if self.load_button.check_pressed():
                        self.menu = pygame_gui.windows.UIFileDialog(pygame.Rect((400, 300), (100, 100)), self.manager)
                        self.state = False
                    if self.rel_button.check_pressed():
                        self.rel()
                    if self.clear_button.check_pressed():
                        self.clear()
                    if self.menu is not None and event.ui_element == self.menu.ok_button:
                        path = self.menu.current_file_path
                        self.menu = None
                        #self.gen = self.load(path)
                        self.load(path)
                        self.state = True
                    if self.show_button.check_pressed():
                        if self.fredgolm_flag == False:
                            self.show_button.set_text('Hide solution')
                            self.fredgolm_flag = True
                        else:
                            self.show_button.set_text('Show solution')
                            self.fredgolm_flag = False
                    if self.show_button_3d.check_pressed():
                        if self.fredgolm_flag_3d == False:
                            self.show_button_3d.set_text('Hide solution 3d')
                            self.fredgolm_flag_3d = True
                        else:
                            self.show_button_3d.set_text('Show solution 3d')
                            self.fredgolm_flag_3d = False

                    if self.flip_button.check_pressed():
                        self.optimize()
                        self.redraw(from_scracth = True)
                    # if self.line_center_button.check_pressed():
                    #     self.line_center()
                    #     self.redraw(from_scracth = True)
                    # if self.height_button.check_pressed():
                    #     newp = self.triangles[0].get_height_intersect(self.triangles[0].points[2])
                    #     self.new_point(newp.coord)
                    #     print(self.triangles[0].integral(self.triangles[0].points[2]))
                    #     self.redraw(from_scracth = True)
                    if self.tetr_calc_button.check_pressed():
                        self.tetrahedron_creation()
                        self.calc(mode = 1)
                    if self.tri_calc_button.check_pressed():
                        self.calc()

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.redraw()

    def redraw(self, from_scracth = True) -> None:
        if from_scracth == True:
            #self.lines = []
            #self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            #self.background.fill(pygame.Color('#000000'))
            pygame.draw.rect(self.background, 'grey', rect=(0, 0, WINDOW_WIDTH * 7//8, WINDOW_HEIGHT), width=WINDOW_WIDTH * 7//8)

            font = pygame.font.SysFont('arial', 25)
            #pygame.draw.circle(self.background, 'red', (WORKING_SPACE_WIDTH_HALF, WORKING_SPACE_HEIGHT_HALF), 300, 4)
            #pygame.draw.circle(self.background, 'blue', (WORKING_SPACE_WIDTH_HALF + 150, WORKING_SPACE_HEIGHT_HALF + 150), 300, 4)

            for point in self.points:
                #text = font.render(str(point.idd), True, (0, 0, 0))

                xy = point.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix, scale=self.scale)
                x = xy[0]
                y = xy[1]
                #self.background.blit(text,
                #                      (x + WORKING_SPACE_WIDTH_HALF, y + WORKING_SPACE_HEIGHT_HALF))
                pygame.draw.circle(self.background, 'black', (x + WORKING_SPACE_WIDTH_HALF, y + WORKING_SPACE_HEIGHT_HALF), 4)

                # for related_p in point.related:
                #     NewLine = Line(point, related_p)
                #     if NewLine not in self.lines:
                #         if all([not line.intersect(NewLine) for line in self.lines]):
                #             self.lines.append(NewLine)
                #             p_xy = point.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix, scale=self.scale)
                #             p_x = p_xy[0]
                #             p_y = p_xy[1]
                #             rel_p_xy = related_p.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix, scale=self.scale)
                #             rel_p_x = rel_p_xy[0]
                #             rel_p_y = rel_p_xy[1]
                #             pygame.draw.aaline(self.background, 'black', (p_x + WORKING_SPACE_WIDTH_HALF,
                #                                                           p_y + WORKING_SPACE_HEIGHT_HALF),
                #                                (rel_p_x + WORKING_SPACE_WIDTH_HALF,
                #                                 rel_p_y + WORKING_SPACE_HEIGHT_HALF), 1)
            for line in self.lines:
                p = [el.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix, scale=self.scale) for el in line.points]
                pygame.draw.aaline(self.background, 'black', (p[0][0] + WORKING_SPACE_WIDTH_HALF,
                                                             p[0][1] + WORKING_SPACE_HEIGHT_HALF),
                                                             (p[1][0] + WORKING_SPACE_WIDTH_HALF,
                                                             p[1][1] + WORKING_SPACE_HEIGHT_HALF), 1)

            # i = 0
            # font = pygame.font.SysFont('arial', 50)
            # for triangle in self.triangles:
            #     text = font.render(str(i), True, (0, 0, 0))
            #     center = triangle.center.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix, scale=self.scale)
            #     self.background.blit(text, (center[0] + WORKING_SPACE_WIDTH_HALF, center[1] + WORKING_SPACE_HEIGHT_HALF))
            #     i += 1

        if self.fredgolm_flag:
            calcul = self.calculated
            min_calcul = abs(min(calcul))
            max_calcul = max(calcul) + min_calcul
            q_p = self.q.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix, scale=self.scale)
            pygame.draw.circle(self.background, 'black',
                               (q_p[0] + WORKING_SPACE_WIDTH_HALF, q_p[1] + WORKING_SPACE_HEIGHT_HALF), 10)
            for i in range(len(calcul)):
                kal = (calcul[i] + min_calcul) / max_calcul
                kal = kal ** 2
                p = self.triangles[i].center.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix,
                                                     scale=self.scale)
                pygame.draw.circle(self.background, (kal * 255, 0, (1 - kal) * 255),
                                   (p[0] + WORKING_SPACE_WIDTH_HALF, p[1] + WORKING_SPACE_HEIGHT_HALF), 8)
        if self.fredgolm_flag_3d:
            calcul = list(map(np.real, self.calculated_3d))
            min_calcul = abs(min(calcul))
            max_calcul = max(calcul) + min_calcul
            q_p = self.q.project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix, scale=self.scale)
            pygame.draw.circle(self.background, 'black',
                               (q_p[0] + WORKING_SPACE_WIDTH_HALF, q_p[1] + WORKING_SPACE_HEIGHT_HALF), 10)
            for i in range(len(calcul)):
                kal = (calcul[i] + min_calcul) / max_calcul
                if math.isnan(kal):
                    kal = 0
                p = self.tetrahedron[i].center().project(self.rot_x, self.rot_y, self.rot_z, self.projection_matrix,
                                                     scale=self.scale)
                pygame.draw.circle(self.background, (kal * 255, 0, (1 - kal) * 255),
                                   (p[0] + WORKING_SPACE_WIDTH_HALF, p[1] + WORKING_SPACE_HEIGHT_HALF), 4)

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
                if line[0] == '#':
                    continue
                self.new_point(tuple(map(float, line.split())))
                #yield

    def calc(self, mode = 0) -> None:
        if mode == 0:
            N = len(self.triangles)
            A, f, self.q = self.find_A(N)
            self.calculated = np.linalg.solve(A, f)
        if mode == 1:
            N = len(self.tetrahedron)
            A, f, self.q = self.find_A(N, mode = 1)
            self.calculated_3d = np.linalg.solve(A, f)
            print(f'ACCURACY IS {self.accuracy(self.analyt_sol(),self.calculated_3d)}')


    def core(self, p1: Point, p2: Point):
        return 1/(pi * 9) * (1/ abs(p1 - p2))

    def core_3d(self, p1: Point, p2: Point, mode = 'c', w = 2.5):
        return 1 / (pi * 4/3 * 27) * (1 / abs(p1 - p2))

        num = np.exp((1j * w * abs(p1 - p2)) / np.exp(1))
        denom = pi * 4/3 * 27 * abs(p1 - p2)
        if mode == 'f':
            return num
        else:
            return num / denom
        return 1/(abs(p1 - p2) * 4/3 * pi * 27)

    def exp_core(self, p1, p2):
        return p1[0] * p2[1]

    def exp_f(self, x: Point):
        return x[0]

    def analyt_sol(self):
        A = np.array([[8/9, -1/3], [-1/15, 8/9]])
        f = np.array([1, 1/3])
        c1, c2 = np.linalg.solve(A, f)
        c = 2/3 * (1.73 ** 3) / (1 + 2/3 * (1.73 ** 3))
        f = lambda x: x*(1 - c)
        return [f(i.center()[0]) for i in self.tetrahedron]

    def accuracy(self, true, calc):
        return sum([abs(x/y) for x, y in zip(true, calc)])/len(true)

    def find_A(self, N: int, f=None, mode = 0) -> list:
        if f is None:
            if mode == 0:
                f = self.core
            if mode == 1:
                f = self.core_3d
                #f = lambda x, y: x**2 + y**2
        A = []
        for i in range(0, N):
            temp = []
            for j in range(0, N):
                if j == i:
                    #temp.append(self.triangles[j].integral() * self.triangles[j].area())
                    temp.append(1)
                else:
                    if mode == 0:
                        temp.append(self.core(self.triangles[i].center, self.triangles[j].center) * self.triangles[j].area())
                    else:
                        temp.append(self.core_3d(self.tetrahedron[i].center(), self.tetrahedron[j].center())
                                   * self.tetrahedron[j].volume())
                        #temp.append(self.exp_core(self.tetrahedron[i].center(), self.tetrahedron[j].center()) * self.tetrahedron[j].volume())
            A.append(temp)

        A = np.array(A) + np.eye(len(A))
        q = self.q
        if mode == 0:
            f_vec = [f(i.center, q) for i in self.triangles]
        else:
            f_vec = []
            for i in self.tetrahedron:
                #x, y, z = i.center().coordinates
                #f_vec.append(f(x, y, z))
                f_vec = [self.core_3d(i.center(), q) for i in self.tetrahedron]
                #f_vec = [self.exp_f(i.center()) for i in self.tetrahedron]
        return [A, f_vec, q]


