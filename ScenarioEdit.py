
import math, random
import pygame, eztext



class Floor:

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
            poly1 = pygame.draw.polygon(screen, (255,255,255), self.pointList, 0)  # filled


    def getPoints(self):
        return self.pointList

    def getDistance(self,pointP, pointQ):
        dist = math.sqrt(math.pow(pointQ[0] - pointP[0], 2) + math.pow(pointQ[1] - pointP[1], 2))
        return dist

    def add(self, point):
        # print(point)
        # if self.distance(point, self.lastPoint) > 5:
        self.pointList.append(point)
        # self.lastPoint = point



class Scenario:

    floorList = []

    def __init__(self, res):
        self.res = res
        self.index = -1
        # self.floor = Floor(res)

    def newFloor(self):
        # self.floor = Floor()
        self.floorList.append(Floor())
        self.index += 1

    def getFloor(self):
        pass
        # return self.floor

    def add(self, point):
        self.floorList[self.index].add(point)

    def save(self,name):
        import xml.etree.cElementTree as ET

        root = ET.Element("root")

        for i,floors in enumerate(self.floorList):
            floor = ET.SubElement(root, "Floor")
            for j,point in enumerate(floors.getPoints()):
                ET.SubElement(floor, "Point", number=str(j)).text = str(point)

        tree = ET.ElementTree(root)
        tree.write(str(name)+".xml")



    def draw(self,screen):
        color = 0, 0, 1

        # FLOORS
        for floor in self.floorList:
            floor.draw(screen)


