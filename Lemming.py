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
    def __init__(self,index):
        self.pos = 60, (index-10)*100
        self.alto = 30
        self.ancho = 8

        self.vel = 0.03, 0
        self.accel = 0, 0
    def draw(self,t, screen):
        self.vel = self.vel[0] + 0.5 * self.accel[0] * t*t, self.vel[1] + 0.5 * self.accel[1] * t*t
        self.pos = self.pos[0] + self.vel[0]*t,  self.pos[1] + self.vel[1]*t

        self.color = 50, 0, 0

        pygame.draw.rect(screen, self.color, (self.pos[0],  self.pos[1], self.ancho, self.alto),6)



    def getPos(self):
        return self.pos

    def isFloor(self,isFloor):
        if isFloor:
            self.vel = 0.03, 0
        else:
            self.vel = 0, 0.1