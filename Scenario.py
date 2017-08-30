import pygame


class Floor:

    def __init__(self, size, font=None):
        self.start = (50, size[1] * 0.7)
        self.end = (size[0] - 500, size[1] * 0.1)
        self.color = 0, 0, 255

        if font is None:
            self.pointList = []
            a = (self.end[1]-self.start[1])/(self.end[0]-self.start[0])
            for x in range (self.start[0], self.end[0]):
                y = a*(x-self.start[0])+self.start[1]
                self.pointList.append([x, y])
        else:
            import yaml
            self.pointList = yaml.load(open(font))
            print(self.pointList)


    def draw(self, screen):
        # line = pygame.draw.line(screen, self.color, self.start, self.end, 1)

        pygame.draw.polygon(screen, self.color, self.pointList, 1)


    def getInit(self):
        return self.start

    def getEnd(self):
        return self.end



class Scenario:

    def __init__(self, res, font = None):
        self.size = res
        self.floor = Floor(res, font)

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
