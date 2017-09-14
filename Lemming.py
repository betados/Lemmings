"""
The lemming sprite module.

"""

import random
import pygame

from Interaction import Interaction


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

    def get(self, index):
        """ get the lemming """
        return self.lista[index]


class Lemming(object):
    """ This class is the implementation of the lemmings sprites"""
    def __init__(self, index, screen):
        self.screen = screen
        self.index = index
        self.pos = 30, (index-10)*100
        self.alto = 36
        self.ancho = 22
        self.rect = pygame.Rect(self.pos, (self.ancho, self.alto))
        self.rect.bottomright = self.pos
        self.knee = 0, 0
        self.isFalling = True
        self.action = "Walk"
        self.stairCount = 0
        self.stairPos = None
        self.floor = None

        self.vel = 0, 0.1
        self.accel = 0, 0
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
                              "CLimb": self.climb, "Stairway": self.stairway,
                              "Bomb": self.bomb, "Dig down": self.dig,
                              "Dig horiz.": self.dig, "Dig diag.": self.dig,
                              "Parachute": self.parachute}

    def actualize(self, t):
        """Actualize the position and speed of the lemming"""
        if self.action is not None:
            self.characterDict[self.action](t)

        # print(self.index, self.action, self.vel)

        self.pos = self.pos[0] + self.vel[0]*t, self.pos[1] + self.vel[1]*t
        self.rect.bottomright = self.pos
        self.knee = self.pos[0] - self.ancho/2, self.pos[1] - self.ancho/2 + 3

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
        if self.isFalling:
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
        return bool(self.action == "Walk")

    # ACTIONS for switch-case statement
    def walk(self, t):
        """ case """
        self.vel = self.vel[0] + 0.5 * self.accel[0] * t * t,\
            self.vel[1] + 0.5 * self.accel[1] * t * t

    def stop(self, t):
        """ case """
        self.vel = 0, 0

    def bomb(self, t):
        """ case """
        radio = self.ancho * 1.3
        self.vel = 0, 0
        self.timer += t
        if self.timer >= 3:
            for line in self.floor.rellenoLines:
                if abs(line[0][0] - self.knee[0]) < radio:
                    # self.floor.rellenoLines.remove(line)
                    y1, y2 = Interaction.getBoomY(radio, self.knee, line[0][0])
                    line[0] = line[0][0], y1
            for point in self.floor.pointList:
                if abs(point[0] - self.knee[0]) < radio:
                    self.floor.pointList.remove(point)
            # self.action = "Walk"





    def climb(self, t):
        """ case """
        pass

    def stairway(self, t):
        """ case """
        self.vel = 0, 0
        if self.stairCount % 1 == 0:
            if self.stairPos is None:
                self.stairPos = self.pos
            else:
                self.stairPos = self.stairPos[0] + 7, self.stairPos[1] - 5
                self.pos = self.stairPos
            self.complements.append(Step(self.stairPos, self.screen))
        self.stairCount += 0.125
        if self.stairCount >= 15:
            self.stairCount = 0
            self.stairPos = None

    def dig(self, t):
        """ case """
        # dig down
        self.vel = 0, 0.01

        for point in self.floor.pointList:
            if Interaction.getDistance(self.knee, point) < self.ancho / 2:
                self.floor.pointList.remove(point)

        areLines = False
        for line in self.floor.rellenoLines:
            if Interaction.getDistance(self.knee, line[0]) < self.ancho / 2:
                # si la linea se acaba se quita de la lista
                if line[0][1] >= line[1][1]:
                    self.floor.rellenoLines.remove(line)
                    continue
                line[0][1] += 1
                self.floor.pointList.append(line[0])
                areLines = True

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
            pointer = pointer[0]+1, pointer[1]
            self.pointList.append(pointer)
        for _ in range(Step.height):
            pointer = pointer[0], pointer[1]-1
            self.pointList.append(pointer)
        for _ in range(Step.width):
            pointer = pointer[0]-1, pointer[1]
            self.pointList.append(pointer)
        for _ in range(Step.height):
            pointer = pointer[0], pointer[1]+1
            self.pointList.append(pointer)

    def draw(self):
        """ Draws it"""
        pygame.draw.lines(self.screen, (150, 150, 150), False, self.pointList, 1)

