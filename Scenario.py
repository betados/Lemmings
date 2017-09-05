"""
    Module in charge of generating the map
"""
import pygame
import yaml


class Floor(object):
    """ A floor object is each of the separated point lists"""
    def __init__(self, screen, size, pointList, discreteDebugging):
        self.start = (50, size[1] * 0.7)
        self.end = (size[0] - 500, size[1] * 0.1)
        if discreteDebugging:
            self.color = 0, 0, 50
        else:
            self.color = 0, 0, 255
        self.pointList = []
        self.sprite = Sprite()

        # Rellena si faltan puntos.
        for i, point in enumerate(pointList):
            self.pointList.append(point)
            if i < len(pointList)-1:
                if (pointList[i+1][0] - point[0]) > 1:
                    for x in range(point[0]+1, pointList[i+1][0]):
                        self.pointList.append((x, point[1]))

        self.screen = screen

    def draw(self):
        """ draw the floor """
        pygame.draw.lines(self.screen, self.color, False, self.pointList, 1)
        # for point in self.pointList:
        #     if point[0] % 7 == 0:
        #         self.screen.blit(self.sprite.image, (point[0]-20,point[1]-3,1,1), (248,0,30,8))

    # def  getInit(self):
    #     return self.start
    #
    # def getEnd(self):
    #     return self.end


class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([5, 5])
        self.image = pygame.image.load("images/grass.png").convert_alpha()


class Scenario(object):
    """ It contains and handles the list of floors"""
    def __init__(self, screen, res, font=None, discreteDebugging=False):
        self.size = res
        self.floorList = []
        self.screen = screen

        load = yaml.load(open(font))
        for i, element in enumerate(load):
            # print(element)
            if i == len(load)-1:
                break
            if element == "floor" and load[i+1] != "floor" and len(load[i+1]) > 2:
                self.floorList.append(Floor(screen, res, load[i+1], discreteDebugging))

    def draw(self):
        """ draws each floor """
        for floor in self.floorList:
            floor.draw()
