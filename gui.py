""" Graphic user interface

the buttons and that stuff
"""

import pygame


class Gui(object):
    """ stores and draw the buttons """

    def __init__(self, res, screen, character_list, discrete_debugging=False):
        height = res[0] / len(character_list)

        self.button_list = [
            Button(screen, i * height, res[1] - height, height, height,
                   discrete_debugging, text) for i, text in enumerate(character_list)
        ]

    def draw(self):
        """ draw each button """
        for button in self.button_list:
            button.draw()


class Button(object):
    """ Buttons to select the different actions """

    def __init__(self, screen, x, y, width, height, discrete_debugging, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.coordinates = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        self.text = text
        self.font = pygame.font.SysFont("Arial", 20)
        if discrete_debugging:
            self.color = 25, 0, 25
        else:
            self.color = 255, 0, 255

    def draw(self):
        """ draw the button """
        pygame.draw.lines(self.screen, self.color, 0, self.coordinates, 2)
        label = self.font.render(self.text, 1, (255, 220, 255))
        self.screen.blit(label, (self.x + 10, self.y + self.height / 2))
