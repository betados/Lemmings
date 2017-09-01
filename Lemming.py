import pygame

class LemmingList:

    def __init__(self,quantity):
        self.lista = []
        for i in range(quantity):
            lemming = Lemming(i)
            self.lista.append(lemming)
    def draw(self,t,screen):
        for lemming in self.lista:
            lemming.draw(t, screen)
    def getList(self):
        return self.lista

class Lemming:
    def __init__(self, index):
        # todo hacer que la pos sea el pie delantero
        self.index = index
        self.pos = 20, (index-10)*100
        self.alto = 30
        self.ancho = 8
        self.rect = pygame.Rect(self.pos, (self.ancho, self.alto))
        self.rect.bottomright = self.pos

        self.vel = 0.03, 0
        self.accel = 0, 0
    def draw(self,t, screen):
        # print(self.pos)
        self.vel = self.vel[0] + 0.5 * self.accel[0] * t*t, self.vel[1] + 0.5 * self.accel[1] * t*t
        self.pos = self.pos[0] + self.vel[0]*t,  self.pos[1] + self.vel[1]*t
        self.rect.bottomright = self.pos


        # self.color = 50, 0, 0

        pygame.draw.rect(screen, (0, 100, 0), self.rect, 2)