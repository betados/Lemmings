# -*- coding: utf-8 -*-

""" Check the interaction between the elements in the game """
from vector_2d import Vector

import math


class Interaction(object):
    """ static class in charge of checking interaction between different elements"""

    @staticmethod
    def caminaRect(lemmingList, floor_list):
        """ look each lemming checking if it is touching a floor"""
        for lemming in lemmingList:
            if lemming.action in ("Walk", "Bomb", "Fall"):
                for floor in floor_list:
                    collision, vel = Interaction.collide_list(lemming.knee.int_vector(), floor)
                    # TODO tener en cuenta la inclinacion para caer o no poder avanzar
                    if collision:
                        lemming.vel = vel
                        if lemming.action == "Fall":
                            lemming.action = "Walk"
                        lemming.floor = floor
                        break
                    else:
                        lemming.action = "Fall"
            if lemming.action == "Dig down":
                pass

    @staticmethod
    def collide_list(pos: Vector, floor):
        """ checks if a point is colliding whith a point list"""
        if pos in floor.relleno:
            if pos - Vector(0, 5) in floor.relleno:
                if pos - Vector(0, 10) in floor.relleno:
                    return True, Vector(0, 0)
                else:
                    return True, Vector(1, -1) * 0.02
            else:
                return True, Vector(0.03, 0)
        else:
            return False, None

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
        """returns the unit vector between two bidimensional points"""
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
