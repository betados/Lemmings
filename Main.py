
# -*- coding: utf-8 -*-

import os, sys, math, random
import pygame
from pygame.locals import *
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

from Scenario import Scenario
from Lemming import LemmingList
from Interaction import Interaction
from gui import Gui

pygame.init()
reloj = pygame.time.Clock()


resolution = (800, 600)

discreteDebugging = True

characterList = ["Stop", "Stairs up", "Stairs down", "Bomb",
                "Dig down", "Dig horiz.", "Parachute"]

pygame.display.set_caption('Lemmings')
screen = pygame.display.set_mode(resolution)
scenario = Scenario(screen, resolution, "maps/a.yaml", discreteDebugging)
gui = Gui(resolution, screen, characterList, discreteDebugging)
lemmingList = LemmingList(10, discreteDebugging)
interaction = Interaction()

stateDict = {}
stateDict["isActionSelected"] = False
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
    # para sair
    if teclas[pygame.K_ESCAPE]:
        done=True
    if teclas[pygame.K_q]:
        stateDict["isActionSelected"] = False


    if pygame.mouse.get_pressed()[0] == 1:
        position = pygame.mouse.get_pos()
        if not stateDict["isActionSelected"]:
            click = interaction.isButtonPressed(position, gui.buttonList)
            if click is not None:
                stateDict["isActionSelected"] = True
                stateDict["action"] = click
        else:
            click = interaction.isLemmingPressed(position, lemmingList.lista, stateDict)
            if click is not None:
                stateDict["isActionSelected"] = False
                # stateDict["actionSelected"] = click




    t=reloj.get_time()
    # print(t)


    # --- EL CÓDIGO DE DIBUJO DEBERÍA IR AQUÍ

    # borra lo anterior
    scenario.draw()
    interaction.caminaRect(lemmingList, scenario.floorList)
    gui.draw()
    lemmingList.draw(t, screen)


    # --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.

    pygame.display.flip()

    # --- Limitamos a 60 fotogramas por segundo (frames per second)
    reloj.tick(100)

# Cerramos la ventana y salimos.
# Si te olvidas de esta última línea, el programa se 'colgará'
# al salir si lo hemos estado ejecutando desde el IDLE.
pygame.quit()
