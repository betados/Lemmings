import math

class Interaction:

    def caminaRect(self, lemmingList, floor):
        for lemming in lemmingList.lista:
            collision, point, nextPoint = self.collideList(lemming.pos, floor.pointList)
            if collision:
                lemming.vel = (nextPoint[0] - point[0]) * 0.03, (nextPoint[1] - point[1]) * 0.03
            else:
                lemming.vel = 0, 0.1


    def collideList(self, pos, pointList):
        for index, point in enumerate(pointList):
            if index == len(pointList)-1:
                break
            if self.getDistance(pos, point) < 2:
                return True, point, pointList[index+1]
        return False, None, None


    def getDistance(self, pointP, pointQ):
        dist = math.sqrt(math.pow(pointQ[0] - pointP[0], 2) + math.pow(pointQ[1] - pointP[1], 2))
        return dist

