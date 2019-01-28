# -*- coding: utf-8 -*-

""" Check the interaction between the elements in the game """

import math


class Interaction(object):
    """ static class in charge of checking interaction between different elements"""

    @staticmethod
    def caminaRect(lemmingList, floor_list):
        """ look each lemming checking if it is touching a floor"""
        for lemming in lemmingList:
            if lemming.action in ("Walk", "Bomb", "Fall"):
                for floor in floor_list:
                    collision, point, next_point = Interaction.collide_list(lemming.knee, floor.pointList)
                    # TODO tener en cuenta la inclinacion para caer o no poder avanzar
                    if collision and next_point.x >= point.x and abs(point - next_point) < 2:
                        lemming.vel = (next_point - point) * 0.03
                        if lemming.action == "Fall":
                            lemming.action = "Walk"
                        lemming.floor = floor
                        break
                    else:
                        lemming.action = "Fall"
            if lemming.action == "Dig down":
                pass

    @staticmethod
    def collide_list(pos, pointList):
        """ checks if a point is colliding whith a point list"""
        for i, point in enumerate(pointList):
            if abs(pos - point) <= 4:
                return True, point, pointList[i + 1]

        return False, None, None

    @staticmethod
    def isButtonPressed(pos, buttonList):
        """ check if and witch button of the gui is clicked """
        for button in buttonList:
            if button.coordinates[1][0] > pos[0] > button.coordinates[0][0] and \
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
        return catH / modulo, catV / modulo

    @staticmethod
    def add(point1, point2):
        """returns the sum of two bidimensional points"""
        return point2[0] + point1[0], point2[1] + point1[1]

    @staticmethod
    def getBoomY(radio, point, x):
        """ returns the Y coordinate for the line in case of explosion """
        # FIXME quizá sea mejor pasar toda la linea en lugar de la x y que se la recorte aquí dentro sin devolver nada
        part = math.sqrt(radio * radio - math.pow(abs(point[0] - x), 2))
        return point[1] + part, point[1] - part

    # TODO comprabación lemming-lemming y sus complementos
