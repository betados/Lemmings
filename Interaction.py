# -*- coding: utf-8 -*-

""" Check the interaction between the elements in the game """
from vector_2d import Vector

V = 0.03
COS45 = 0.71


class Interaction(object):
    """ static class in charge of checking interaction between different elements"""

    @staticmethod
    def camina_rect(lemmingList, floor_list):
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
                    return True, Vector(1, -1) * V * COS45
            else:
                return True, Vector(V, 0)
        elif pos + Vector(0, 5) in floor.relleno:
            return True, Vector(1, 1) * V * COS45
        else:
            return False, None

    @staticmethod
    def is_button_pressed(pos, button_list):
        """ check if and witch button of the gui is clicked """
        for button in button_list:
            if button.coordinates[1][0] > pos[0] > button.coordinates[0][0] and \
                    button.coordinates[0][1] < pos[1] < button.coordinates[3][1]:
                print(button.text)
                return button.text
        return None

    @staticmethod
    def is_lemming_pressed(pos, lemming_list, state_dict):
        """ check if and witch lemming is clicked  """
        for lemming in lemming_list:
            if lemming.rect.collidepoint(pos):
                print(lemming.index)
                lemming.action = state_dict["action"]
                return lemming.index
        return None

    # TODO comprabación lemming-lemming y sus complementos
