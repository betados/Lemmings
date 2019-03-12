import unittest
from interaction import Interaction
from lemming import LemmingList
from scenario import Scenario, Floor
from vector_2d import Vector
import pygame


class TestInteraction(unittest.TestCase):
    pygame.init()
    res = (640, 480)
    screen = pygame.display.set_mode(res)
    scenario = Scenario(screen, res)
    floor = Floor(res)
    floor.point_list.relleno = {Vector(1, i) for i in range(10, 100)}
    scenario.floor_list.append(floor)

    def test_walking(self):
        lemmings = LemmingList(1)
        lemmings[0].pos = Vector(1, 0)
        lemmings[0].actualize(1)
        # print('\n', lemmings[0].action)
        Interaction.walking(lemmings, TestInteraction.scenario.floor_list)
        # print()
        self.assertEqual('Fall', lemmings[0].action)
        lemmings[0].pos = Vector(1, 20)
        lemmings[0].actualize(1)
        print('\n', lemmings[0].action)


if __name__ == '__main__':
    unittest.main()
