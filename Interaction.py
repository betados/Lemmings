import math

class Interaction:

    # @deprecated
    def check(self, lemmingList, floor):
        for lemming in lemmingList.getList():
            if lemming.getPos()[0] > floor.getInit()[0] and lemming.getPos()[0] < floor.getEnd()[0] and \
               lemming.getPos()[1] > floor.getInit()[1]*0.95 and lemming.getPos()[1] < floor.getInit()[1]*1.05:
                    lemming.isFloor(True)
            else:
                lemming.isFloor(False)


    def camina(self, lemmingList, floor):

        for lemming in lemmingList.lista:
            distanceMin = 9999
            nearestPoint = None
            for point in floor.pointList:
                distance = self.getDistance(lemming.getPos(), point)
                if distance < distanceMin:
                    distanceMin=distance
                    nearestPoint = point

            # nex point to the nearest:
            if nearestPoint is not None:
                index = floor.pointList.index(nearestPoint)
                if index < len(floor.pointList)-1:
                    nextPoint = floor.pointList[index+1]
                else:
                    nextPoint = [nearestPoint[0]+1, nearestPoint[1]]

                # is near enought and above
                if distanceMin <= lemming.alto and abs(lemming.pos[0]) - abs(nearestPoint[0]) < 2:
                    lemming.vel = (nextPoint[0]-nearestPoint[0])*0.03, (nextPoint[1]-nearestPoint[1])*0.03
                    # print(lemming.vel)
                    # lemming.vel = 0.03, 0
                else:
                    lemming.vel = 0, 0.1

    def caminaRect(self, lemmingList, floor):
        for lemming in lemmingList.lista:
            for i, point in enumerate(floor.pointList):
                if lemming.rect.collidepoint(point):
                    nextPoint = floor.pointList[i + 1]
                    lemming.vel = (nextPoint[0] - point[0]) * 0.03, (nextPoint[1] - point[1]) * 0.03
                    break
                else:
                    lemming.vel = 0, 0.1
            print(lemming.vel)





    def getDistance(self, pointP, pointQ):
        dist = math.sqrt(math.pow(pointQ[0] - pointP[0], 2) + math.pow(pointQ[1] - pointP[1], 2))
        return dist

