import math


class Interaction(object):
    """ static class in charge of checking interaction between different elements"""
    @staticmethod
    def caminaRect(lemmingList, floorList):
        """ look each lemming checking if it is touching a floor"""
        for lemming in lemmingList.lista:
            if lemming.action == "Walk":
                for floor in floorList:
                    collision, point, nextPoint = Interaction.collideList(lemming.knee, floor.pointList)
                    # TODO tener en cuenta la inclinacion para caer o no poder avanzar
                    if collision and nextPoint[0] >= point[0]:
                        lemming.vel = (nextPoint[0] - point[0]) * 0.03, (nextPoint[1] - point[1]) * 0.03
                        lemming.isFalling = False
                        break
                    else:
                        lemming.isFalling = True
                        lemming.vel = 0, 0.1

    @staticmethod
    def collideList(pos, pointList):
        """ checks if a point is colliding whith a point list"""
        for index, point in enumerate(pointList):
            if index == len(pointList)-1:
                break

            if Interaction.getDistance(pos, point) <= 4:
                # print("colision")
                return True, point, pointList[index+1]

        return False, None, None

    @staticmethod
    def getDistance(pointP, pointQ):
        """ returns the distance between two bidimensional points"""
        dist = math.sqrt(math.pow(pointQ[0] - pointP[0], 2) + math.pow(pointQ[1] - pointP[1], 2))
        return dist

    @staticmethod
    def isButtonPressed(pos, buttonList):
        """ check if and witch button of the gui is clicked """
        for button in buttonList:
            if button.coordinates[1][0] > pos[0] > button.coordinates[0][0] and\
                    button.coordinates[0][1] < pos[1] < button.coordinates[3][1]:
                print(button.text)
                return button.text
        return None

    @staticmethod
    def isLemmingPressed(pos, lemmingList, stateDict):
        """ check if and witch lemming is clicked  """
        for lemming in lemmingList:
            if lemming.rect.collidepoint(pos):
                print(lemming.index)
                lemming.action = stateDict["action"]
                return lemming.index
        return None
