from OpenGL.GL import *
from OpenGL.GLU import *
import math


class Floor:

    lista = []

    def __init__(self,size):
        pass

    def draw(self):
        glBegin(GL_LINE_LOOP)
        for element in self.lista:
            glVertex3f(element[0], 700-element[1]*1.37, 0)
        glEnd()

    def add(self, point):
        self.lista.append(point)



class Scenario:
    lastPoint = -9999, -9999

    def __init__(self, res):
        self.size = res
        self.floor = Floor(res)

    def getFloor(self):
        return self.floor

    def add(self, point):
        if self.lastPoint != (-9999, -9999):
            if self.distance(point, self.lastPoint) > 5:
                self.floor.add(point)

        self.lastPoint = point

    def distance(self,pointP, pointQ):
        distance = math.sqrt(math.pow(pointQ[0] - pointP[0], 2) + math.pow(pointQ[1] - pointP[1], 2))
        return distance

    def draw(self):
        color = 0, 0, 0.2
        glColor3fv(color)
        # glBegin(GL_POLYGON)
        # glVertex3f(10, 10, 0)
        # glVertex3f(2, 1, 0)
        # glVertex3f(2,2, 0)
        # glVertex3f(1, 2, 0)
        # glEnd()

        # FRAME
        glBegin(GL_LINE_LOOP)
        glVertex3f(0,               0, 0)
        glVertex3f(self.size[0],    0, 0)
        glVertex3f(self.size[0],    self.size[1], 0)
        glVertex3f(0,               self.size[1], 0)
        glEnd()

        self.floor.draw()



        #
        # glBegin(GL_LINE_LOOP)
        # glVertex3f(400, 400, 0)
        # glVertex3f(590, 400, 0)
        # glVertex3f(590, 590, 0)
        # glVertex3f(400, 590, 0)
        # glEnd()
