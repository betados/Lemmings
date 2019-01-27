# -*- coding: utf-8 -*-

import os
import sys
import eztext
import pygame
from ScenarioEdit import Scenario

if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
reloj = pygame.time.Clock()

resolution = (800, 600)
scenario = Scenario(resolution)
pygame.display.set_caption('Lemmings map editor')
screen = pygame.display.set_mode(resolution)

WHITE = 100, 100, 100

done = False
previousPosition = -9999, -9999

state = "drawing"

text = eztext.Input(maxlength=45, color=(100, 0, 0), prompt='Scenario name: ')

while not done:

    screen.fill((0, 0, 0))
    events = pygame.event.get()
    teclas = pygame.key.get_pressed()
    if state == "drawing":
        # --- Bucle principal de eventos

        for event in events:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                scenario.newFloor()
            if event.type == pygame.MOUSEBUTTONUP:
                pass

        if pygame.mouse.get_pressed()[0] == 1:
            movement = pygame.mouse.get_rel()
            position = pygame.mouse.get_pos()
            if movement[0] != 0 or movement[1] != 0:
                scenario.add(position)
                previousPosition = position

        # --- LA LÓGICA DEL JUEGO DEBERÍA IR AQUÍ

        # SAVE
        if teclas[pygame.K_s]:
            events = 0
            state = "saving"
            text = eztext.Input(maxlength=45, color=(150, 0, 0), prompt='Scenario name: ')

        # TEXT
        size = 20
        myfont = pygame.font.SysFont("calibri", size)
        # render text
        label = myfont.render("To save press \"s\"", 1, (0, 100, 255))
        screen.blit(label, (resolution[0] / 50, resolution[1] - size))
        label = myfont.render("To exit press esc", 1, (0, 100, 255))
        screen.blit(label, (resolution[0] / 50, resolution[1] - size * 2))

        # to exit
        if teclas[pygame.K_ESCAPE]:
            done = True

    scenario.draw(screen)

    if state == "saving" and events != 0:
        if teclas[pygame.K_RETURN] or teclas[pygame.K_KP_ENTER]:
            scenario.save(text.getInput())
            state = "drawing"
        text.update(events)
        text.draw(screen)

        # TEXT
        size = 20
        myfont = pygame.font.SysFont("calibri", size)
        # render text
        label = myfont.render("To save press enter", 1, (0, 100, 255))
        screen.blit(label, (resolution[0] / 50, resolution[1] - size))

    # t=reloj.get_time()
    # print(t)

    # --- EL CÓDIGO DE DIBUJO DEBERÍA IR AQUÍ

    # # borra lo anterior

    # --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.

    pygame.display.flip()

    # --- Limitamos a 60 fotogramas por segundo (frames per second)
    # print("iteracion")
    reloj.tick(500)

# Cerramos la ventana y salimos.
# Si te olvidas de esta última línea, el programa se 'colgará'
# al salir si lo hemos estado ejecutando desde el IDLE.
pygame.quit()
