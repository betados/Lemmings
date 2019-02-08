"""
The lemming sprite module.

"""

import random

import pygame
from vector_2d import Vector
from typing import List, Tuple, Optional
from Scenario import Floor


class LemmingList(object):
    """ This class contains and handles the list of lemmings"""

    def __init__(self, quantity, screen):
        self.complements = []
        self.lista = [Lemming(i, screen, self.complements) for i in range(quantity)]

    def draw(self, t, screen):
        """ Atualize position and draw each lemming"""
        # print('time', t)
        if t < 1000:
            for lemming in self.lista:
                lemming.actualize(t)
                lemming.draw(screen)

            for complement in self.complements:
                complement.draw(screen)

    def __getitem__(self, item):
        """ get the lemming """
        return self.lista[item]

    def __iter__(self):
        return iter(self.lista)


class Lemming(object):
    """ This class is the implementation of the lemmings sprites"""
    def __init__(self, index: int, screen, complements: List):
        self.complements = complements
        self.screen = screen
        self.index = index
        self.pos = Vector(60, (index - 10) * 100)
        self.height = 36
        self.width = 22
        self.rect = pygame.Rect(self.pos(), (self.width, self.height))
        self.rect.bottomright = self.pos()
        self.knee = Vector()
        self.action = "Walk"
        self.stairCount = 0
        self.stairPos = None
        self.floor = None

        self.vel = Vector(0, 0.1)
        self.accel = Vector(0, 0)

        self.sprite = Sprite()
        self.totalWalkingImages = 7
        self.walkingImagePointer = random.randrange(7)
        self.totalFallingImages = 3
        self.fallingImagePointer = random.randrange(1, 3)
        self.image = self.get_next_image()
        self.times = 0
        self.period = 10
        self.timer = 0

        self.bomb_radius = self.width * 1.3
        self.bomb_set = {
            Vector(int(x), int(y)) for x in self.float_range(-self.bomb_radius, self.bomb_radius) for y in
            self.float_range(-self.bomb_radius, self.bomb_radius)
            if abs(Vector(x, y)) < self.bomb_radius}

        self.characterDict = {"Walk": self.walk, "Stop": self.stop,
                              "Climb": self.climb, "Stairway": self.stairway,
                              "Bomb": self.bomb, "Dig down": self.dig,
                              "Dig horiz.": self.dig, "Dig diag.": self.dig,
                              "Parachute": self.parachute, "Fall": self.fall}

    @staticmethod
    def float_range(x: float, y: float, jump: float = 1):
        while x < y:
            yield x
            x += jump

    def actualize(self, t: int):
        """ Actualize the position and speed of the lemming """

        if self.action:
            self.characterDict[self.action](t)

        self.pos += self.vel * t
        self.rect.bottomright = self.pos()
        self.knee = self.pos - Vector(self.width / 2, self.width / 5)

    def draw(self, screen, discrete_debugging: bool = True):
        """Draw the lemming"""
        if discrete_debugging:
            pygame.draw.rect(screen, (0, 50, 0), self.rect, 1)
        else:
            self.times += 1
            if self.times > self.period:
                self.image = self.get_next_image()
                self.times = 0
            screen.blit(self.sprite.image, self.rect, self.image)

    def get_next_image(self) -> Tuple[int, int, int, int]:
        """Return the corresponding image for the sprite"""
        side = 46
        if self.action == "Fall":
            self.fallingImagePointer += 1
            if self.fallingImagePointer >= self.totalFallingImages:
                self.fallingImagePointer = 1
            return 50 * self.fallingImagePointer + 8, side * 5, side, side - 10
        else:
            self.walkingImagePointer += 1
            if self.walkingImagePointer >= self.totalWalkingImages:
                self.walkingImagePointer = 0
            return 50 * self.walkingImagePointer + 8, side * 2, side, side - 10

    def is_walking(self) -> bool:
        """Is the lemming walking?"""
        return self.action == "Walk"

    # ACTIONS for switch-case statement
    def walk(self, t):
        """ case """
        pass

    def fall(self, t):
        """ case """
        self.vel = Vector(0, 0.1)

    def stop(self, t):
        """ case """
        self.vel = Vector()

    def bomb(self, t):
        """ case """
        self.timer += t
        if self.timer >= 1:
            self.vel = Vector()
            for point in self.floor.point_list.lista:
                if abs(point - self.knee) < self.bomb_radius:
                    self.floor.point_list.remove(point)

            self.floor.point_list.relleno -= {self.knee.int_vector() + point for point in self.bomb_set}

        # TODO hacer que muera el lemming

    def climb(self, t):
        """ case """
        raise NotImplementedError

    def stairway(self, t):
        """ case """
        self.timer += t
        self.vel = Vector()
        if self.timer >= 500:
            self.timer = 0
            if self.stairPos is None:
                self.stairPos = self.pos
            else:
                self.stairPos += Vector(7, -5)
                self.pos = self.stairPos
            self.complements.append(Step(self.stairPos, self.floor))
            self.stairCount += 1
        if self.stairCount >= 15:
            self.stairCount = 0
            self.stairPos = None
            self.action = "Walk"

    def dig(self, t):
        """ case """
        # dig down
        self.vel = Vector(0, 0.01)

        remove_list = []
        for i, point in enumerate(self.floor.point_list):
            if abs(self.knee - point) < self.width / 2:
                remove_list.append(i)
        remove_list.sort(reverse=True)
        for index in remove_list:
            self.floor.point_list.pop(index)

        are_lines = False
        for line in self.floor.rellenoLines:
            if abs(self.knee - line[0]) < self.width / 2:
                # si la linea se acaba se quita de la lista
                if line[0].y >= line[1].y:
                    self.floor.rellenoLines.remove(line)
                    continue
                line[0] += Vector(0, 1)
                self.floor.point_list.add(line[0])
                are_lines = True
        # self.floor.connect()

        if not are_lines:
            self.action = "Walk"

    def parachute(self, t):
        """ case """
        pass


class Sprite(pygame.sprite.Sprite):
    # FIXME esta clase sobra, pero si la quito da un error que ahora mismo no se arreglar.
    def __init__(self):
        self.image = pygame.Surface([5, 5])
        self.image = pygame.image.load("images/lemmings.png").convert()


class Step(object):
    """ The stair step object that"""
    width = 10
    height = 3

    def __init__(self, pos: Vector, floor: Floor):
        # down left corner
        self.pos = pos
        self.point_list = []
        self.relleno = set()
        pointer = self.pos.int_vector()

        self.point_list.append(pointer)

        pointer += Vector(Step.width, 0)
        self.point_list.append(pointer)

        pointer += Vector(0, -Step.height)
        self.point_list.append(pointer)

        pointer += Vector(-Step.width, 0)
        self.point_list.append(pointer)

        for x in range(int(self.point_list[0].x), int(self.point_list[1].x)):
            for y in range(int(self.point_list[2].y), int(self.point_list[1].y)):
                self.relleno.add(Vector(x, y))

    def draw(self, screen):
        """ Draws it"""
        pygame.draw.lines(screen, (150, 150, 150), True, [point.int() for point in self.point_list], 1)
