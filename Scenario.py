"""
    Module in charge of generating the map
"""
import pygame
from ruamel.yaml import YAML
from vector_2d import Vector

from pointList import PointList


class Floor(object):
    """ A floor object is each of the separated point lists"""

    def __init__(self, size):
        self.size = size
        self.color = 0, 0, 255
        self.point_list = PointList()

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
            for point in self.point_list:
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
            for i, point in enumerate(self.point_list.lista):
                pygame.draw.circle(screen, self.color, point.int(), 1, 1)
            for i, point in enumerate(self.point_list.set):
                pygame.draw.circle(screen, self.color, point.int(), 1, 1)

        if self.point_list.relleno:
            for point in self.point_list:
                pygame.draw.circle(screen, (100, 100, 10), point.int(), 3, 3)

    def add(self, point):
        self.point_list.add(Vector(*point))

    def append(self, point):
        self.point_list.append(Vector(*point))

    def complete(self):
        self.point_list.connect()
        self.point_list.fill()


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([5, 5])
        self.image = pygame.image.load("images/grass.png").convert_alpha()


class Scenario(object):
    """ It contains and handles the list of floors"""

    def __init__(self, screen, size):
        self.size = size

        self.screen = screen
        self.floor_list = []

    def load(self, font):
        yaml = YAML(typ='safe')
        yaml.register_class(Floor)
        yaml.register_class(Vector)
        yaml.register_class(PointList)
        self.floor_list = yaml.load(open(font))

    def new_floor(self):
        self.floor_list.append(Floor(self.size))

    def append(self, point):
        self.floor_list[-1].append(point)

    def save(self, name):
        for floor in self.floor_list:
            floor.complete()

        yaml = YAML()
        yaml.default_flow_style = False
        yaml.register_class(Floor)
        yaml.register_class(Vector)
        yaml.register_class(PointList)
        yaml.dump(self.floor_list, open("maps/" + name + '.yaml', 'w'))

    def draw(self, status):
        """ draws each floor """
        for floor in self.floor_list:
            floor.draw(self.screen, status)
