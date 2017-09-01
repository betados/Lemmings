
# -*- coding: utf-8 -*-

import os, sys, math, random
import pygame
from pygame.locals import *
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

from Scenario import Scenario
from Lemming import LemmingList
from Interaction import Interaction

pygame.init()
reloj = pygame.time.Clock()


resolution = (800, 600)


pygame.display.set_caption('Lemmings')
screen = pygame.display.set_mode(resolution)
scenario = Scenario(screen, resolution, "maps/a.yaml")
lemmingList = LemmingList(10)
interaction = Interaction()

done = False


while not done:

    screen.fill((0, 0, 0))
    events = pygame.event.get()
    teclas = pygame.key.get_pressed()

    # --- Bucle principal de eventos
    for event in events:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass


    # --- LA LÓGICA DEL JUEGO DEBERÍA IR AQUÍ
    teclas = pygame.key.get_pressed()

    # if teclas[pygame.K_w]:
    #     # x=x+0.2
    #     avance = avance[0]+1, avance[1]
    # if teclas[pygame.K_a]:
    #     # y=y+0.2
    #     avance = avance[0], avance[1]+1
    # if teclas[pygame.K_s]:
    #     # x=x-0.2
    #     avance = avance[0]-1, avance[1]
    # if teclas[pygame.K_d]:
    #     # y=y-0.2
    #     avance = avance[0], avance[1]-1

    # para sair
    if teclas[pygame.K_ESCAPE]:
        done=True

    t=reloj.get_time()
    # print(t)


    # --- EL CÓDIGO DE DIBUJO DEBERÍA IR AQUÍ

    # borra lo anterior
    scenario.draw()
    interaction.caminaRect(lemmingList, scenario.floorList)
    # interaction.check(lemmingList, scenario.getFloor())
    lemmingList.draw(t, screen)


    # --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.

    pygame.display.flip()

    # --- Limitamos a 60 fotogramas por segundo (frames per second)
    # print("iteracion")
    reloj.tick(200)

# Cerramos la ventana y salimos.
# Si te olvidas de esta última línea, el programa se 'colgará'
# al salir si lo hemos estado ejecutando desde el IDLE.
pygame.quit()
