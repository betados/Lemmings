from OpenGL.GL import *
from OpenGL.GLU import *


class Floor:

    def __init__(self,size):
        self.init = (50, 50)
        self.end = (size[0] - 300, 50)

    def draw(self):
        glBegin(GL_LINE_LOOP)
        glVertex3f(self.init[0], self.init[1], 0)
        glVertex3f(self.end[0], self.end[1], 0)
        glEnd()

    def getInit(self):
        return self.init

    def getEnd(self):
        return self.end



class Scenario:

    def __init__(self, res):
        self.size = res
        self.floor = Floor(res)

    def getFloor(self):
        return self.floor

    def draw(self):
        color = 0, 0, 1
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
