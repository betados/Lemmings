""" Graphic user interface

the buttons and that stuff
"""

import pygame


class Gui(object):
    """ stores and draw the buttons """
    def __init__(self, res, screen, characterList, discreteDebugging=False):
        self.screen = screen
        self.res = res
        self.characterList = characterList
        self.quantity = len(self.characterList)
        self.height = res[0] / self.quantity

        self.buttonList = []
        for i, text in enumerate(self.characterList):
            button = Button(self.screen, i*self.height, self.res[1]-self.height,
                            self.height, self.height, discreteDebugging, text=text)
            self.buttonList.append(button)

    def draw(self):
        """ draw each button """
        for button in self.buttonList:
            button.draw()
        # self.images()

    # def images(self):
    #     self.image = pygame.image.load("images/lemmings.png").convert()
    #     for i,rect in enumerate(self.characterList):
    #         self.screen.blit(self.image, ((i+1)*self.height,self.res[1]-self.height/2), rect)


class Button(object):
    """ Buttons to select the different actions """
    def __init__(self, screen, x, y, width, height, discreteDebugging, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.coordinates = [(x, y), (x+width, y), (x+width, y+height), (x, y+height)]
        self.text = text
        self.font = pygame.font.SysFont("Arial", 20)
        if discreteDebugging:
            self.color = 25, 0, 25
        else:
            self.color = 255, 0, 255

    def draw(self):
        """ draw the button """
        pygame.draw.lines(self.screen, self.color, 0, self.coordinates, 2)
        label = self.font.render(self.text, 1, (255, 220, 255))
        self.screen.blit(label, (self.x+10, self.y+self.height/2))
