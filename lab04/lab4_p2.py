#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

from math import cos, sin, pi, hypot

viewer = [0.0, 0.0, 10.0]
position = [5.0, -0.7, 7.0]

step = 0.2

theta = 0.0
phi = 0.0
pix2angle = 1.0

R = 10.0
up_y = 1.0

#left_mouse_button_pressed = 0
mouse_x_pos_old = 0
delta_x = 0

mouse_y_pos_old = 0
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
    glVertex3f(0.0, -5000.0, 0.0)
    glVertex3f(0.0, 5000.0, 0.0)

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


def update_camera():
    global R
    global theta
    global phi
    global viewer
    global up_y



    phi = min([89.0, max([-89.0, phi])])
    #while(phi > 180.0):
    #    phi -= 360.0

    #while(phi < -180.0):
    #    phi += 360.0

    #now, phi belongs to <-180.0; 180.0>

    #w zaleznosci od kata obroc kamere
    #if phi <= 90.0 and phi >= -90.0:
    #    up_y = 1.0
    #else:
    #    up_y = -1.0

    viewer = [
        R * cos(theta * pi/180.0) * cos(phi * pi/180.0),
	R * sin(phi * pi/180.0),
	R * sin(theta * pi/180.0) * cos(phi * pi/180.0),
    ]




def render(time):
    global theta
    global phi
    global R
    global viewer
    global up_y
    global delta_x
    global delta_y

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    

    #gluLookAt(viewer[0], viewer[1], viewer[2],
    #          0.0, 0.0, 0.0,
    #          0.0, up_y, 0.0)
    
    gluLookAt(position[0], position[1], position[2],
              viewer[0]+position[0], viewer[1] + position[1], viewer[2]+position[2],
              0.0, up_y, 0.0)

    #if left_mouse_button_pressed:
    theta -= delta_x * pix2angle  * up_y
    phi += delta_y * pix2angle# * up_y

    update_camera()

    [delta_x, delta_y] = [0.0, 0.0]

    #glRotatef(theta, 0.0, 1.0, 0.0)

    axes()
    #example_object()
    draw_sierpinski_pyramid(3,[0.0,2.0,0.0],4.0)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width * 10.0

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
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_W and action == GLFW_PRESS:
        #position[0] += step
        position[0] += step*viewer[0]*cos(phi*pi/180.0)/hypot(viewer[0],viewer[2])
        position[2] += step*viewer[2]*cos(phi*pi/180.0)/hypot(viewer[0],viewer[2])
    if key == GLFW_KEY_S and action == GLFW_PRESS:
        #position[0] -= step
        position[0] -= step*viewer[0]*cos(phi*pi/180.0)/hypot(viewer[0],viewer[2])
        position[2] -= step*viewer[2]*cos(phi*pi/180.0)/hypot(viewer[0],viewer[2])
    if key == GLFW_KEY_D and action == GLFW_PRESS:
        position[0] -= step*viewer[2]*cos(phi*pi/180.0)/hypot(viewer[0],viewer[2])
        position[2] += step*viewer[0]*cos(phi*pi/180.0)/hypot(viewer[0],viewer[2])
	#position[2] += step
    if key == GLFW_KEY_A and action == GLFW_PRESS:
        position[0] += step*viewer[2]*cos(phi*pi/180.0)/hypot(viewer[0],viewer[2])
        position[2] -= step*viewer[0]*cos(phi*pi/180.0)/hypot(viewer[0],viewer[2])

	#position[2] -= step
    
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

    #if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
    #    left_mouse_button_pressed = 1
    #else:
    #    left_mouse_button_pressed = 0


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
