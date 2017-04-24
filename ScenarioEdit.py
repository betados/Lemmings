from OpenGL.GL import *
from OpenGL.GLU import *
import math, random


class Floor:

    pointList = []

    def __init__(self):
        self.lastPoint = -9999, -9999
        self.color = random.randrange(256) / 255, random.randrange(256) / 255, random.randrange(256) / 255
        print (self.color)

    def draw(self):
        glColor3fv(self.color)
        glBegin(GL_LINE_LOOP)
        for element in self.pointList:
            glVertex3f(element[0], 700-element[1]*1.37, 0)
            #FIXME hay que tunear la Y del ratón por que la imagen está achatada con la X no pasa.
        glEnd()
        glFlush()


    def getPoints(self):
        return self.pointList

    def distance(self,pointP, pointQ):
        distance = math.sqrt(math.pow(pointQ[0] - pointP[0], 2) + math.pow(pointQ[1] - pointP[1], 2))
        return distance

    def add(self, point):
        # print(point)
        # if self.distance(point, self.lastPoint) > 5:
        self.pointList.append(point)
        # self.lastPoint = point



class Scenario:

    floorList = []


    def __init__(self, res):
        self.size = res
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

    def save(self):
        print("s")
        import xml.etree.cElementTree as ET

        root = ET.Element("floor")
        for i, floor in enumerate(self.floorList):
            ET.Element(root, floor, number=str(i)).text = str(floor)
            points = ET.SubElement(root, "points")
            for j, point in enumerate(floor.getPoints()):
                ET.SubElement(points, "point", number=str(j)).text = str(point)
        tree = ET.ElementTree(root)
        tree.write("output.xml")



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

        for floor in self.floorList:
            print(floor)
            floor.draw()
        print("___________")



        #
        # glBegin(GL_LINE_LOOP)
        # glVertex3f(400, 400, 0)
        # glVertex3f(590, 400, 0)
        # glVertex3f(590, 590, 0)
        # glVertex3f(400, 590, 0)
        # glEnd()
