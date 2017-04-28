import pygame


class Floor:

    def __init__(self,size):
        self.start = (50, size[1] *0.9)
        self.end = (size[0] -50, size[1] *0.9)
        self.color = 0,0,50

    def draw(self, screen):
        line = pygame.draw.line(screen, self.color, self.start, self.end, 2)



    def getInit(self):
        return self.start

    def getEnd(self):
        return self.end



class Scenario:

    def __init__(self, res):
        self.size = res
        self.floor = Floor(res)

    def getFloor(self):
        return self.floor

    def draw(self,screen):
        self.color = 0, 0, 1
        # glColor3fv(color)
        # glBegin(GL_POLYGON)
        # glVertex3f(10, 10, 0)
        # glVertex3f(2, 1, 0)
        # glVertex3f(2,2, 0)
        # glVertex3f(1, 2, 0)
        # glEnd()

        # FRAME
        # glBegin(GL_LINE_LOOP)
        # glVertex3f(0,               0, 0)
        # glVertex3f(self.size[0],    0, 0)
        # glVertex3f(self.size[0],    self.size[1], 0)
        # glVertex3f(0,               self.size[1], 0)
        # glEnd()

        self.floor.draw(screen)
        # pygame.draw.rect(screen,(255,255,255), (100, 100, 10, 10), 3)



        #
        # glBegin(GL_LINE_LOOP)
        # glVertex3f(400, 400, 0)
        # glVertex3f(590, 400, 0)
        # glVertex3f(590, 590, 0)
        # glVertex3f(400, 590, 0)
        # glEnd()
