from classes.Frame import Frame
from classes.Point import Point
import concurrent.futures
import numpy as np


class Scene:
    objects: list

    def __init__(self, file):
        self.objects = self.__parse(file)

    def __parse(self, file):
        parsed_list = []
        with open(file, 'r') as text:
            object_num = int(text.readline())
            for object in range(0, object_num):
                parsed_list.append([])
                modules_num = int(text.readline())
                for module in range(0, modules_num):
                    parsed_list[object].append([])
                    text.readline()
                    lines_num = int(text.readline())
                    text.readline()
                    for lines in range(0, lines_num):
                        points = []
                        line = text.readline().strip().split()
                        idx = f'{str(object)}_{str(module)}_{str(lines)}'
                        for start, name in zip(range(0, 12, 3), 'ABCD'):
                            points.append(Point([x for x in map(float, line[start: start + 3])],
                                                name=name + idx))
                        parsed_list[object][module].append(
                            Frame(points[0], points[1], points[2], points[3], index=idx))
        return parsed_list

    def colocation(self, n_frame, n_obj=0, n_module=0):
        frame = self.objects[n_obj][n_module][n_frame]
        return sum(frame.integral_summ(other) for other in self)

    def __iter__(self):
        return next(self)

    def __next__(self):
        for object in self.objects:
            for module in object:
                for frame in module:
                    yield frame

    def __len__(self):
        s = 0
        for object in self.objects:
            for module in object:
                s += len(module)
        return s

    def __getitem__(self, item3=0, item2=0, item1=0):
        return self.objects[item1][item2][item3]

    def calculate_colocation(self, start, end):
        res = []
        for i in range(start, end):
            result = self.colocation(i)
            res.append(result)
        return start, res

    def calculate_all_colocations(self, n_proc=1):
        res = []
        ret = []
        l = len(self)
        s = int(l / n_proc)
        with concurrent.futures.ProcessPoolExecutor(max_workers=n_proc) as executor:
            results = [executor.submit(self.calculate_colocation, start, min(start + s, l))
                       for start in range(0, l, s)]

            for proc in concurrent.futures.as_completed(results):
                ret.append(proc.result())

        for result in sorted(ret, key=lambda x: x[0]):
            res += result[1]
        return res

    def calculate_diag_colocation(self, start, end):
        res = []
        for i in range(start, end):
            res.append(self[i].integral_summ(self[i]))
        return start, res

    def calculate_diag_colocations(self, n_proc=1):
        res = []
        ret = []
        l = len(self)
        s = int(l / n_proc)
        with concurrent.futures.ProcessPoolExecutor(max_workers=n_proc) as executor:
            results = [executor.submit(self.calculate_diag_colocation, start, min(start + s, l))
                       for start in range(0, l, s)]

            for proc in concurrent.futures.as_completed(results):
                ret.append(proc.result())

        for result in sorted(ret, key=lambda x: x[0]):
            res += result[1]
        return res

    def calculate_k(self, func, start, end):
        res = []
        for i in range(start, end):
            res1 = []
            for frame in self:
                res1.append(self[i].calk_k(frame, func))
            #res1.append(1)
            res.append(res1)
        return start, res

    def calculate_all_k(self, n_proc=1, func=lambda p1, p2: 1):
        res = []
        ret = []
        l = len(self)
        s = int(l / n_proc)
        with concurrent.futures.ProcessPoolExecutor(max_workers=n_proc) as executor:
            results = [executor.submit(self.calculate_k, func, start, min(start + s, l)) for start in range(0, l, s)]

            for proc in concurrent.futures.as_completed(results):
                ret.append(proc.result())

            for result in sorted(ret, key=lambda x: x[0]):
                res += result[1]
        #res += [[1] * len(res[0])]
        return np.array(res)
