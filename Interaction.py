# -*- coding: utf-8 -*-

""" Check the interaction between the elements in the game """

import math


class Interaction(object):
    """ static class in charge of checking interaction between different elements"""
    @staticmethod
    def caminaRect(lemmingList, floorList):
        """ look each lemming checking if it is touching a floor"""
        for lemming in lemmingList.lista:
            if lemming.action == "Walk" or \
               lemming.action == "Bomb" or \
               lemming.action == "Fall":
                for floor in floorList:
                    collision, point, nextPoint = \
                        Interaction.collideList(lemming.knee, floor.pointList)
                    # TODO tener en cuenta la inclinacion para caer o no poder avanzar
                    if collision and nextPoint[0] >= \
                            point[0] and Interaction.getDistance(point, nextPoint) < 2:
                        lemming.vel = (nextPoint[0] - point[0]) * 0.03,\
                                      (nextPoint[1] - point[1]) * 0.03
                        if lemming.action == "Fall":
                            lemming.action = "Walk"
                        lemming.floor = floor
                        break
                    else:
                        lemming.action = "Fall"
            if lemming.action == "Dig down":
                pass

    @staticmethod
    def collideList(pos, pointList):
        """ checks if a point is colliding whith a point list"""
        for index, point in enumerate(pointList):
            if index == len(pointList)-1:
                break

            if Interaction.getDistance(pos, point) <= 4:
                return True, point, pointList[index+1]

        return False, None, None

    @staticmethod
    def getDistance(pointP, pointQ):
        """ returns the distance between two bidimensional points"""
        dist = math.sqrt(math.pow(pointQ[0] - pointP[0], 2) + math.pow(pointQ[1] - pointP[1], 2))
        # print(dist)
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

    @staticmethod
    def getUnitVector(point1, point2):
        """returns the unit vector betwen two bidimensional points"""
        catH = point2[0] - point1[0]
        catV = point2[1] - point1[1]
        modulo = math.sqrt(math.pow(catH, 2) + math.pow(catV, 2))
        if modulo == 0:
            return 9999, 9999
        return catH/modulo, catV/modulo

    @staticmethod
    def add(point1, point2):
        """returns the sum of two bidimensional points"""
        return point2[0] + point1[0], point2[1] + point1[1]

    @staticmethod
    def getBoomY(radio, point, x):
        """ returns the Y coordinate for the line in case of explosion """
        # FIXME quizá sea mejor pasar toda la linea en lugar de la x y que se la recorte aquí dentro sin devolver nada
        part = math.sqrt(radio*radio - math.pow(abs(point[0]-x), 2))
        return point[1] + part, point[1] - part

    # TODO comprabación lemming-lemming y sus complementos
