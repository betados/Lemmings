import pygame, random


class LemmingList:

    def __init__(self,quantity, discreteDebugging=False):
        self.lista = []
        self.discreteDebugging = discreteDebugging

        for i in range(quantity):
            lemming = Lemming(i)
            self.lista.append(lemming)

    def draw(self, t, screen):
        for lemming in self.lista:
            lemming.actualize(t)
            lemming.draw(screen, self.discreteDebugging)

    def getList(self):
        return self.lista

class Lemming:
    def __init__(self, index):
        self.index = index
        self.pos = 30, (index-10)*100
        self.alto = 36
        self.ancho = 22
        self.rect = pygame.Rect(self.pos, (self.ancho, self.alto))
        self.rect.bottomright = self.pos
        self.knee = 0, 0
        self.isFalling = True
        self.action = None

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

    def actualize(self,t):
        if self.action == "Stop":
            self.vel = 0, 0
        else:
            self.vel = self.vel[0] + 0.5 * self.accel[0] * t*t, self.vel[1] + 0.5 * self.accel[1] * t*t
        self.pos = self.pos[0] + self.vel[0]*t,  self.pos[1] + self.vel[1]*t
        self.rect.bottomright = self.pos
        self.knee = self.pos[0] - self.ancho/2, self.pos[1] - self.ancho/2 + 3

    def draw(self, screen, discreteDebugging):
        if discreteDebugging:
            pygame.draw.rect(screen, (0, 50, 0), self.rect, 1)
        else:
            self.times += 1
            if self.times > self.period:
                self.image = self.getNextImage()
                self.times = 0
            screen.blit(self.sprite.image, self.rect, self.image)



    def getNextImage(self):
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


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([5, 5])
        self.image = pygame.image.load("images/lemmings.png").convert()
