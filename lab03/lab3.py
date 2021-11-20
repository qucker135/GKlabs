#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin, cos, pi

N = 50

def x(u,v):
    return ((((-90.0*u + 225.0)*u - 270.0)*u + 180.0)*u - 45.0)*u * cos(pi * v)

def y(u,v):
    return ((160.0*u - 320.0)*u + 160.0)*u*u - 5.0
    # alternatively: return 160.0*u*u*(u-1.0)*(u-1.0) - 5.0

def z(u,v):
    return ((((-90.0*u + 225.0)*u - 270.0)*u + 180.0)*u - 45.0)*u * sin(pi * v)

# u = i/(N-1) ; v = j/(N-1)
#tab = [[x(i/(N-1),j/(N-1)),y(i/(N-1),j/(N-1)),z(i/(N-1),j/(N-1))] for i in range(N) for j in range(N)]
tab = [[[x(u,v),y(u,v),z(u,v)] for i in range(N) for u in [i/(N-1)] ] for j in range(N) for v in [j/(N-1)]]


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def draw_egg_dots():
    glBegin(GL_POINTS)

    glColor3f(1.0, 1.0, 0.0) #yellow
    
    for i in range(N):
        for j in range(N):
            glVertex3fv(tab[i][j])

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    axes()
    spin(time * 180.0/pi)
    #rysowanie obiektu

    draw_egg_dots()
    

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
    #debug
    #print(tab)
