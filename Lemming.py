"""
The lemming sprite module.

"""

import random
import pygame

from Interaction import Interaction
from vector_2d import Vector


class LemmingList(object):
    """ This class contains and handles the list of lemmings"""

    def __init__(self, quantity, screen, discreteDebugging=False):
        self.lista = []
        self.discreteDebugging = discreteDebugging

        for i in range(quantity):
            lemming = Lemming(i, screen)
            self.lista.append(lemming)

    def draw(self, t, screen):
        """ Atualize position and draw each lemming"""
        for lemming in self.lista:
            lemming.actualize(t)
            lemming.draw(screen, self.discreteDebugging)

    def __getitem__(self, item):
        """ get the lemming """
        return self.lista[item]

    def __iter__(self):
        return iter(self.lista)


class Lemming(object):
    """ This class is the implementation of the lemmings sprites"""

    def __init__(self, index, screen):
        self.screen = screen
        self.index = index
        self.pos = Vector(30, (index - 10) * 100)
        self.alto = 36
        self.ancho = 22
        self.rect = pygame.Rect(self.pos(), (self.ancho, self.alto))
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
        self.image = self.getNextImage()
        self.times = 0
        self.period = 10
        self.timer = 0

        self.complements = []

        self.characterDict = {"Walk": self.walk, "Stop": self.stop,
                              "Climb": self.climb, "Stairway": self.stairway,
                              "Bomb": self.bomb, "Dig down": self.dig,
                              "Dig horiz.": self.dig, "Dig diag.": self.dig,
                              "Parachute": self.parachute, "Fall": self.fall}

    def actualize(self, t):
        """ Actualize the position and speed of the lemming """

        if self.action:
            self.characterDict[self.action](t)

        self.pos = self.pos + self.vel * t
        self.rect.bottomright = self.pos()
        self.knee = self.pos - Vector(self.ancho / 2, self.ancho / 2 + 3)

    def draw(self, screen, discreteDebugging):
        """Draw the lemming"""
        if discreteDebugging:
            pygame.draw.rect(screen, (0, 50, 0), self.rect, 1)
        else:
            self.times += 1
            if self.times > self.period:
                self.image = self.getNextImage()
                self.times = 0
            screen.blit(self.sprite.image, self.rect, self.image)

        for complement in self.complements:
            complement.draw()

    def getNextImage(self):
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

    def isWalking(self):
        """Is the lemming walking?"""
        return self.action == "Walk"

    # ACTIONS for switch-case statement
    def walk(self, t):
        """ case """
        pass
        # self.vel = self.vel[0] + 0.5 * self.accel[0] * t * t,\
        #     self.vel[1] + 0.5 * self.accel[1] * t * t

    def fall(self, t):
        """ case """
        self.vel = Vector(0, 0.1)

    def stop(self, t):
        """ case """
        self.vel = Vector()

    def bomb(self, t):
        """ case """
        radio = self.ancho * 1.3
        self.timer += t
        if self.timer >= 1:
            self.vel = Vector()
            # FIXME si no se repite no se borran bien
            for _ in range(10):
                for point in self.floor.pointList:
                    if abs(point[0] - self.knee[0]) < radio:
                        self.floor.pointList.remove(point)
                for line in self.floor.rellenoLines:
                    if abs(line[0][0] - self.knee[0]) < radio:
                        y1, y2 = Interaction.getBoomY(radio, self.knee, line[0][0])
                        y1 = int(y1)
                        y2 = int(y2)
                        # 1
                        if line[1][1] >= y2 >= line[0][1] and line[1][1] >= y1 >= line[0][1]:
                            print(1)
                            newLine2 = [line[0], [line[0][0], y2]]
                            newLine1 = [[line[0][0], y1], line[1]]
                            self.floor.rellenoLines.remove(line)
                            self.floor.rellenoLines.append(newLine2)
                            self.floor.rellenoLines.append(newLine1)
                            self.floor.pointList.append(newLine2[1])
                            self.floor.pointList.append(newLine1[0])
                            continue
                        # 2
                        if y2 < line[0].y and line[1].y >= y1 >= line[0].y:
                            print(2)
                            line[0] = [line[0][0], int(y1)]
                            self.floor.pointList.append(line[0])
                            continue
                        # 3
                        if line[1][1] >= y2 >= line[0][1] and line[1][1] > y1:
                            print(3)
                            line[1] = [line[0][0], int(y2)]
                            self.floor.pointList.append(line[1])
                            continue
                        # 4
                        if y2 < line[0][1] and y1 > line[1][1]:
                            print(4)
                            self.floor.rellenoLines.remove(line)
                            continue

                        # if y1 > line[1][1]:
                        #     # y1 = line[1][1]
                        #     self.floor.rellenoLines.remove(line)
                        #     continue
                        # if y1 < line[0][1]:
                        #     y1 = line[0][1]
                        # line[0] = [line[0][0], int(y1)]
                        # self.floor.pointList.append(line[0])

            self.action = "Walk"

    def climb(self, t):
        """ case """
        raise NotImplementedError

    def stairway(self, t):
        """ case """
        self.timer += t
        self.vel = Vector()
        if self.timer >= 500:
            self.timer = 0
            if not self.stairPos:
                self.stairPos = self.pos
            else:
                self.stairPos += Vector(7, -5)
                self.pos = self.stairPos
            self.complements.append(Step(self.stairPos, self.screen))
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
        for i, point in enumerate(self.floor.pointList):
            if abs(self.knee - point) < self.ancho / 2:
                remove_list.append(i)
        remove_list.sort(reverse=True)
        for index in remove_list:
            self.floor.pointList.pop(index)

        areLines = False
        for line in self.floor.rellenoLines:
            if abs(self.knee - line[0]) < self.ancho / 2:
                # si la linea se acaba se quita de la lista
                if line[0].y >= line[1].y:
                    self.floor.rellenoLines.remove(line)
                    continue
                line[0] += Vector(0, 1)
                self.floor.pointList.append(line[0])
                areLines = True
        # self.floor.connect()

        if not areLines:
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

    def __init__(self, pos, screen):
        # down left corner
        self.pos = pos
        self.screen = screen
        self.pointList = []
        pointer = self.pos
        for _ in range(Step.width):
            pointer += Vector(1, 0)
            self.pointList.append(pointer)
        for _ in range(Step.height):
            pointer += Vector(0, -1)
            self.pointList.append(pointer)
        for _ in range(Step.width):
            pointer += Vector(-1, 0)
            self.pointList.append(pointer)
        for _ in range(Step.height):
            pointer += Vector(0, 1)
            self.pointList.append(pointer)

    def get_points(self):
        for point in self.pointList:
            yield point()

    def draw(self):
        """ Draws it"""
        pygame.draw.lines(self.screen, (150, 150, 150), False, list(self.get_points()), 1)
