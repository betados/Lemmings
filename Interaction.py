import math

class Interaction:

    def caminaRect(self, lemmingList, floorList):
        for lemming in lemmingList.lista:
            for floor in floorList:
                collision, point, nextPoint = self.collideList(lemming.knee, floor.pointList)
                # TODO tener en cuenta la inclinacion para caer o no poder avanzar
                if collision and nextPoint[0] >= point[0]:
                    lemming.vel = (nextPoint[0] - point[0]) * 0.03, (nextPoint[1] - point[1]) * 0.03
                    lemming.isFalling = False
                    break
                else:
                    lemming.isFalling = True
                    lemming.vel = 0, 0.1
                # print("lemming.vel:",lemming.index, lemming.vel)

    def collideList(self, pos, pointList):
        for index, point in enumerate(pointList):
            if index == len(pointList)-1:
                break

            if self.getDistance(pos, point) <= 4:
                # print("colision")
                return True, point, pointList[index+1]

        return False, None, None


    def getDistance(self, pointP, pointQ):
        dist = math.sqrt(math.pow(pointQ[0] - pointP[0], 2) + math.pow(pointQ[1] - pointP[1], 2))
        return dist

    def isButtonPressed(self, pos, buttonList):
        for button in buttonList:
            if button.coordinates[1][0] > pos[0] > button.coordinates[0][0] and\
                    button.coordinates[0][1] < pos[1] < button.coordinates[3][1]:
                print(button.text)
                return button.text
        return None

    def isLemmingPressed(self, pos, lemmingList, stateDict):
        for lemming in lemmingList:
            if lemming.rect.collidepoint(pos):
                print(lemming.index)
                lemming.action = stateDict["action"]
                return lemming.index
        return None
