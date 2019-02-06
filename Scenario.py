"""
    Module in charge of generating the map
"""
import pygame
import yaml
from vector_2d import Vector

from pointList import PointList


class Floor(object):
    """ A floor object is each of the separated point lists"""

    def __init__(self, size, discreteDebugging=False):
        self.size = size
        self.relleno: str = []
        self.relleno_points = []
        self.pointListAdded = []
        if discreteDebugging:
            self.color = 0, 0, 150
        else:
            self.color = 0, 0, 255
        self.pointList = PointList()

    def connect(self):
        # Rellena si faltan puntos entremedias
        # FIXME a veces sale del while sin tener que hacerlo por eso lo ejecuto varias veces
        for _ in range(9):
            fake_list = self.pointList.lista[:]
            for i, p in enumerate(fake_list):
                line = p - fake_list[i - 1]
                if abs(line) > 1.5:
                    j = 1
                    while (line.unit() * j + fake_list[i - 1]).int_vector() not in self.pointList.set:
                        self.pointList.append(line.unit() * j + fake_list[i - 1])
                        j += 1

        print('connected')

    def fill(self):
        vertical_set = set()
        for x in range(int(self.pointList.leftest.x + 1), int(self.pointList.rightest.x)):
            inside = False
            for y in range(int(self.pointList.highest.y - 1), int(self.pointList.lowest.y)):
                if Vector(x, y) in self.pointList.set:
                    inside = not inside
                elif inside:
                    vertical_set.add(Vector(x, y))

        horizontal_set = set()
        for y in range(int(self.pointList.highest.y + 1), int(self.pointList.lowest.y)):
            inside = False
            for x in range(int(self.pointList.leftest.x - 1), int(self.pointList.rightest.x)):
                if Vector(x, y) in self.pointList.set:
                    inside = not inside
                elif inside:
                    horizontal_set.add(Vector(x, y))

        self.relleno_points += list((vertical_set.intersection(horizontal_set)))
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

    def complete_select_strategy(self):
        if abs(self.pointList[-1] - self.pointList[0]) < 100:
            print("cierra el circulo")
            self.complete(self.pointList[0], self.pointList[len(self.pointList) - 1], self.pointList, 0)
        else:
            # Completa verticalmente desde el final hasta el suelo
            # s = size[0], size[1]-50
            self.complete(self.pointList[len(self.pointList) - 1], self.size, self.pointList, axis=1)
            # Completa horizontalmente desde el final hasta el inicio por el suelo
            self.complete(self.pointList[len(self.pointList) - 1], self.pointList[0], self.pointList, axis=0)
            # Completa verticalmente desde el final hasta el inicio
            self.complete(self.pointList[len(self.pointList) - 1], self.pointList[0], self.pointList, axis=1)

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
        for i, point in enumerate(self.pointList.set):
            pygame.draw.circle(screen, self.color, point.int(), 2, 2)
            # text = pygame.font.Font(None, 15).render(str(i), 1, (0, 255, 0))
            # screen.blit(text, point())
        for point in self.pointListAdded:
            pygame.draw.circle(screen, (100, 0, 0), point(), 4, 4)
        for point in self.relleno:
            pygame.draw.circle(screen, (100, 100, 10), point(), 1, 1)
        for point in self.relleno_points:
            pygame.draw.circle(screen, (100, 100, 10), point.int(), 1, 1)
            # pygame.draw.lines(screen, (100, 100, 10), False, (line[0](), line[1]()), 1)

        pygame.draw.circle(screen, (255, 0, 0), self.pointList.rightest.int(), 3, 3)
        pygame.draw.circle(screen, (255, 0, 0), self.pointList.leftest.int(), 3, 3)
        pygame.draw.circle(screen, (255, 0, 0), self.pointList.highest.int(), 3, 3)
        pygame.draw.circle(screen, (255, 0, 0), self.pointList.lowest.int(), 3, 3)

    def add(self, point):
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

    def add(self, point):
        self.floor_list[-1].add(point)

    def save(self, name):
        import yaml
        for floor in self.floor_list:
            floor.connect()
            # floor.complete_select_strategy()
            floor.fill()

        yaml.dump(self.floor_list, open("maps/" + name + '.yaml', 'w'))

    def draw(self):
        """ draws each floor """
        for floor in self.floor_list:
            floor.draw(self.screen)
