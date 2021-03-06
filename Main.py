# -*- coding: utf-8 -*-

import os
import sys

import pygame

import eztext
from Interaction import Interaction
from Lemming import LemmingList
from Scenario import Scenario
from gui import Gui

if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
resolution = (800, 600)

character_list = ['Stop', 'Climb', 'Stairway', 'Bomb',
                  'Dig down', 'Dig horiz.', 'Dig diag.', 'Parachute']

pygame.display.set_caption('Lemmings')
screen = pygame.display.set_mode(resolution)
scenario = Scenario(screen, resolution)
gui = Gui(resolution, screen, character_list)
lemmingQuantity = 10
lemmingList = LemmingList(lemmingQuantity, screen)

stateDict = {'isActionSelected': False}
done = False
reloj = pygame.time.Clock()
t = reloj.get_time()

status = 'drawing'
# text = eztext.Input(maxlength=45, color=(100, 0, 0), prompt='Scenario name: ')

while not done:
    screen.fill((0, 0, 0))
    events = pygame.event.get()
    teclas = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT:
            done = True

    # para sair
    if teclas[pygame.K_ESCAPE]:
        done = True
    if teclas[pygame.K_q]:
        stateDict['isActionSelected'] = False

    if status == 'drawing':
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                scenario.new_floor()
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        if not scenario.floor_list:
            myfont = pygame.font.SysFont('Impact', 50)
            label = myfont.render('DRAW SOMETHING', 1, (30, 0, 30))
            screen.blit(label, (200, 200))

        if pygame.mouse.get_pressed()[0] == 1:
            movement = pygame.mouse.get_rel()
            position = pygame.mouse.get_pos()
            if movement[0] != 0 or movement[1] != 0:
                scenario.append(position)

        # SAVE
        if teclas[pygame.K_s]:
            events = 0
            status = 'saving'
            text = eztext.Input(maxlength=45, color=(150, 0, 0), prompt='Scenario name: ')

        # LOAD
        if teclas[pygame.K_l]:
            scenario.load('maps/.yaml')
            status = 'playing'

        # TEXT
        size = 20
        myfont = pygame.font.SysFont('calibri', size)
        # render text
        label = myfont.render('To save press \'s\'', 1, (0, 100, 255))
        screen.blit(label, (resolution[0] / 50, resolution[1] - size))
        label = myfont.render('To load press \'L\'', 1, (0, 100, 255))
        screen.blit(label, (resolution[0] / 50, resolution[1] - size * 2))
        label = myfont.render('To exit press esc', 1, (0, 100, 255))
        screen.blit(label, (resolution[0] / 50, resolution[1] - size * 3))

        # to exit
        if teclas[pygame.K_ESCAPE]:
            done = True

    elif status == 'playing':

        if pygame.mouse.get_pressed()[0] == 1:
            position = pygame.mouse.get_pos()
            if not stateDict['isActionSelected']:
                clicked_action = Interaction.is_button_pressed(position, gui.buttonList)
                if clicked_action is not None:
                    stateDict['isActionSelected'] = True
                    stateDict['action'] = clicked_action
            else:
                clicked_lemming = Interaction.is_lemming_pressed(position, lemmingList.lista, stateDict)
                if clicked_lemming is not None:
                    stateDict['isActionSelected'] = False
        Interaction.camina_rect(lemmingList, scenario.floor_list)
        gui.draw()
        lemmingList.draw(t, screen)

    elif status == 'saving' and events != 0:
        if teclas[pygame.K_RETURN] or teclas[pygame.K_KP_ENTER]:
            scenario.save(text.getInput())
            status = 'playing'

        text.update(events)
        text.draw(screen)

        # TEXT
        size = 20
        myfont = pygame.font.SysFont('Arial', size)
        # render text
        label = myfont.render('To save press enter', 1, (0, 100, 255))
        screen.blit(label, (resolution[0] / 50, resolution[1] - size))

    # PRINT MOUSE
    myfont = pygame.font.SysFont('Arial', 20)
    label = myfont.render(str(pygame.mouse.get_pos()), 1, (250, 0, 255))
    screen.blit(label, (resolution[0] / 2, resolution[1] - 25))

    t = reloj.get_time()
    scenario.draw(status)
    pygame.display.flip()

    reloj.tick(60)

pygame.quit()
