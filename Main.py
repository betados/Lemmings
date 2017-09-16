
# -*- coding: utf-8 -*-

import os
import sys
import pygame

from Scenario import Scenario
from Lemming import LemmingList
from Interaction import Interaction
from gui import Gui

if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()


resolution = (800, 600)

discreteDebugging = False

characterList = ["Stop", "Climb", "Stairway", "Bomb",
                 "Dig down", "Dig horiz.", "Dig diag.", "Parachute"]


pygame.display.set_caption('Lemmings')
screen = pygame.display.set_mode(resolution)
scenario = Scenario(screen, resolution, "maps/a.yaml", discreteDebugging)
gui = Gui(resolution, screen, characterList, discreteDebugging)
lemmingQuantity = 10
lemmingList = LemmingList(lemmingQuantity, screen, discreteDebugging)

stateDict = dict()
stateDict["isActionSelected"] = False
done = False
reloj = pygame.time.Clock()
t = reloj.get_time()

while not done:

    screen.fill((0, 0, 0))
    events = pygame.event.get()
    teclas = pygame.key.get_pressed()

    # --- Bucle principal de eventos
    for event in events:
        if event.type == pygame.QUIT:
            done = True
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     pass

    # --- LA LÓGICA DEL JUEGO DEBERÍA IR AQUÍ

    # para sair
    if teclas[pygame.K_ESCAPE]:
        done = True
    if teclas[pygame.K_q]:
        stateDict["isActionSelected"] = False

    if pygame.mouse.get_pressed()[0] == 1:
        position = pygame.mouse.get_pos()
        if not stateDict["isActionSelected"]:
            click = Interaction.isButtonPressed(position, gui.buttonList)
            if click is not None:
                stateDict["isActionSelected"] = True
                stateDict["action"] = click
        else:
            click = Interaction.isLemmingPressed(position, lemmingList.lista, stateDict)
            if click is not None:
                stateDict["isActionSelected"] = False

    t = reloj.get_time()

    # --- EL CÓDIGO DE DIBUJO DEBERÍA IR AQUÍ

    # borra lo anterior
    scenario.draw()
    Interaction.caminaRect(lemmingList, scenario.floorList)
    gui.draw()
    lemmingList.draw(t, screen)

    # --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.
    pygame.display.flip()

    # --- Limitamos a 60 fotogramas por segundo (frames per second)
    reloj.tick(60)

# Cerramos la ventana y salimos.
# Si te olvidas de esta última línea, el programa se 'colgará'
# al salir si lo hemos estado ejecutando desde el IDLE.
pygame.quit()
