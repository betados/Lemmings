from OpenGL.GL import *
from OpenGL.GLU import *

class Lemming:
    def __init__(self):
        self.pos = 0, 0
        self.alto = 30
        self.ancho = 8

        self.vel = 0.03, 0
    def draw(self,t):
        self.pos = self.pos[0] + self.vel[0]*t,  self.pos[1] + self.vel[1]*t
        self.color = 0.1, 0, 0
        glColor3fv(self.color)
        glBegin(GL_POLYGON)
        glVertex2f(self.pos[0],self.pos[1])
        glVertex2f(self.pos[0]+self.ancho,self.pos[1])
        glVertex2f(self.pos[0]+self.ancho,self.pos[1]+self.alto)
        glVertex2f(self.pos[0],self.pos[1]+self.alto)
        glEnd()