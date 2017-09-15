import unittest
from Interaction import Interaction


class TestAlvaro(unittest.TestCase):
    def test_getDistance(self):
        point1 = 5, 5
        for i in range(99):
            point2 = 5, point1[1]+i
            self.assertEqual(Interaction.getDistance(point1, point2), i)

    def test_collideList(self):
        self.assertEqual(Interaction.collideList((0, 0), [(0, 0), (1, 1)]),
                         (True, (0, 0), (1, 1)))

if __name__ == '__main__':
    unittest.main()