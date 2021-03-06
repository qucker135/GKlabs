#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import cos, sin, pi

mode = 2 #1 - obrot obiektu, 2 - poruszanie kamera

maxR = 20.0
R = 10.0
minR = 1.0
up_y = 1.0 #poczatkowo zorientowana w gore

viewer = [0.0, 0.0, 10.0]
#[x_eye, y_eye, z_eye] = [0.0, 0.0, R]

theta = 0.0 #ruch wokol osi y (prawo-lewo)
phi = 0.0   #ruch wokol osi x (gora-dol)
scale = 1.0
scalingRatio = 1.005
pix2angle = 1.0

left_mouse_button_pressed = 0
right_mouse_button_pressed = 0

mouse_x_pos_old = 0 #ruch myszy w osi x, steruje obrotem wokol osi y
delta_x = 0

mouse_y_pos_old = 0 #ruch myszy w osi y, steruje obrotem wokol osi x
delta_y = 0

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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def update_camera():
    global R
    global theta
    global phi
    global viewer
    global up_y

    while(phi > 180.0):
        phi -= 360.0

    while(phi < -180.0):
        phi += 360.0

    #now, phi belongs to <-180.0; 180.0>

    #w zaleznosci od kata obroc kamere
    if phi <= 90.0 and phi >= -90.0:
        up_y = 1.0
    else:
        up_y = -1.0

    viewer = [
        R * cos(theta * pi/180.0) * cos(phi * pi/180.0),
	R * sin(phi * pi/180.0),
	R * sin(theta * pi/180.0) * cos(phi * pi/180.0),
    ]

def render(time):
    global theta
    global phi
    global scale
    global scalingRatio
    global R
    global viewer
    global up_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if mode==2:
        update_camera()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, up_y, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle * up_y #naprawienie sterowania w osi y
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        scale *= scalingRatio
        scale = max([minR, min([maxR,scale])]) 
        R /= scalingRatio
        R = max([minR, min([maxR,R])])

    if mode==1:
        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi,   1.0, 0.0, 0.0)
        glScalef(scale,scale,scale)

    axes()
    example_object()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global mode
    #przywracanie ust. domyslnych w tym miejscu to byl jednak zly pomysl
    #global theta
    #global phi
    #global R

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        mode = 1
        #theta = 0.0
        #phi = 0.0
        #R = 10.0
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        mode = 2
        #theta = 0.0
        #phi = 0.0
        #R = 10.0


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    global delta_y
    global mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed
    global scalingRatio

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_RELEASE:
        scalingRatio = 1.0/scalingRatio


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
