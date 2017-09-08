
import math
import random
import pygame


class Floor(object):

    def __init__(self):
        self.pointList = []
        self.lastPoint = -9999, -9999
        # self.color = random.randrange(256) / 255, random.randrange(256) / 255, random.randrange(256) / 255
        self.color = random.randrange(256) / 600, random.randrange(256) / 600, random.randrange(256) / 600
        # print (self.color)

    def draw(self, screen):

        # print("dibuja")
        # rect2 = pygame.draw.rect(screen,(255,255,255), (100, 20, 60, 60), 3)  # not filled
        if len(self.pointList) > 2:
            pygame.draw.lines(screen, (100, 100, 100), False, self.pointList, 1)  # filled

    def getPoints(self):
        return self.pointList

    def getDistance(self,pointP, pointQ):
        dist = math.sqrt(math.pow(pointQ[0] - pointP[0], 2) + math.pow(pointQ[1] - pointP[1], 2))
        return dist

    def add(self, point):
        self.pointList.append(point)


class Scenario(object):

    def __init__(self, res):
        self.res = res
        self.index = -1
        self.floorList = []
        # self.floor = Floor(res)

    def newFloor(self):
        # self.floor = Floor()
        self.floorList.append(Floor())
        self.index += 1

    def add(self, point):
        self.floorList[self.index].add(point)

    def save(self, name):
        import yaml

        floorList_pointList = []
        for floor in self.floorList:
            floorList_pointList.append("floor")
            floorList_pointList.append(floor.pointList)

        yaml.dump(floorList_pointList, open("maps/"+name + '.yaml', 'w'))
        # print(floorList_pointList)

    def draw(self,screen):
        # color = 0, 0, 1

        # FLOORS
        for floor in self.floorList:
            floor.draw(screen)


