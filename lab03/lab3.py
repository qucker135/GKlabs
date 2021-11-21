#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import sin, cos, pi
from random import random

N = 21

def x(u,v):
    return ((((-90.0*u + 225.0)*u - 270.0)*u + 180.0)*u - 45.0)*u * cos(pi * v)

def y(u,v):
    return ((160.0*u - 320.0)*u + 160.0)*u*u - 5.0
    # alternatively: return 160.0*u*u*(u-1.0)*(u-1.0) - 5.0

def z(u,v):
    return ((((-90.0*u + 225.0)*u - 270.0)*u + 180.0)*u - 45.0)*u * sin(pi * v)

# u = i/(N-1) ; v = j/(N-1)
#vertices = [[x(i/(N-1),j/(N-1)),y(i/(N-1),j/(N-1)),z(i/(N-1),j/(N-1))] for i in range(N) for j in range(N)]
vertices = [[[x(u,v),y(u,v),z(u,v)] for i in range(N) for u in [i/(N-1)] ] for j in range(N) for v in [j/(N-1)]]
colors = [[[random(),random(),random()] for i in range(N)] for j in range(N)]

#pozbycie się ''paskow'':
#PYTANIE - dlaczego konieczne transponowanie?
'''
colors[N-1][0] = colors[0][0]
for j in range(1,N):
    colors[0][j] = colors[0][0]
    colors[N-1][j] = colors[0][0]

if N%2==1:
    for j in range(1,N):
        colors[(N-1)//2][j] = colors[(N-1)//2][0]

for i in range(N):
    colors[N-1-i][N-1] = colors[i][0]

'''

colors[0][N-1] = colors[0][0]
for j in range(1,N):
    colors[j][0] = colors[0][0]
    colors[j][N-1] = colors[0][0]

if N%2==1:
    for j in range(1,N):
        colors[j][(N-1)//2] = colors[0][(N-1)//2]

for i in range(N):
    colors[N-1][N-1-i] = colors[0][i]


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
            glVertex3fv(vertices[i][j])

    glEnd()

def draw_egg_lines():
    glBegin(GL_LINES)
    

    for i in range(N-1):
        for j in range(N-1):
            glColor3f(1.0, 0.0, 1.0) #pink
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i+1][j])

            glColor3f(1.0, 1.0, 0.0) #yellow
            glVertex3fv(vertices[i][j])
            glVertex3fv(vertices[i][j+1])

    glEnd()

def draw_egg_triangles(): #dlaczego tranpozycja wspolrzednych???
    glBegin(GL_TRIANGLES)
    for i in range(N-1):
        for j in range(N-1):
            #pierwszy trojkat
            glColor3fv(colors[i][j])
            glVertex3fv(vertices[i][j])
            glColor3fv(colors[i+1][j])
            glVertex3fv(vertices[i+1][j])
            glColor3fv(colors[i][j+1])
            glVertex3fv(vertices[i][j+1])
            #drugi trojkat
            glColor3fv(colors[i+1][j])
            glVertex3fv(vertices[i+1][j])
            glColor3fv(colors[i][j+1])
            glVertex3fv(vertices[i][j+1])
            glColor3fv(colors[i+1][j+1])
            glVertex3fv(vertices[i+1][j+1])
            
    glEnd()

def draw_egg_triangles_strip(): 
    for i in range(N-1):
        glBegin(GL_TRIANGLE_STRIP)
        for j in range(N):
            glColor3fv(colors[i][j])
            glVertex3fv(vertices[i][j])
            glColor3fv(colors[(i+1)%N][j])
            glVertex3fv(vertices[(i+1)%N][j])
        glEnd()    

    
def vec_sum(v1,v2):
    return [v1[i]+v2[i] for i in range(len(v1))]

def draw_sierpinski_pyramid(n,peak,a): #stopien rekurencji; ;krawedz-podstawy i jednoczesnie wysokosc
    if n==0:
        glBegin(GL_TRIANGLES)
        glColor3f(1.0,0.0,1.0) #pink
        #pierwszy trojkat
        glVertex3fv(peak)
        glVertex3fv(vec_sum(peak,[ a/2.0,-a, a/2.0]))
        glVertex3fv(vec_sum(peak,[ a/2.0,-a,-a/2.0]))
        glColor3f(1.0,0.0,0.0) #red
	#drugi trojkat
        glVertex3fv(peak)
        glVertex3fv(vec_sum(peak,[ a/2.0,-a, a/2.0]))
        glVertex3fv(vec_sum(peak,[-a/2.0,-a, a/2.0]))
        glColor3f(0.0,1.0,0.0) #green
	#trzeci trojkat
        glVertex3fv(peak)
        glVertex3fv(vec_sum(peak,[-a/2.0,-a,-a/2.0]))
        glVertex3fv(vec_sum(peak,[ a/2.0,-a,-a/2.0]))
        glColor3f(0.0,0.0,1.0) #blue
	#czwarty trojkat
        glVertex3fv(peak)
        glVertex3fv(vec_sum(peak,[-a/2.0,-a,-a/2.0]))
        glVertex3fv(vec_sum(peak,[-a/2.0,-a, a/2.0]))
        glColor3f(1.0,1.0,0.0)
	#piaty trojkat
        glVertex3fv(vec_sum(peak,[ a/2.0,-a, a/2.0]))
        glVertex3fv(vec_sum(peak,[ a/2.0,-a,-a/2.0]))
        glVertex3fv(vec_sum(peak,[-a/2.0,-a, a/2.0]))
        #szosty trojkat
        glVertex3fv(vec_sum(peak,[-a/2.0,-a,-a/2.0]))
        glVertex3fv(vec_sum(peak,[ a/2.0,-a,-a/2.0]))
        glVertex3fv(vec_sum(peak,[-a/2.0,-a, a/2.0]))

        glEnd()
    else:
        #narysuj 5 piramid
        draw_sierpinski_pyramid(n-1,peak,a/2.0)
        draw_sierpinski_pyramid(n-1,vec_sum(peak,[ a/4.0,-a/2.0, a/4.0]),a/2.0)
        draw_sierpinski_pyramid(n-1,vec_sum(peak,[ a/4.0,-a/2.0,-a/4.0]),a/2.0)
        draw_sierpinski_pyramid(n-1,vec_sum(peak,[-a/4.0,-a/2.0, a/4.0]),a/2.0)
        draw_sierpinski_pyramid(n-1,vec_sum(peak,[-a/4.0,-a/2.0,-a/4.0]),a/2.0)

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    
    spin(time * 180.0/pi * 1.0)
    axes()
    #rysowanie obiektu
    draw_egg_dots()
    #draw_egg_lines()
    #draw_egg_triangles()
    #draw_egg_triangles_strip()
    #draw_sierpinski_pyramid(3,[0.0,4.0,0.0],8.0)

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
