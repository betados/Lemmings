import pygame

class Gui:
    def __init__(self, res, screen):
        self.screen = screen
        self.res = res
        self.characterList = ["Stop", "Stairs", "Bomb", "Dig down", "Dig horiz.","Parachute"]
        self.quantity = len(self.characterList)
        self.heigth = res[0] / self.quantity

        self.font = pygame.font.SysFont("calibri", 30)

    def draw(self):
        for i in range(self.quantity):
            pygame.draw.line(self.screen,(100, 100, 100),((i+1)*self.heigth,self.res[1]),((i+1)*self.heigth,self.res[1]-self.heigth),2)
        pygame.draw.line(self.screen,(100, 100, 100),(0,self.res[1]-self.heigth),(self.res[0],self.res[1]-self.heigth))
        # self.images()
        self.text()

    def text(self):
        for i,text in enumerate(self.characterList):
            # TEXT
            # render text
            label = self.font.render(text, 1, (255, 255, 255))
            self.screen.blit(label, (i*self.heigth+20,self.res[1]-self.heigth/2))
            # self.screen.blit(label, (50,50))

    def images(self):
        self.image = pygame.image.load("images/lemmings.png").convert()
        for i,rect in enumerate(self.characterList):
            self.screen.blit(self.image, ((i+1)*self.heigth,self.res[1]-self.heigth/2), rect)


