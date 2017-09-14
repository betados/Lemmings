"""
    Module in charge of generating the map
"""
import pygame
import yaml
from Interaction import Interaction


class Floor(object):
    """ A floor object is each of the separated point lists"""
    def __init__(self, screen, size, pointList, discreteDebugging):
        # self.start = (50, size[1] * 0.7)
        # self.end = (size[0] - 500, size[1] * 0.1)
        self.screen = screen
        self.size = size
        self.relleno = []
        self.rellenoLines = []
        self.pointListAdded = []
        if discreteDebugging:
            self.color = 0, 0, 150
        else:
            self.color = 0, 0, 255
        self.pointList = []
        self.sprite = Sprite()

        # Rellena si faltan puntos entremedias
        # FIXME rellena en horizontal cuando deberia rellenar con una linea desde un punto hasta otro
        for i, point in enumerate(pointList):
            self.pointList.append(point)
            if i < len(pointList)-1:
                # while Interaction.getDistance(self.pointList[len(self.pointList)-1],
                #                               pointList[i+1]) > 2:
                #     unitVector = Interaction.getUnitVector(self.pointList[len(self.pointList)-1], pointList[i+i])
                #     next = Interaction.add(self.pointList[len(self.pointList)-1], unitVector)
                #     print(next, unitVector)
                #     self.pointList.append((int(next[0]), int(next[1])))
                #     self.draw()
                if (pointList[i+1][0] - point[0]) > 1:
                    for x in range(point[0]+1, pointList[i+1][0]):
                        self.pointList.append((x, point[1]))
                if (point[0] - pointList[i+1][0]) > 1:
                    for x in range(pointList[i+1][0], point[0]+1):
                        self.pointList.append((x, point[1]))


        if Interaction.getDistance(self.pointList[len(self.pointList)-1], self.pointList[0]) < 50:
            print("cierra el circulo")
            self.complete(self.pointList[0], self.pointList[len(self.pointList)-1], self.pointList, 0)
        else:
            # Completa verticalmente desde el final hasta el suelo
            # s = size[0], size[1]-50
            self.complete(self.pointList[len(self.pointList)-1], size, self.pointList, axis=1)
            # Completa horizontalmente desde el final hasta el inicio por el suelo
            self.complete(self.pointList[len(self.pointList)-1], self.pointList[0], self.pointList, axis=0)
            # Completa verticalmente desde el final hasta el inicio
            self.complete(self.pointList[len(self.pointList) - 1], self.pointList[0], self.pointList, axis=1)


        # RELLENO
        if True:
            # Cuadrado donde buscar para rellenar
            # pointRange = [[minX, maxX], [minY, maxY]]
            pointRange = [[9999, 0], [9999, 0]]
            for point in self.pointList:
                for i in range(2):
                    if point[i] < pointRange[i][0]:
                        pointRange[i][0] = point[i]
                    if point[i] > pointRange[i][1]:
                        pointRange[i][1] = point[i]
            # print("range: ", pointRange)

            for x in range(pointRange[0][0]-10, pointRange[0][1]+10):
                trigered = False
                yAnt = 0
                init = None
                end = None
                for y in range(pointRange[1][0]-10, pointRange[1][1]+10):
                    if (x, y) in self.pointList:
                        if trigered and y-yAnt > 5:
                            yAnt = y
                            trigered = False
                            end = [x, y]
                        if not trigered and y - yAnt > 5:
                            yAnt = y
                            trigered = True
                            init = [x, y]
                            continue
                        # if trigered:
                        #     yAnt= y
                        #     trigered = False
                        # if not trigered:
                        #     yAnt = y
                        #     trigered = True
                    if trigered:
                        # self.relleno.append((x, y))
                        pass
                if init is not None and end is not None:
                    self.rellenoLines.append([init, end])

        # for y in range(self.size[1]):
        #     for x in range(self.size[0]):
        #         if (x, y) in self.pointList:
        #             pass
                    # print ("relleno: " , x,y)

    @staticmethod
    def complete(point1, point2, pointList, axis=0):
        if point2[axis] < point1[axis]:
            interval = -1
        else:
            interval = 1
        for i in range(point1[axis], point2[axis], interval):
            if axis == 0:
                pointList.append((i, point1[1]))
            if axis == 1:
                pointList.append((point1[0], i))

    def draw(self):
        """ draw the floor """
        #
        for point in self.pointList:
            pygame.draw.circle(self.screen, self.color, point, 2, 2)
        for point in self.pointListAdded:
            pygame.draw.circle(self.screen, (100, 0, 0), point, 4, 4)
        for point in self.relleno:
            pygame.draw.circle(self.screen, (100, 100, 10), point, 1, 1)
        for line in self.rellenoLines:
            pygame.draw.lines(self.screen, (100, 100, 10), False, (line[0], line[1]), 1)

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

