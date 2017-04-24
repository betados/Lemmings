from OpenGL.GL import *
from OpenGL.GLU import *

class LemmingList:
    lista = []
    def __init__(self,quantity):
        for i in range(quantity):
            lemming = Lemming(i)
            self.lista.append(lemming)
    def draw(self,t):
        for lemming in self.lista:
            lemming.draw(t)
    def getList(self):
        return self.lista

class Lemming:
    def __init__(self,index):
        self.pos = 60, 400+index*100
        self.alto = 30
        self.ancho = 8

        self.vel = 0.03, 0
        self.accel = 0, 0
    def draw(self,t):
        self.vel = self.vel[0] + 0.5 * self.accel[0] * t*t, self.vel[1] + 0.5 * self.accel[1] * t*t
        self.pos = self.pos[0] + self.vel[0]*t,  self.pos[1] + self.vel[1]*t
        self.color = 1, 0, 0
        glColor3fv(self.color)
        glBegin(GL_POLYGON)
        glVertex2f(self.pos[0], self.pos[1])
        glVertex2f(self.pos[0]+self.ancho, self.pos[1])
        glVertex2f(self.pos[0]+self.ancho, self.pos[1]+self.alto)
        glVertex2f(self.pos[0], self.pos[1]+self.alto)
        glEnd()

    def getPos(self):
        return self.pos

    def isFloor(self,isFloor):
        if isFloor:
            self.vel = 0.03, 0
        else:
            self.vel = 0, -0.1