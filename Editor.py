
import os, sys, math, random
import pygame
from pygame.locals import *
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
import GL
from ScenarioEdit import Scenario
from Interaction import Interaction

pygame.init()
reloj = pygame.time.Clock()


size = (800, 600)
scenario = Scenario(size)
interaction = Interaction()
pygame.display.set_caption('Lemmings map editor')
screen = pygame.display.set_mode(size)
# GL.resize(size)
# GL.init(size)


WHITE = 255, 255, 255

done = False
previousPosition = -9999, -9999

while not done:

    # --- Bucle principal de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            done = True
        if evento.type == pygame.MOUSEBUTTONDOWN:
           scenario.newFloor()
           # position = pygame.mouse.get_pos()
           # rect2 = pygame.draw.rect(screen, WHITE, (position[0], position[1], 60, 60), 3)  # not filled
        if evento.type == pygame.MOUSEBUTTONUP:
            pass
           # scenario.addFloor()

    if pygame.mouse.get_pressed()[0] == 1:
        movimiento = pygame.mouse.get_rel()
        position = pygame.mouse.get_pos()
        # print(movimiento)
        if movimiento[0] != 0 or movimiento[1] != 0:
            # print(position)
            scenario.add(position)
            previousPosition= position

    # --- LA LÓGICA DEL JUEGO DEBERÍA IR AQUÍ
    teclas = pygame.key.get_pressed()

    # if teclas[pygame.K_w]:
    #     # x=x+0.2
    #     avance = avance[0]+1, avance[1]
    if teclas[pygame.K_a]:
        # draw a few rectangles

        rect1 = pygame.draw.rect(screen, WHITE, (20, 20, 60, 60), 0)  # filled = 0
        rect2 = pygame.draw.rect(screen, WHITE, (100, 20, 60, 60), 3)  # not filled
    #     # y=y+0.2
    #     avance = avance[0], avance[1]+1

    #SAVE
    if teclas[pygame.K_s]:
        # pygame.key.get_pressed()

        # font = pygame.font.Font(None, 50)
        # block = font.render("ola ka ase", True, (255, 255, 255))
        # rect = block.get_rect()
        # rect.center = newScreen.get_rect().center
        # newScreen.blit(block, rect)

        scenario.save()


    #     # x=x-0.2
    #     avance = avance[0]-1, avance[1]
    # if teclas[pygame.K_d]:
    #     # y=y-0.2
    #     avance = avance[0], avance[1]-1

    # para sair
    if teclas[pygame.K_ESCAPE]:
        done=True

    # t=reloj.get_time()
    # print(t)


    # --- EL CÓDIGO DE DIBUJO DEBERÍA IR AQUÍ

    # # borra lo anterior
    # glClearColor(0.0, 0.0, 0.0, 1)
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glDisable(GL_LIGHTING)

    scenario.draw(screen)
    #
    # glEnable(GL_LIGHTING)
    # glFlush()


    # --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.

    pygame.display.flip()

    # --- Limitamos a 60 fotogramas por segundo (frames per second)
    # print("iteracion")
    reloj.tick(20)

# Cerramos la ventana y salimos.
# Si te olvidas de esta última línea, el programa se 'colgará'
# al salir si lo hemos estado ejecutando desde el IDLE.
pygame.quit()
