from OpenGL.GL import *
from OpenGL.GLU import *
import os, sys, math, random
import pygame
from pygame.locals import *
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
import GL
from Scenario import Scenario
from Lemming import Lemming

pygame.init()
reloj = pygame.time.Clock()




size = (800, 600)
scenario = Scenario(size)
lemming = Lemming()
pygame.display.set_caption('Le')
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


    # --- LA LÓGICA DEL JUEGO DEBERÍA IR AQUÍ
    avance = 0, 0
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_w]:
        # x=x+0.2
        avance = avance[0]+1, avance[1]
    if teclas[pygame.K_a]:
        # y=y+0.2
        avance = avance[0], avance[1]+1
    if teclas[pygame.K_s]:
        # x=x-0.2
        avance = avance[0]-1, avance[1]
    if teclas[pygame.K_d]:
        # y=y-0.2
        avance = avance[0], avance[1]-1

    # para sair
    if teclas[pygame.K_ESCAPE]:
        done=True

    t=reloj.get_time()
    # print(t)



    # posicion y orientacion de la cámara
    # glMatrixMode(GL_PROJECTION);
    # glLoadIdentity()
    # gluPerspective(90, 1, 0.01, 1000)

    #
    # if primeraPersona:
    #     """PRIMERA PERSONA"""
    #     gluLookAt(personaje.getPos()[0], personaje.getPos()[1], matriz.getZ(),  # pos
    #               personaje.getMirada()[0], personaje.getMirada()[1], personaje.getMirada()[2],  # hacia donde mira
    #               0, 0, 1)  # eje vertical
    # else:
    #     """TERCERA PERSONA"""
    #     gluLookAt(personaje.getPos()[0], personaje.getPos()[1], matriz.getZ()*8,  # pos
    #               personaje.getPos()[0]+1, personaje.getPos()[1], 0,  # hacia donde mira
    #                   0, 0, 1)  # eje vertical



    # --- EL CÓDIGO DE DIBUJO DEBERÍA IR AQUÍ

    # borra lo anterior
    glClearColor(0.0, 0.0, 0.0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_LIGHTING)
    scenario.draw()
    lemming.draw(t)
    glEnable(GL_LIGHTING)
    glFlush()


    # use the texture
    # vertices & texture data






    # print(reloj.get_time())
    # listaGranos.actualiza(reloj.get_time())
    # listaGranos.dibuja()

    # --- Avanzamos y actualizamos la pantalla con lo que hemos dibujado.

    pygame.display.flip()

    # --- Limitamos a 60 fotogramas por segundo (frames per second)
    # print("iteracion")
    reloj.tick(10)

# Cerramos la ventana y salimos.
# Si te olvidas de esta última línea, el programa se 'colgará'
# al salir si lo hemos estado ejecutando desde el IDLE.
pygame.quit()
