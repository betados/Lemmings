from OpenGL.GL import *
from OpenGL.GLU import *


def resize(res):
    pass
    # if res[1] == 0:
    #     res[1] = 1
    # glViewport(0, 0, res[0], res[1])
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # gluPerspective(45, 1.0 * res[0] / res[1], 1.0, 10000.0)
    # glMatrixMode(GL_MODELVIEW)
    # glLoadIdentity()


def init(res):
    # aspect = float(res[0]) / float(res[1])
    # glViewport(int(-res[0]/2)+10, int(-res[1]/2)+10, int(res[0]*1), res[1])
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # glOrtho(-aspect * 30, aspect * 30, -30, 30, -1, 1)
    #
    # glMatrixMode(GL_MODELVIEW);
    # glLoadIdentity()
    #
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Get a perspective at the helix
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity()
    gluPerspective(90, 1, 0.01, 1000)
    gluLookAt(int(res[0]/2),int(res[1]/2), 401,  # pos
                 int(res[0] / 2), int(res[1] / 2), 0,  # hacia donde mira
              0, 1, 0)  # eje vertical
    # CameraPos = [40.0, 50.0, 40.0]
    glMatrixMode(GL_MODELVIEW)
    # glEnable(GL_BLEND) """transparencia"""
    glBlendFunc(GL_SRC_ALPHA, GL_ONE) # XXX Why GL_ONE?
    glShadeModel(GL_SMOOTH)

    # glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
