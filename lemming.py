"""
The lemming sprite module.

"""

import random

import pygame
from vector_2d import Vector
from typing import List, Tuple, Optional
from scenario import Floor
import warnings


class LemmingList(object):
    """ This class contains and handles the list of lemmings"""

    def __init__(self, quantity):
        self.lista = [Lemming(i) for i in range(quantity)]

    def draw(self, t, screen):
        """ Atualize position and draw each lemming"""
        # print('time', t)
        if t < 1000:
            for lemming in self.lista:
                lemming.actualize(t)
                lemming.draw(screen)

    def __getitem__(self, item):
        """ get the lemming """
        return self.lista[item]

    def __iter__(self):
        return iter(self.lista)


class Lemming(object):
    """ This class is the implementation of the lemmings sprites"""

    def __init__(self, index: int):
        self.index = index
        self.pos = Vector(60, index * -100)
        self.height = 32
        self.width = 20
        self.rect = pygame.Rect(self.pos(), (self.width, self.height))
        self.rect.bottomright = self.pos()
        self.knee = Vector()
        self.action = "Walk"
        self.parachuted = False
        self.stairCount = 0
        self.stairPos = None
        self.floor = None

        self.vel = Vector(0, 0.1)
        self.accel = Vector(0, 0)

        self.sprite = Sprite()
        self.totalWalkingImages = 10
        self.walkingImagePointer = random.randrange(7)

        self.total_falling_images = 4
        self.fallingImagePointer = random.randrange(0, 3)

        self.parachute_images = 4, 12
        self.parachute_pointer = 4

        self.total_dig_images = 8
        self.dig_image_pointer = 10

        self.total_bomb_images = 14
        self.bomb_pointer = 0

        self.image = self.get_next_image()
        self.times = 0
        self.period = 10
        self.timer = 0

        self.bomb_radius = self.width * 1.3
        self.dig_radius = self.width / 2
        self.bomb_set = {
            Vector(int(x), int(y)) for x in self.float_range(-self.bomb_radius, self.bomb_radius) for y in
            self.float_range(-self.bomb_radius, self.bomb_radius)
            if abs(Vector(x, y)) < self.bomb_radius}

        self.dig_set = {
            Vector(int(x), int(y)) for x in self.float_range(-self.dig_radius, self.dig_radius) for y in
            self.float_range(-self.dig_radius, self.dig_radius)
            if abs(Vector(x, y)) < self.dig_radius}

        self.complements = []

        self.character_dict = {"Walk": self.walk, "Stop": self.stop,
                               "Climb": self.climb, "Stairway": self.stairway,
                               "Bomb": self.bomb, 'Dig down': self.dig,
                               "Dig horiz.": self.dig, "Dig diag.": self.dig,
                               "Parachute": self.parachute, "Fall": self.fall}

        self.vel_dict = {"Walk": Vector(0.03, 0), "Stop": Vector(),
                         # "Climb": self.climb, "Stairway": self.stairway,
                         "Bomb": Vector(), "Dig down": Vector(0, 0.01),
                         "Dig horiz.": Vector(0.01, 0), "Dig diag.": Vector(0.007, 0.007),
                         "Parachute": Vector(0, 0.05), "Fall": Vector(0, 0.1)}

    @staticmethod
    def float_range(x: float, y: float, jump: float = 1):
        while x < y:
            yield x
            x += jump

    def actualize(self, t: int):
        """ Actualize the position and speed of the lemming """

        if self.action:
            self.character_dict[self.action](t)
            if self.action in self.vel_dict:
                self.vel = self.vel_dict[self.action]

        self.pos += self.vel * t
        self.rect.bottomright = self.pos()
        self.knee = self.pos - Vector(self.width / 2, self.width / 5)

    def draw(self, screen, discrete_debugging: bool = False):
        """Draw the lemming"""
        if discrete_debugging:
            pygame.draw.rect(screen, (0, 50, 0), self.rect, 1)
        else:
            pygame.draw.rect(screen, (0, 50, 0), self.rect, 1)
            self.times += 1
            if self.times > self.period:
                self.image = self.get_next_image()
                self.times = 0
            screen.blit(self.sprite.image, self.rect, self.image)

        for complement in self.complements:
            complement.draw()

    def get_next_image(self) -> Tuple[int, int, int, int]:
        """Return the corresponding image for the sprite"""
        width = 50
        height = 50
        offset = 9
        # pointer = None
        if self.action == "Fall":
            if self.parachuted:
                self.parachute_pointer += 1
                if self.parachute_pointer >= self.parachute_images[1]:
                    self.parachute_pointer = self.parachute_images[0] + 3
                pointer = self.parachute_pointer
                line = 2
            else:
                self.fallingImagePointer += 1
                if self.fallingImagePointer >= self.total_falling_images:
                    self.fallingImagePointer = 0
                pointer = self.fallingImagePointer
                line = 2

        elif self.action == 'Dig down':
            self.dig_image_pointer += 1
            if self.dig_image_pointer >= self.total_dig_images:
                self.dig_image_pointer = 0
            pointer = self.dig_image_pointer
            line = 8

        elif self.action == 'Bomb':
            self.bomb_pointer += 1
            if self.bomb_pointer >= self.total_bomb_images:
                self.bomb_pointer = 0
            pointer = self.bomb_pointer
            line = 13

        else:
            self.walkingImagePointer += 1
            if self.walkingImagePointer >= self.totalWalkingImages:
                self.walkingImagePointer = 0
            pointer = self.walkingImagePointer
            line = 0

        return width * pointer + offset, height * line, width - offset, height

    def is_walking(self) -> bool:
        """Is the lemming walking?"""
        return self.action == "Walk"

    # ACTIONS for switch-case statement
    def walk(self, t):
        """ case """
        self.parachute_pointer = self.parachute_images[0]

    def fall(self, t):
        """ case """
        # self.vel = Vector(0, 0.1)

    def stop(self, t):
        """ case """
        warnings.warn('Not implemented')

    def bomb(self, t):
        """ case """
        self.timer += t
        if self.timer >= 2333:
            self.vel = Vector()
            for point in self.floor.point_list.lista:
                if abs(point - self.knee) < self.bomb_radius:
                    self.floor.point_list.remove(point)

            self.floor.point_list.relleno -= {self.knee.int_vector() + point for point in self.bomb_set}

        # TODO hacer que muera el lemming

    def climb(self, t):
        """ case """
        warnings.warn('Not implemented')

    def stairway(self, t):
        """ case """
        self.timer += t
        self.vel = Vector()
        if self.timer >= 500:
            self.timer = 0
            if not self.stairPos:
                self.stairPos = self.pos
            else:
                self.stairPos += Vector(7, -4)
                self.pos = self.stairPos
            self.complements.append(Step(self.stairPos, self.screen, self.floor))
            self.stairCount += 1
        if self.stairCount >= 15:
            self.stairCount = 0
            self.stairPos = None
            self.action = "Walk"

    def dig(self, t):
        """ case """
        self.floor.point_list.relleno -= {self.knee.int_vector() + point for point in self.dig_set}

    def parachute(self, t):
        """ case """
        self.parachuted = True
        self.vel_dict['Fall'] = self.vel_dict['Parachute']
        self.action = 'Fall'
        # warnings.warn('Not implemented')


