import pygame


class Floor:

    def __init__(self, screen, size, pointList):
        print(pointList)
        self.start = (50, size[1] * 0.7)
        self.end = (size[0] - 500, size[1] * 0.1)
        self.color = 0, 255, 0
        self.pointList = []
        self.sprite = Sprite()

        # Rellena si faltan puntos.
        for i, point in enumerate(pointList):
            self.pointList.append(point)
            if i < len(pointList)-1:
                if (pointList[i+1][0] - point[0]) > 1:
                    for x in range(point[0]+1, pointList[i+1][0]):
                        self.pointList.append((x, point[1]))
        print(self.pointList)

        self.screen = screen

    def draw(self):
        # pygame.draw.polygon(self.screen, self.color, self.pointList, 1)
        pygame.draw.lines(self.screen, self.color, False, self.pointList, 2)
        # for point in self.pointList:
        #     if point[0] % 7 == 0:
        #         self.screen.blit(self.sprite.image, (point[0]-20,point[1]-3,1,1), (248,0,30,8))

    def getInit(self):
        return self.start

    def getEnd(self):
        return self.end

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.Surface([5, 5])
        self.image = pygame.image.load("images/grass.png").convert_alpha()



class Scenario:

    def __init__(self, screen, res, font=None):
        self.size = res
        self.floorList = []
        self.screen = screen

        if font is None:
            pointList = []
            a = (self.end[1]-self.start[1])/(self.end[0]-self.start[0])
            for x in range(self.start[0], self.end[0]):
                y = a*(x-self.start[0])+self.start[1]
                pointList.append([x, y])
            self.floorList.append(Floor(screen,res, pointList))
        else:
            import yaml

            load = yaml.load(open(font))
            for i, element in enumerate(load):
                # print(element)
                if i == len(load)-1:
                    break
                if element == "floor" and load[i+1] != "floor" and len(load[i+1])>2:
                    self.floorList.append(Floor(screen, res, load[i+1]))

    def draw(self):
        for floor in self.floorList:
            floor.draw()
