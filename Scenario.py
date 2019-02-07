"""
    Module in charge of generating the map
"""
import pygame
import yaml
from vector_2d import Vector
import time

from pointList import PointList


class Floor(object):
    """ A floor object is each of the separated point lists"""

    def __init__(self, size, discreteDebugging=False):
        self.size = size
        self.relleno = set()
        if discreteDebugging:
            self.color = 0, 0, 150
        else:
            self.color = 0, 0, 255
        self.pointList = PointList()

    def connect(self):
        """ Rellena si faltan puntos entremedias """
        self.pointList.set = set(self.pointList.lista)
        original_set = set(self.pointList.lista)
        for i, p in enumerate(self.pointList.lista):
            line = (p - self.pointList.lista[i - 1]).unit()
            while (self.pointList.lista[i - 1] + line).int_vector() not in original_set:
                self.pointList.add(line + self.pointList.lista[i - 1])
                line += line.unit()
        # self.pointList.order_list()
        # print(self.pointList.lista)
        print('connected')

    def fill(self):
        vertical_set = set()
        for x in range(int(self.pointList.leftest.x + 1), int(self.pointList.rightest.x)):
            inside = False
            for y in range(int(self.pointList.highest.y - 1), int(self.pointList.lowest.y)):
                if Vector(x, y) in self.pointList.set and Vector(x, y - 1) not in self.pointList.set:
                    inside = not inside
                elif inside:
                    vertical_set.add(Vector(x, y))

        self.relleno = vertical_set
        print('filled')

    def point_is_inside_closed_lines(self, point):
        """
            This function is slow. Use it carefully
        """
        # FIXME no funciona perfecto todas las veces
        if point.y > self.size[1] / 2:
            rango = (0, int(self.size[1] - point.y), 1)
        else:
            rango = (0, -int(point.y), -1)
        times = 0
        for i in range(*rango):
            p = point + Vector(0, i)
            for point in self.pointList:
                if abs(p - point) < 1:
                    times += 1
        # print times
        # I divide it cause, when crossing each line, two points are at less than one of distance
        # TODO esto puede ser una linea
        if times % 2 != 0:
            return True
        else:
            return False

    def draw(self, screen, status):
        """ draw the floor """
        if status == 'drawing':
            for i, point in enumerate(self.pointList.lista):
                pygame.draw.circle(screen, self.color, point.int(), 1, 1)
            for i, point in enumerate(self.pointList.set):
                pygame.draw.circle(screen, self.color, point.int(), 1, 1)
            # text = pygame.font.Font(None, 15).render(str(i), 1, (0, 255, 0))
            # screen.blit(text, point())
        for point in self.relleno:
            pygame.draw.circle(screen, (100, 100, 10), point.int(), 1, 1)
            # pygame.draw.lines(screen, (100, 100, 10), False, (line[0](), line[1]()), 1)

        # pygame.draw.circle(screen, (255, 0, 0), self.pointList.rightest.int(), 3, 3)
        # pygame.draw.circle(screen, (255, 0, 0), self.pointList.leftest.int(), 3, 3)
        # pygame.draw.circle(screen, (255, 0, 0), self.pointList.highest.int(), 3, 3)
        # pygame.draw.circle(screen, (255, 0, 0), self.pointList.lowest.int(), 3, 3)

    def add(self, point):
        self.pointList.add(Vector(*point))

    def append(self, point):
        self.pointList.append(Vector(*point))


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([5, 5])
        self.image = pygame.image.load("images/grass.png").convert_alpha()


class Scenario(object):
    """ It contains and handles the list of floors"""

    def __init__(self, screen, size, discreteDebugging=False):
        self.size = size

        self.screen = screen
        self.floor_list = []

    def load(self, font):
        self.floor_list = yaml.load(open(font))

    def newFloor(self):
        self.floor_list.append(Floor(self.size))

    def append(self, point):
        self.floor_list[-1].append(point)

    def save(self, name):
        import yaml
        for floor in self.floor_list:
            floor.connect()
            # floor.complete_select_strategy()
            floor.fill()

        yaml.dump(self.floor_list, open("maps/" + name + '.yaml', 'w'))

    def draw(self, status):
        """ draws each floor """
        for floor in self.floor_list:
            floor.draw(self.screen, status)
