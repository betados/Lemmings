import random

import pygame
from vector_2d import Vector


class Floor(object):

    def __init__(self):
        self.point_list = []
        self.last_point = Vector(-9999, -9999)
        # self.color = random.randrange(256) / 255, random.randrange(256) / 255, random.randrange(256) / 255
        self.color = random.randrange(256) / 600, random.randrange(256) / 600, random.randrange(256) / 600

    def draw(self, screen):
        if len(self.point_list) > 2:
            pygame.draw.lines(screen, (100, 100, 100), False, list(self.get_points()), 1)  # filled

    def get_points(self):
        for point in self.point_list:
            yield point()

    def add(self, point):
        self.point_list.append(Vector(*point))


class Scenario(object):

    def __init__(self, res):
        self.res = res
        self.index = -1
        self.floorList = []
        # self.floor = Floor(res)

    def newFloor(self):
        # self.floor = Floor()
        self.floorList.append(Floor())
        self.index += 1

    def add(self, point):
        self.floorList[self.index].add(point)

    def save(self, name):
        import yaml

        yaml.dump(self.floorList, open("maps/" + name + '.yaml', 'w'))

    def draw(self, screen):
        # FLOORS
        for floor in self.floorList:
            floor.draw(screen)
