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
        self.relleno = set()
        self.color = 0, 0, 255
        self.point_list = PointList()

    def connect(self):
        """ Rellena si faltan puntos entremedias """
        self.point_list.set = set(self.point_list.lista)
        original_set = set(self.point_list.lista)
        for i, p in enumerate(self.point_list.lista):
            line = (p - self.point_list.lista[i - 1]).unit()
            while (self.point_list.lista[i - 1] + line).int_vector() not in original_set:
                self.point_list.add(line + self.point_list.lista[i - 1])
                line += line.unit()
        print('connected')

    def fill(self):
        self.point_list.calc_bounding_box()
        vertical_set = set()
        for x in range(int(self.point_list.leftest + 1), int(self.point_list.rightest)):
            inside = False
            for y in range(int(self.point_list.highest - 1), int(self.point_list.lowest)):
                if Vector(x, y) in self.point_list.set and Vector(x, y - 1) not in self.point_list.set:
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

        if self.relleno:
            for x in range(int(self.point_list.leftest + 1), int(self.point_list.rightest), 5):
                for y in range(int(self.point_list.highest - 1), int(self.point_list.lowest), 5):
                    if Vector(x, y) in self.relleno:
                        pygame.draw.circle(screen, (100, 100, 10), (x, y), 3, 3)

    def add(self, point):
        self.point_list.add(Vector(*point))

    def append(self, point):
        self.point_list.append(Vector(*point))


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
            floor.connect()
            floor.fill()

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
