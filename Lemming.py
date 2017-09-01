import pygame

class LemmingList:

    def __init__(self,quantity):
        self.lista = []
        for i in range(quantity):
            lemming = Lemming(i)
            self.lista.append(lemming)
    def draw(self,t,screen):
        for lemming in self.lista:
            lemming.draw(t, screen)
    def getList(self):
        return self.lista

class Lemming:
    def __init__(self, index):
        self.index = index
        self.pos = 20, (index-10)*100
        self.alto = 30
        self.ancho = 8
        self.rect = pygame.Rect(self.pos, (self.ancho, self.alto))
        self.rect.bottomright = self.pos

        self.vel = 0.03, 0
        self.accel = 0, 0
        self.sprite = Sprite()
    def draw(self,t, screen):
        # print(self.pos)
        self.vel = self.vel[0] + 0.5 * self.accel[0] * t*t, self.vel[1] + 0.5 * self.accel[1] * t*t
        self.pos = self.pos[0] + self.vel[0]*t,  self.pos[1] + self.vel[1]*t
        self.rect.bottomright = self.pos
        self.sprite.rect.x = self.pos[0]
        self.sprite.rect.y = self.pos[1]

        screen.blit(self.sprite.image, self.rect, self.getLemming(0,2))


        # self.color = 50, 0, 0

        # pygame.draw.rect(screen, (0, 100, 0), self.rect, 2)

    def getLemming(self,x,y):
        side = 47
        return (side*x+10, side* y+-1, side*0.6, side)



class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        # super().__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([5, 5])
        self.image = pygame.image.load("images/lemmings.png").convert()
        self.rect = self.image.get_rect()
