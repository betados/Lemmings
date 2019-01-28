"""
    Module in charge of generating the map
"""
import pygame
import yaml
from vector_2d import Vector, distance_point_segment


class PointList(object):
    def __init__(self, lista=None):
        self.lista = lista if lista else []

    @property
    def leftest(self):
        return sorted(self.lista, key=lambda point: point.x)[0]

    @property
    def rightest(self):
        return sorted(self.lista, key=lambda point: point.x)[-1]

    @property
    def highest(self):
        return sorted(self.lista, key=lambda point: point.y)[0]

    @property
    def lowest(self):
        return sorted(self.lista, key=lambda point: point.y)[-1]

    def __getitem__(self, item: int):
        return self.lista[item]

    def append(self, element: Vector):
        self.lista.append(element)

    def remove(self, item: Vector):
        self.lista.remove(item)

    def pop(self, index: int = -1):
        return self.lista.pop(index)

    def __len__(self) -> int:
        return len(self.lista)


class Floor(object):
    """ A floor object is each of the separated point lists"""

    def __init__(self, size, pointList, discreteDebugging):
        self.size = size
        self.relleno: str = []
        self.rellenoLines = []
        self.pointListAdded = []
        if discreteDebugging:
            self.color = 0, 0, 150
        else:
            self.color = 0, 0, 255
        self.pointList = PointList()

        # Rellena si faltan puntos entremedias
        # FIXME rellena en horizontal cuando deberia rellenar con una linea desde un punto hasta otro
        for i in range(-1, (len(pointList)) * -1, -1):
            self.pointList.append(pointList[i])
            if (pointList[i - 1].x - pointList[i].x) > 1:
                for x in range(pointList[i].x + 1, pointList[i - 1].x):
                    self.pointList.append(Vector(x, pointList[i].y))
            if (pointList[i].x - pointList[i - 1].x) > 1:
                for x in range(pointList[i - 1].x, pointList[i].x + 1):
                    self.pointList.append(Vector(x, pointList[i].y))

        if abs(self.pointList[len(self.pointList) - 1] - self.pointList[0]) < 100:
            print("cierra el circulo")
            self.complete(self.pointList[0], self.pointList[len(self.pointList) - 1], self.pointList, 0)
        else:
            # Completa verticalmente desde el final hasta el suelo
            # s = size[0], size[1]-50
            self.complete(self.pointList[len(self.pointList) - 1], size, self.pointList, axis=1)
            # Completa horizontalmente desde el final hasta el inicio por el suelo
            self.complete(self.pointList[len(self.pointList) - 1], self.pointList[0], self.pointList, axis=0)
            # Completa verticalmente desde el final hasta el inicio
            self.complete(self.pointList[len(self.pointList) - 1], self.pointList[0], self.pointList, axis=1)

        # RELLENO
        if True:
            for x in range(self.pointList.leftest.x, self.pointList.rightest.x + 1):
                trigered = False
                yAnt = 0
                init = None
                end = None
                for y in range(self.pointList.highest.y, self.pointList.lowest.y + 1):
                    if Vector(x, y) in self.pointList:
                        if trigered and y - yAnt > 5:
                            yAnt = y
                            trigered = False
                            end = [x, y]
                        if not trigered and y - yAnt > 5:
                            yAnt = y
                            trigered = True
                            init = [x, y]
                            continue
                    if trigered:
                        pass
                if init is not None and end is not None:
                    self.rellenoLines.append(
                        [Vector(*init), Vector(*end)]
                    )

    def point_is_inside_closed_lines(self, point, lines_list):
        """
            This function is slow. Use it carefully
        """
        # FIXME no funciona perfecto todas las veces
        if point.y > self.size[1] / 2:
            rango = (0, self.size[1] - point.y, 1)
        else:
            rango = (0, -point.y, -1)
        times = 0
        for i in range(*rango):
            p = point + Vector(0, i)
            for line in lines_list:
                if distance_point_segment(p, line) < 1:
                    times += 1
        # print times
        # I divide it cause, when crossing each line, two points are at less than one of distance
        if (times / 2) % 2 != 0:
            return True
        else:
            return False

    def connect(self):
        new_point_list = []
        for i in range(-1, (len(self.pointList)) * -1, -1):
            new_point_list.append(self.pointList[i])
            if (self.pointList[i - 1].x - self.pointList[i].x) > 1:
                for x in range(self.pointList[i].x + 1, self.pointList[i - 1].x):
                    new_point_list.append(Vector(x, self.pointList[i].y))
            if (self.pointList[i].x - self.pointList[i - 1].x) > 1:
                for x in range(self.pointList[i - 1].x, self.pointList[i].x + 1):
                    new_point_list.append(Vector(x, self.pointList[i].y))

        self.pointList = new_point_list

    @staticmethod
    def complete(point1, point2, pointList, axis=0):
        if point2[axis] < point1[axis]:
            interval = -1
        else:
            interval = 1
        for i in range(point1[axis], point2[axis], interval):
            if axis == 0:
                pointList.append(Vector(i, point1.y))
            if axis == 1:
                pointList.append(Vector(point1.x, i))

    def draw(self, screen):
        """ draw the floor """
        #
        for point in self.pointList:
            pygame.draw.circle(screen, self.color, point(), 2, 2)
        for point in self.pointListAdded:
            pygame.draw.circle(screen, (100, 0, 0), point(), 4, 4)
        for point in self.relleno:
            pygame.draw.circle(screen, (100, 100, 10), point(), 1, 1)
        for line in self.rellenoLines:
            pygame.draw.lines(screen, (100, 100, 10), False, (line[0](), line[1]()), 1)

        pygame.draw.circle(screen, (255, 0, 0), self.pointList.rightest(), 3, 3)
        pygame.draw.circle(screen, (255, 0, 0), self.pointList.leftest(), 3, 3)
        pygame.draw.circle(screen, (255, 0, 0), self.pointList.highest(), 3, 3)
        pygame.draw.circle(screen, (255, 0, 0), self.pointList.lowest(), 3, 3)


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([5, 5])
        self.image = pygame.image.load("images/grass.png").convert_alpha()


class Scenario(object):
    """ It contains and handles the list of floors"""

    def __init__(self, screen, res, font=None, discreteDebugging=False):
        self.size = res

        self.screen = screen

        self.floorList = yaml.load(open(font))

    def draw(self):
        """ draws each floor """
        for floor in self.floorList:
            floor.draw(self.screen)
