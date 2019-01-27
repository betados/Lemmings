"""
    Module in charge of generating the map
"""
import pygame
import yaml
from vector_2d import Vector
from Interaction import Interaction


class Floor(object):
    """ A floor object is each of the separated point lists"""

    def __init__(self, size, pointList, discreteDebugging):
        # self.start = (50, size[1] * 0.7)
        # self.end = (size[0] - 500, size[1] * 0.1)
        self.size = size
        self.relleno = []
        self.rellenoLines = []
        self.pointListAdded = []
        if discreteDebugging:
            self.color = 0, 0, 150
        else:
            self.color = 0, 0, 255
        self.pointList = []
        # self.sprite = Sprite()

        # Rellena si faltan puntos entremedias
        # FIXME rellena en horizontal cuando deberia rellenar con una linea desde un punto hasta otro
        for i in range(-1, (len(pointList))*-1, -1):
            self.pointList.append(pointList[i])
            if (pointList[i - 1].x - pointList[i].x) > 1:
                for x in range(pointList[i].x + 1, pointList[i - 1].x):
                    self.pointList.append(Vector(x, pointList[i].y))
            if (pointList[i].x - pointList[i - 1].x) > 1:
                for x in range(pointList[i - 1].x, pointList[i].x + 1):
                    self.pointList.append(Vector(x, pointList[i].y))

        if abs(self.pointList[len(self.pointList) - 1] - self.pointList[0]) < 50:
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
        if False:
            # Cuadrado donde buscar para rellenar
            pointRange = [[9999, 0], [9999, 0]]
            for point in self.pointList:
                for i in range(2):
                    if point[i] < pointRange[i][0]:
                        pointRange[i][0] = point[i]
                    if point[i] > pointRange[i][1]:
                        pointRange[i][1] = point[i]

            for x in range(pointRange[0][0] - 10, pointRange[0][1] + 10):
                trigered = False
                yAnt = 0
                init = None
                end = None
                for y in range(pointRange[1][0] - 10, pointRange[1][1] + 10):
                    if point in self.pointList:
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
                    self.rellenoLines.append([init, end])

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
            pygame.draw.lines(screen, (100, 100, 10), False, (line[0], line[1]), 1)


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
