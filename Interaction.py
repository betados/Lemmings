# -*- coding: utf-8 -*-

""" Check the interaction between the elements in the game """
from vector_2d import Vector
from Scenario import Floor
from typing import List, Tuple, Optional
from Lemming import LemmingList

V = 0.03
COS45 = 0.71


class Interaction(object):
    """ static class in charge of checking interaction between different elements"""

    @staticmethod
    def camina_rect(lemming_list: LemmingList, floor_list: List[Floor]):
        """ look each lemming checking if it is touching a floor"""
        for lemming in lemming_list:
            if lemming.action in ("Walk", "Bomb", "Fall"):
                for floor in floor_list:
                    collision, vel = Interaction.collide_list(lemming.knee.int_vector(), floor)
                    if collision:
                        if lemming.action == "Fall":
                            lemming.action = "Walk"
                        if lemming.action == 'Walk':
                            lemming.vel_dict['Walk'] = vel
                        lemming.floor = floor
                        break
                    else:
                        lemming.action = "Fall"
            if lemming.action == "Dig down":
                pass

    @staticmethod
    def collide_list(pos: Vector, floor: Floor) -> Tuple[bool, Optional[Vector]]:
        """ checks if a point is colliding whith a point list"""
        if pos in floor.point_list.relleno:
            if pos - Vector(0, 5) in floor.point_list.relleno:
                if pos - Vector(0, 10) in floor.point_list.relleno:
                    return True, Vector(0, 0)
                else:
                    return True, Vector(1, -1) * V * COS45
            else:
                return True, Vector(V, 0)
        elif pos + Vector(0, 5) in floor.point_list.relleno:
            return True, Vector(1, 1) * V * COS45
        else:
            return False, None

    @staticmethod
    def is_button_pressed(pos: Vector, button_list) -> str:
        """ check if and witch button of the gui is clicked """
        for button in button_list:
            if button.coordinates[1][0] > pos[0] > button.coordinates[0][0] and \
                    button.coordinates[0][1] < pos[1] < button.coordinates[3][1]:
                print(button.text)
                return button.text

    @staticmethod
    def is_lemming_pressed(pos: Tuple[int, int], lemming_list: LemmingList, state_dict: dict) -> int:
        """ check if and witch lemming is clicked  """
        for lemming in lemming_list:
            if lemming.rect.collidepoint(pos):
                print(lemming.index)
                lemming.action = state_dict["action"]
                return lemming.index

    # TODO comprabación lemming-lemming y sus complementos
