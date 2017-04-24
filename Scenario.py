from OpenGL.GL import *
from OpenGL.GLU import *

class Scenario:
    def __init__(self, res):
        self.size = res


    def draw(self):


        self.color = 0, 0, 0.2
        glColor3fv(self.color)
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

        # GROUND

        glBegin(GL_LINE_LOOP)
        glVertex3f(50, 50, 0)
        glVertex3f(self.size[0]-50,50, 0)
        glEnd()


        #
        # glBegin(GL_LINE_LOOP)
        # glVertex3f(400, 400, 0)
        # glVertex3f(590, 400, 0)
        # glVertex3f(590, 590, 0)
        # glVertex3f(400, 590, 0)
        # glEnd()
