import random

import pygame
from vector_2d import Vector


class Floor(object):

    def __init__(self, screen):
        self.screen = screen
        self.point_list = []
        self.last_point = Vector(-9999, -9999)

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
        self.floor_list = []

    def newFloor(self):
        self.floor_list.append(Floor(self.screen))

    def add(self, point):
        self.floor_list[-1].add(point)

    def save(self, name):
        import yaml
        from Scenario import Floor
        new_floor_style_list = [Floor(self.res, floor.point_list, False) for floor in self.floor_list]

        yaml.dump(new_floor_style_list, open("maps/" + name + '.yaml', 'w'))

    def draw(self):
        # FLOORS
        for floor in self.floor_list:
            floor.draw()