class Sprite(pygame.sprite.Sprite):
    # FIXME esta clase sobra, pero si la quito da un error que ahora mismo no se arreglar.
    def __init__(self):
        # self.image = pygame.Surface([5, 5])
        self.image = pygame.image.load("images/lemmings_classic.png").convert()
        # self.image = pygame.transform.scale2x(self.image)
        # factor = 2.5
        int_mul = lambda x: int(x * 2.5)
        self.image = pygame.transform.scale(self.image, (int_mul(437), int_mul(710)))


class Step(object):
    """ The stair step object that"""
    width = 10
    height = 3

    def __init__(self, pos: Vector, screen, floor: Floor):
        # down left corner
        self.pos = pos
        self.screen = screen
        self.point_list = []

        pointer = self.pos
        self.point_list.append(pointer)

        pointer += Vector(Step.width, 0)
        self.point_list.append(pointer)

        pointer += Vector(0, -Step.height)
        self.point_list.append(pointer)

        pointer += Vector(-Step.width, 0)
        self.point_list.append(pointer)

        floor.point_list.relleno |= {Vector(x, y) for x in range(int(self.pos.x), int(self.pos.x) + Step.width + 1)
                                     for y in range(int(self.pos.y) - Step.height, int(self.pos.y) + 1)}

    def draw(self):
        """ Draws it"""
        pygame.draw.lines(self.screen, (150, 150, 150), True, [point.int() for point in self.point_list], 1)
