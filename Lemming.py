import pygame, random

class LemmingList:

    def __init__(self,quantity):
        self.lista = []
        for i in range(quantity):
            lemming = Lemming(i)
            self.lista.append(lemming)

    def draw(self, t, screen):
        for lemming in self.lista:
            lemming.draw(t, screen)

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

        self.vel = 0, 0.1
        self.accel = 0, 0
        self.sprite = Sprite()
        self.totalImages = 7
        self.imagePointer = random.randrange(7)
        self.image = self.getNextImage()
        self.times = 0
        self.period = 7


    def draw(self,t, screen):
        # print(self.pos)
        self.vel = self.vel[0] + 0.5 * self.accel[0] * t*t, self.vel[1] + 0.5 * self.accel[1] * t*t
        self.pos = self.pos[0] + self.vel[0]*t,  self.pos[1] + self.vel[1]*t
        self.rect.bottomright = self.pos
        self.knee = self.pos[0] - self.ancho/2, self.pos[1] - self.ancho/2 + 3

        self.times += 1
        if self.times > self.period:
            self.image = self.getNextImage()
            self.times = 0
        screen.blit(self.sprite.image, self.rect, self.image)

        # pygame.draw.rect(screen, (0, 100, 0), self.rect, 2)

    def getNextImage(self):
        side = 46
        self.imagePointer += 1
        if self.imagePointer >= self.totalImages:
            self.imagePointer = 0
        return 50*self.imagePointer+8, side*2, side, side-10


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([5, 5])
        self.image = pygame.image.load("images/lemmings.png").convert()
