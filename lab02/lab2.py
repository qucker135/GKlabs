#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from random import *
import math

def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass

def draw_rectangle(x,y,a,b,d=0.0):
    glColor3f(1.0, 0.0, 0.0)

    #seed(3)
    dx = random()
    dy = random()

    glBegin(GL_TRIANGLES)
    glVertex2f(x-a/2.0+d*dx, y-b/2.0+d*dy)
    glVertex2f(x+a/2.0+d*dx, y-b/2.0+d*dy)
    glVertex2f(x-a/2.0+d*dx, y+b/2.0+d*dy)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x+a/2.0+d*dx, y+b/2.0+d*dy)
    glVertex2f(x+a/2.0+d*dx, y-b/2.0+d*dy)
    glVertex2f(x-a/2.0+d*dx, y+b/2.0+d*dy)
    glEnd()

def draw_equilateral_triangle(x,y,a): #współrzędne dolnego wierzchołka oraz bok
    glColor(1.0,1.0,0.0)

    glBegin(GL_TRIANGLES)
    glVertex2f(x,y)
    glVertex2f(x+a,y)
    glVertex2f(x+a/2.0, y+a*math.sqrt(0.75))
    glEnd()
   
def draw_sierpinski_triangle(x,y,n,a): #współrzędne dolnego wierzchołka oraz bok
    if n==0:
        draw_equilateral_triangle(x,y,a)
    else:
        draw_sierpinski_triangle(x      ,y                     ,n-1,a/2.0)
        draw_sierpinski_triangle(x+a/2.0,y                     ,n-1,a/2.0)
        draw_sierpinski_triangle(x+a/4.0,y+a*math.sqrt(3.0)/4.0,n-1,a/2.0)

def draw_sierpinski_carpet(x,y,a,b,n,d=0.0):
    if n==0:
        draw_rectangle(x,y,a,b,d)
    else:
        draw_sierpinski_carpet(x-a/3.0,y-b/3.0,a/3.0,b/3.0,n-1,d)
        draw_sierpinski_carpet(x-a/3.0,y,      a/3.0,b/3.0,n-1,d)
        draw_sierpinski_carpet(x-a/3.0,y+b/3.0,a/3.0,b/3.0,n-1,d)
        draw_sierpinski_carpet(x      ,y-b/3.0,a/3.0,b/3.0,n-1,d)
        #draw_sierpinski_carpet(x      ,y,      a/3.0,b/3.0,n-1,d)
        draw_sierpinski_carpet(x      ,y+b/3.0,a/3.0,b/3.0,n-1,d)
        draw_sierpinski_carpet(x+a/3.0,y-b/3.0,a/3.0,b/3.0,n-1,d)
        draw_sierpinski_carpet(x+a/3.0,y,      a/3.0,b/3.0,n-1,d)
        draw_sierpinski_carpet(x+a/3.0,y+b/3.0,a/3.0,b/3.0,n-1,d)

def draw_fractal_amogus(x,y,a,b,n,d=0.0):
    if n==0:
        draw_rectangle(x,y,a,b,d)
    else:
        draw_fractal_amogus(x-a*0.4,y-b*0.4,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x-a*0.2,y+b*0.4,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x-a*0.2,y+b*0.2,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x-a*0.2,y      ,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x-a*0.2,y-b*0.2,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x-a*0.2,y-b*0.4,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x      ,y+b*0.4,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x      ,y      ,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x+a*0.2,y+b*0.4,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x+a*0.2,y      ,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x+a*0.2,y-b*0.4,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x+a*0.4,y+b*0.4,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x+a*0.4,y+b*0.2,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x+a*0.4,y      ,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x+a*0.4,y-b*0.2,a/5.0,b/5.0,n-1,d)
        draw_fractal_amogus(x+a*0.4,y-b*0.4,a/5.0,b/5.0,n-1,d)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)
    ############################
    #Prosze odkomentowac odpowiednia funkcje ponizej
    
    #draw_rectangle(20.0, 30.0, 50.0, 10.0, 10.0)
    #draw_sierpinski_carpet(0.0,0.0,100.0,100.0,3,4.0)
    draw_fractal_amogus(0.0,0.0,100.0,100.0,4,0.0)
    draw_sierpinski_triangle(-10.0,-10.0,2,30.0)
    #draw_equilateral_triangle(-10.0,-10.0,30.0)
    ############################

    #glColor3f(0.0, 1.0, 0.0)
    #glBegin(GL_TRIANGLES)
    #glVertex2f(0.0, 0.0)
    #glVertex2f(0.0, 50.0)
    #glVertex2f(50.0, 0.0)
    #glEnd()

    #glColor3f(1.0, 0.0, 0.0)
    #glBegin(GL_TRIANGLES)
    #glVertex2f(0.0, 0.0)
    #glVertex2f(0.0, 50.0)
    #glVertex2f(-50.0, 0.0)
    #glEnd()

    #glBegin(GL_TRIANGLES)
    #glColor3f(1.0, 0.0, 1.0)
    #glVertex2f(50.0, 0.0)
    #glColor3f(0.0, 1.0, 1.0)
    #glVertex2f(50.0, 50.0)
    #glColor3f(1.0, 1.0, 0.0)
    #glVertex2f(0.0, 50.0)
    #glEnd()

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
        glOrtho(-100.0, 100.0, -100.0 / aspect_ratio, 100.0 / aspect_ratio,
                1.0, -1.0)
    else:
        glOrtho(-100.0 * aspect_ratio, 100.0 * aspect_ratio, -100.0, 100.0,
                1.0, -1.0)

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
