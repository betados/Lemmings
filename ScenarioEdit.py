import random

import pygame
from vector_2d import Vector


class Floor(object):

    def __init__(self, screen):
        self.screen = screen
        self.point_list = []
        self.last_point = Vector(-9999, -9999)
        # self.color = random.randrange(256) / 255, random.randrange(256) / 255, random.randrange(256) / 255
        self.color = random.randrange(256) / 600, random.randrange(256) / 600, random.randrange(256) / 600

    def draw(self):
        if len(self.point_list) > 2:
            pygame.draw.lines(self.screen, (100, 100, 100), False, list(self.get_points()), 1)  # filled

    def get_points(self):
        for point in self.point_list:
            yield point()

    def add(self, point):
        self.point_list.append(Vector(*point))


class Scenario(object):

    def __init__(self, screen, res):
        self.screen = screen
        self.res = res
        self.index = -1
        self.floor_list = []

    def newFloor(self):
        self.floor_list.append(Floor(self.screen))
        self.index += 1

    def add(self, point):
        self.floor_list[self.index].add(point)

    def save(self, name):
        import yaml
        from Scenario import Floor
        new_floor_style_list = []
        for floor in self.floor_list:
            new_floor_style_list.append(Floor(self.res, floor.point_list, False))

        yaml.dump(new_floor_style_list, open("maps/" + name + '.yaml', 'w'))

    def draw(self):
        # FLOORS
        for floor in self.floor_list:
            floor.draw()
