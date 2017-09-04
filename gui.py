import pygame


class Gui:
    def __init__(self, res, screen):
        self.screen = screen
        self.res = res
        self.characterList = ["Stop", "Stairs up", "Stairs down", "Bomb",
                              "Dig down", "Dig horiz.","Parachute"]
        self.quantity = len(self.characterList)
        self.height = res[0] / self.quantity

        self.buttonList = []
        for i, text in enumerate(self.characterList):
            button = Button(self.screen, i*self.height, self.res[1]-self.height,
                            self.height, self.height, text=text)
            self.buttonList.append(button)

    def draw(self):
        for button in self.buttonList:
            button.draw()
        # self.images()

    def images(self):
        self.image = pygame.image.load("images/lemmings.png").convert()
        for i,rect in enumerate(self.characterList):
            self.screen.blit(self.image, ((i+1)*self.height,self.res[1]-self.height/2), rect)


class Button:
    def __init__(self, screen, x, y, width, height, text):
        # self.rect = rect
        self.screen = screen
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.coordinates = [(x, y), (x+width, y), (x+width, y+height), (x, y+height)]
        self.text = text
        self.font = pygame.font.SysFont("calibri", 20)

    def draw(self):
        pygame.draw.lines(self.screen, (255, 0, 255), 0, self.coordinates, 2)
        label = self.font.render(self.text, 1, (255, 220, 255))
        self.screen.blit(label, (self.x+10, self.y+self.height/2))






