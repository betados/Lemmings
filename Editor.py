from OpenGL.GL import *
from OpenGL.GLU import *
import os, sys, math, random
import pygame
from pygame.locals import *
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
import GL
from ScenarioEdit import Scenario
from Lemming import LemmingList
from Interaction import Interaction

pygame.init()
reloj = pygame.time.Clock()


size = (800, 600)
scenario = Scenario(size)
interaction = Interaction()
pygame.display.set_caption('Lemmings map editor')
pygame.display.set_mode(size, OPENGL|DOUBLEBUF)
GL.resize(size)
GL.init(size)

done = False


while not done:

    # --- Bucle principal de eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            done = True
        if evento.type == pygame.MOUSEBUTTONDOWN:
           pass

    if pygame.mouse.get_pressed()[0] == 1:
        scenario.add(pygame.mouse.get_pos())

    # --- LA LÓGICA DEL JUEGO DEBERÍA IR AQUÍ
    teclas = pygame.key.get_pressed()

    # if teclas[pygame.K_w]:
    #     # x=x+0.2
    #     avance = avance[0]+1, avance[1]
    # if teclas[pygame.K_a]:
    #     # y=y+0.2
    #     avance = avance[0], avance[1]+1

    #SAVE
    if teclas[pygame.K_s]:
        print("s")
        import xml.etree.cElementTree as ET

        root = ET.Element("floor")
        points = ET.SubElement(root, "points")
        for i,point in enumerate(scenario.getFloor().getPoints()):
            ET.SubElement(points, "point", number=str(i)).text = str(point)
        tree = ET.ElementTree(root)
        tree.write("output.xml")


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

    # borra lo anterior
    glClearColor(0.0, 0.0, 0.0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_LIGHTING)
    scenario.draw()
    glEnable(GL_LIGHTING)
    glFlush()


    # --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.

    pygame.display.flip()

    # --- Limitamos a 60 fotogramas por segundo (frames per second)
    # print("iteracion")
    reloj.tick(10)

# Cerramos la ventana y salimos.
# Si te olvidas de esta última línea, el programa se 'colgará'
# al salir si lo hemos estado ejecutando desde el IDLE.
pygame.quit()
